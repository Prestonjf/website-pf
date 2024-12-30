import pathlib
import sys
import logging
import boto3


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def build_config_file():
    try:
        logger.info('Retrieving website-pf ssm parameteters.')
        ssm = boto3.client('ssm')

        website_pf_api_url = ""
        website_pf_api_key = ""
        website_pf_react_web_url = ""
        website_pf_api_url_ssm = f'/{sys.argv[1]}/website-pf/api-gateway/url'
        website_pf_api_key_ssm = f'/{sys.argv[1]}/website-pf/api-gateway/key'
        website_pf_react_web_url_ssm = f'/{sys.argv[1]}/website-pf/acm/url'
        try:
            website_pf_api_url = ssm.get_parameter(Name=website_pf_api_url_ssm, WithDecryption=True)['Parameter']['Value']
            logger.info(f"Retrieved {website_pf_api_url_ssm}")
            website_pf_api_key = ssm.get_parameter(Name=website_pf_api_key_ssm, WithDecryption=True)['Parameter']['Value']
            logger.info(f"Retrieved {website_pf_api_key_ssm}")
            website_pf_react_web_url = ssm.get_parameter(Name=website_pf_react_web_url_ssm, WithDecryption=True)['Parameter']['Value']
            logger.info(f"Retrieved {website_pf_api_key_ssm}")
        except Exception:
            logger.error("Could not retrieve all SSM parameters")

        logger.info('Building website-pf s3 webapp .env file.')
        file = open(str(pathlib.Path(__file__).parent.absolute()) + "/../webapp/website-pf/.env", "w")
        file.write(f"REACT_APP_API_URL={website_pf_api_url}\n")
        file.write(f"REACT_APP_API_KEY={website_pf_api_key}\n")
        file.write(f"REACT_APP_WEB_URL={website_pf_react_web_url}\n")
        file.write("REACT_APP_ENV=prod\n")
        file.close()
        logger.info(".env created at " + str(pathlib.Path(__file__).parent.absolute()) + "/../webapp/website-pf/.env")
        return 1
    except Exception:
        logger.error("ERROR: ", exc_info=True)
    return 1


build_config_file()
