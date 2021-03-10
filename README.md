# website-pf
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=alert_status)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=bugs)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=code_smells)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=coverage)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)


### Live Version: [https://prestonfrazier.net](https://prestonfrazier.net)

This README file describes how to configure and deploy the website-pf application. This is a personal portfolio and blog site. It is built on an AWS serverless architecture using ReactJS as the front-end webapp and Python with Flask framework as the back-end server. See AWS services used for full tech stack. It is deployed using serverless framework.

### Prerequisites
Before you begin, ensure you have met the following requirements:

- 	AWS CLI & AWS Account Console Access

-   NPM

- 	Serverless framework environment

- 	Serverless Plugins: serverless-plugin-scripts, serverless-wsgi serverless-python-requirements


### Deployment Instructions
To deploy website-pf, follow these steps:


**1\.** Fetch application resources:

```
$ git clone https://github.com/Prestonjf/website-pf.git
```


**2\.** Run the following commands to compile the React webapp

```
$ cd website-pf
$ sls webappbuild
$ sls functionlayer
$ sls fulldeploy
```

**3\.** Website-pf uses AWS secrets to store credentials and URLS. Create a new Secrets for the desired environment. Use the plaintext example below and enter to correct environment specific credentials. Copy the Secret ARN for the next step.

```
{

}
```

**4\.** Updated the custom environment variables in serverless.yml

```
custom.accountId.${self:provider.stage} : { AWS Account Id }
custom.acmCertificateArn.${self:provider.stage} : { ARN of your ACM Certificate for your custom domain name }
custom.secretsArn.${self:provider.stage} : { ARN of your AWS Secret for application credentials }
```

**5\.** Deploy website-pf to AWS. Initial deployment will create AWS services via a Cloudformation Stack and subsequent deployments will update these services. Choose the desired stage (dev|prod). Use the following commands:

```
$ serverless fulldeploy -s prod
```

**6\.** If initial deployment, you will need to add the URL for the newly created API gateway to the .env file of the React webapp. Modify the file website-pf/s3-webapp/.env and update the following property. (Rename .env-example to .env first if .env does not exist):

```
REACT_APP_API_URL= { API Gateway execution URL }
REACT_APP_API_KEY= { API Gateway API Key }
REACT_APP_ENV= { environment name (DEV|PROD) }

```

Perform a new React build, and deploy the static resources:

```
$ cd website-pf/s3-webapp
$ npm run-script build

$ serverless fulldeploy -s prod
```

**7\.** Website-pf is now deployed.

- The webapp can be accessed through the domain created by Cloudfront or the domain name from your certificate!

### Testing / Logging

* View website-pf Lambda Cloudwatch logs for information regarding the application's APIs/back end. Log level can be set with environment variable "LOG_LEVEL". (DEBUG|INFO|ERROR)

### AWS Services Used
- S3: Used to store react webapp static content and content related to posts. Also used for serverless framework deployment storage.
- Lambda: NodeJS processing engine to handle dynamic data requests.
- DynamoDB: Database used to index and store metadata about posts.
- API Gateway: Endpoint to handle api calls from the webapp. Secured with API Key and configured with Usage Plan to throttle requests.
- Cloudfront: Used to securely host and quickly deliver static webapp content to the end users.
- Secrets: Stores credentials and urls for website-pf lambda.
- IAM: Custom role created for website-pf lambda in order to access needed services.

### Built With

* [Serverless](https://serverless.com/) - AWS Services Manager
* [NPM](https://www.npmjs.com/) - Dependency Management

### Authors

* [GitHub](https://github.com/Prestonjf) - **Preston Frazier**

### License
* GNU General Public License v3.0
