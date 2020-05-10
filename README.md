# Website prestonfrazier.net

This README file describes how to configure and deploy the prestonfrazier.net website. This is a personal portfolio site. It is built on a serverless architecture using ReactJS as the front end webapp and AWS API Gateway and NodeJS Lambda as the back end server. It is deployed using serverless framework.

### Prerequisites
Before you begin, ensure you have met the following requirements:

- 	AWS Account Console Access

-	  NPM

- 	Serverless framework environment

- 	Serverless-s3-deploy, Serverless-s3-sync plugin


### Deployment Instructions
To deploy website-pf, follow these steps:


**1\.** Fetch application resources:

```
$ git clone https://github.com/Prestonjf/website-pf.git
```


**2\.** Run the following commands to compile the React webapp

```
$ cd website-pf/s3-webapp
$ npm run-script build
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
$ serverless deploy -s prod
$ sls s3deploy -s prod
$ sls s3sync -s prod
```

**6\.** If initial deployment, you will need to add the URL for the newly created API gateway to the .env file of the React webapp. Modify the file website-pf/s3-webapp/.env and update the following property:

```
REACT_APP_API_URL= { API Gateway execution URL }
```

Perform a new React build, and deploy the static resources:

```
$ cd website-pf/s3-webapp
$ npm run-script build

$ sls s3deploy -s prod
$ sls s3sync -s prod
```

**7\.** Website-pf is now deployed.

- The webapp can be accessed through the domain created by Cloudfront or the domain name from your certificate!

### Testing / Logging

* View website-pf Lambda Cloudwatch logs for information regarding the application's APIs/back end. Log level can be set with environment variable "LOG_LEVEL". (DEBUG|INFO|ERROR)

### AWS Services Used
- S3: Used to store react webapp static content. Also used for serverless framework deployment storage.
- Lambda: NodeJS processing engine to handle dynamic data requests.
- API Gateway: Endpoint to handle api calls from the webapp.
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
