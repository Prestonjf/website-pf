# Python Lambda App
import logging
import boto3
import datetime
import pytz
import json
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO
from lambda_backend.website_pf_post_loader.src.services import post_service
from lambda_backend.website_pf_post_loader.src.utils import utils
from lambda_backend.website_pf_post_loader.src import config
from lambda_backend.website_pf_post_loader.src.repositories import mysql_repository as mysql


logger = logging.getLogger()
utils.setup_logging(logger)
s3_client = boto3.client('s3', region_name=config.REGION)
s3_resource = boto3.resource('s3', region_name=config.REGION)


def do_post_work():
    post_service.generate_robots()
    post_service.generate_rss()


def lambda_handler(event, context):
    logger.info('Begin Website-PF post processing.')
    posts = {}
    for item in s3_client.list_objects(Bucket=config.S3_WEBSITE_PF_BUCKET, Prefix='upload')['Contents']:
        post_folder = item['Key'].split("/")
        if (post_folder[1] and post_folder[1] not in posts):
            posts[post_folder[1]] = {}

    for key in posts.keys():
        logger.info(f'Processing post {key}')
        post_data = process_post(key)
        if post_data:
            posts[key] = post_data
            logger.info(f'Successfully processed post {key}')
        else:
            logger.error(f'Could not process post {key}')

    # Generate new rss.xml, sitemap.xml, robots.txt, featured.yml - cache control = 0
    post_service.generate_robots()
    post_service.generate_rss()
    post_service.generate_sitemap()
    # post_service.generate_featured()

    logger.info('Finished Website-PF post processing.')
    return 'done'


def process_post(key):
    try:
        post_data = {}
        post_files = []
        post_file_key = 'upload/' + key + '/'

        # Find all post files
        for item in s3_client.list_objects(Bucket=config.S3_WEBSITE_PF_BUCKET, Prefix='upload/' + key)['Contents']:
            file = item['Key'].split('/')
            if (len(file) > 1 and file[2]):
                post_files.append(file[2])
        post_data['post_files'] = post_files

        # Load Post Config
        if 'config.yml' not in post_files:
            return None
        post_data['post_config'] = get_post_config(post_file_key)
        logger.info(f'Loaded post config.yml id: {post_data["post_config"]["idName"]} path: {post_data["post_config"]["id"]}')

        # Set Post Create or Update Info
        timeZ_Ny = pytz.timezone('America/New_York')
        current_time = datetime.datetime.now(timeZ_Ny)
        if post_data['post_config']['id']:
            # post_data['post_config']['id']
            post_data['process_mode'] = 'UPDATE'
            post_data['post_config']['updatedDate'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f'Updating {post_data["post_config"]["idName"]}')
        else:
            post_data['post_config']['id'] = f'{current_time.strftime("%Y")}/{current_time.strftime("%m")}/{current_time.strftime("%d")}/{post_data["post_config"]["idName"]}'
            post_data['process_mode'] = 'CREATE'
            post_data['post_config']['createdDate'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f'Creating {post_data["post_config"]["idName"]}')

        # Process Author
        author = post_data['post_config']['author']
        post_data['post_config']['author']['id'] = get_add_author(author['username'], author['name'])
        logger.info(f'Processed author for {post_data["post_config"]["idName"]}')

        # Process Post HTML
        html_file_s3 = post_data['post_config']['htmlFile']
        post_data['post_html'] = get_s3_file_text(post_file_key, html_file_s3)
        post_data['post_html'] = replace_html_dynamic_values(post_data['post_html'])
        post_data['post_config']['htmlFile'] = f'post_{current_time.strftime("%Y%m%d%H%M%S")}.html'
        logger.info(f'Processed HTML for {post_data["post_config"]["idName"]}')

        # Process Post Attributes
        post_data['post_config']['post_db_id'] = create_update_post(post_data['post_config'], post_data['process_mode'])
        logger.info(f'Database updated for {post_data["post_config"]["idName"]}')

        # Move All Post files to s3 key path
        for file in post_files:
            if 'config.yml' == file:
                # Write new config file
                cache_control = 'maxage=0,s-maxage=0'
                content_type = 'text/yaml'
                config_obj = s3_resource.Object(config.S3_WEBSITE_PF_BUCKET, f'posts/{post_data["post_config"]["id"]}/config.yml')
                yaml = YAML(typ='safe')
                stream = StringIO()
                yaml.dump(post_data["post_config"], stream)
                config_obj.put(Body=stream.getvalue().encode(), ContentType=content_type, CacheControl=cache_control)
            elif html_file_s3 == file:
                # rename html file
                content_type = 'text/html'
                html_file_s3_key = f'posts/{post_data["post_config"]["id"]}/{post_data["post_config"]["htmlFile"]}'
                config_obj = s3_resource.Object(config.S3_WEBSITE_PF_BUCKET, html_file_s3_key)
                config_obj.put(Body=post_data['post_html'], ContentType=content_type)
                # Upload old html file to archive and delete from posts folder
                archive_html_file(post_data["post_config"]["id"], html_file_s3)
            else:
                # move files to post folder
                s3_resource.Object(
                    config.S3_WEBSITE_PF_BUCKET,
                    f'posts/{post_data["post_config"]["id"]}/{file}'
                ).copy_from(CopySource={'Bucket': config.S3_WEBSITE_PF_BUCKET, 'Key': f'{post_file_key}{file}'})

        post_data['status'] = 'success'
        logger.info(f'Files moved for {post_data["post_config"]["idName"]} {post_files}')

        bucket = s3_resource.Bucket(config.S3_WEBSITE_PF_BUCKET)
        bucket.objects.filter(Prefix=post_file_key).delete()
        logger.info(f'Upload files deleted for {post_file_key}')

        return post_data
    except Exception:
        logger.error(f'Cannot process post {key}', exc_info=True)
        post_data['status'] = 'failure'
        return None


