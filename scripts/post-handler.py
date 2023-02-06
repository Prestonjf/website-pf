import sys
import logging
import argparse
import boto3
import os

parser = argparse.ArgumentParser(description='Read in a file containing HL7 messages and send them somewhere. Ask developer for usage help.')
parser.add_argument('--action', type=str, required=True, help='Action for the post handler')
parser.add_argument('--stage', type=str, required=True, help='Stage to apply changes')
parser.add_argument('--postKey', type=str, required=False, help='Post key for the post')
args = parser.parse_args()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

s3_resource = boto3.resource('s3')

# Download Post - python3 post-handler.py --stage prod --action download --postKey posts/portfolio
# Upload Post - python3 post-handler.py --stage prod --action upload --postKey
# Run Post Loader - python3 post-handler.py --stage prod --action loader


def main():
    try:
        action = args.action
        stage = args.stage
        post_key = args.postKey
        if action and stage:
            logger.info(f'Starting post handler with action {action} in {stage}')

            if 'loader' == action:
                lambda_client = boto3.client('lambda')
                lambda_client.invoke(FunctionName=f'website-pf-post-loader-{stage}')

            elif 'download' == action:
                download_post(post_key, stage)

            elif 'upload' == action:
                upload_post(post_key, stage)

        else:
            logger.info('No action or stage specified for post handler')
    except Exception:
        logger.error("ERROR: ", exc_info=True)


def download_post(post_path, stage):
    logger.info(f'downloading post to {post_path}')
    bucket = s3_resource.Bucket(f'website-pf-{stage}')
    for obj in bucket.objects.filter(Prefix=post_path):
        logger.info(f'downloading {obj.key}')
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        if not obj.key.endswith("/"):
            bucket.download_file(obj.key, obj.key)


def upload_post(post_path, stage):
    s3_client = boto3.client('s3')
    new_post_path = post_path.replace('posts', 'upload').split("/")
    new_post_path = f'{new_post_path[0]}/{new_post_path[len(new_post_path) - 1]}'
    logger.info(f'uploading post to {new_post_path}')
    directory = os.fsencode(post_path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if not filename.endswith("/") and not filename.startswith('archive'):
            key = f'{new_post_path}/{filename}'
            logger.info(f'uploading {key}')
            s3_client.put_object(
                Bucket=f'website-pf-{stage}',
                Key=key,
                Body=open(f'{post_path}/{filename}', 'rb')
            )


main()
