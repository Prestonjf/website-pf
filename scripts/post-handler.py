import sys
import logging
import argparse
import boto3
import os

parser = argparse.ArgumentParser(description='Read in a file containing HL7 messages and send them somewhere. Ask developer for usage help.')
parser.add_argument('--action', type=str, required=True, help='Action for the post handler')
parser.add_argument('--postKey', type=str, required=True, help='Post key for the post')
args = parser.parse_args()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

s3_resource = boto3.resource('s3')

# Download Post - python3 post-handler.py --action download --postKey posts/portfolio
# Upload Post - python3 post-handler.py --action upload --postKey
# Run Post Loader - python3 post-handler.py --action loader


def main():
    try:
        action = args.action
        if action:
            logger.info(f'Starting post handler with action {action}')

            if 'loader' == action:
                lambda_client = boto3.client('lambda')
                lambda_client.invoke(FunctionName='website-pf-post-loader-prod')

            elif 'download' == action:
                download_post(args.postKey)
        
        else:
            logger.info('No action specified for post handler')
    except Exception:
        logger.error("ERROR: ", exc_info=True)


def download_post(post_path):
    bucket = s3_resource.Bucket('website-pf-prod')
    for obj in bucket.objects.filter(Prefix=post_path):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key)


main()