def get_post_config(post_file_key):
    obj = s3_resource.Object(config.S3_WEBSITE_PF_BUCKET, post_file_key + 'config.yml')
    body = obj.get()['Body'].read()
    yaml = YAML(typ='safe')
    post_config = yaml.load(body)
    return post_config


def get_s3_file_text(post_file_key, html_file):
    obj = s3_resource.Object(config.S3_WEBSITE_PF_BUCKET, post_file_key + html_file)
    body = obj.get()['Body'].read()
    return str(body.decode())


def replace_html_dynamic_values(html):
    # Replace with domain name $$_domain_$$
    html = html.replace('$$_domain_$$', config.WEBSITE_URL)
    return html


def archive_html_file(id_name, html_file_name):
    try:
        s3_client.copy_object(
            Bucket=config.S3_WEBSITE_PF_BUCKET,
            Key=f'posts/{id_name}/archive/{html_file_name}',
            CopySource={
                'Bucket': config.S3_WEBSITE_PF_BUCKET,
                'Key': f'posts/{id_name}/{html_file_name}'
            }
        )
        s3_client.delete_object(
            Bucket=config.S3_WEBSITE_PF_BUCKET,
            Key=f'posts/{id_name}/{html_file_name}',
        )
    except Exception:
        logger.warning(f"Unable to archive file: posts/{id_name}/{html_file_name}. It might not exist.")


def get_add_author(username, displayName):
    sql = 'select id from author where username = %s'
    params = [(username)]
    data = mysql.mysql_select(sql, params)
    if data and len(data) > 0:
        return data[0][0]
    else:
        sql = 'insert into author (username, display_name) values (%s, %s)'
        params = [username, displayName]
        return mysql.mysql_modify(sql, params)


def create_update_post(config, mode):
    sql = ''
    params = []
    if 'CREATE' == mode:
        sql = '''insert into post (post_s3_path, post_name, post_html_path, primary_image_path, thumbnail_image_path, post_summary, author_id, meta, post_url)
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
        params.append(f's3://{config.S3_WEBSITE_PF_BUCKET}/posts/{config["id"]}')
    else:
        sql = '''update post set post_name=%s, post_html_path=%s, primary_image_path=%s, thumbnail_image_path=%s, post_summary=%s, author_id=%s, meta=%s,
            updated_date=now() where post_url=%s'''

    params.append(config['name'])
    params.append(config['htmlFile'])
    params.append(config['primaryImageFile'])
    params.append(config['primaryImageThumbnail'])
    params.append(config['summary'])
    params.append(config['author']['id'])

    # Process Tags
    post_meta = {}
    post_meta['tags'] = config['tags']
    params.append(json.dumps(post_meta))

    params.append(config['id'])

    return mysql.mysql_modify(sql, params)
