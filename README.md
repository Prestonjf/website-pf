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

- AWS CLI & AWS Account Console Access
- NPM/NodeJS v14+
- Python v3.13+
- Poetry v1.6+
- Serverless Framework v3


### Deployment Instructions
To deploy website-pf, follow these steps:

**1\.** The following SSM parameters and subsequent services need to be configured to allow deployment of website-pf

```
/prod/waf/cloudfront/arn  -  AWS account web application firewall (WAF) ARN for cloudfront distribution
/prod/website-pf/vpc/id  -  AWS account vpc id where application will be deployed
/prod/website-pf/vpc/subnet/id  -  AWS account subnet id where application will be deployed
/prod/website-pf/vpc/sg/id  -  AWS security group id that application will be attached to

/prod/website-pf/acm/arn  -  domain name certificate ARN for website-pf application
/prod/website-pf/acm/url  - domain name where website-pf application is hosted

/prod/website-pf/rds/hostname  -  mysql database hostname
/prod/website-pf/rds/username  -  mysql database username
/prod/website-pf/rds/password  -  mysql database password
/prod/website-pf/rds/schema  - mysql database schema name for website-pf Application
```


**2\.** Fetch application resources:

```
$ git clone https://github.com/Prestonjf/website-pf.git
$ ./deploy.sh prod
```

### Testing / Logging

* View website-pf Lambda Cloudwatch logs for information regarding the application's APIs/back end. Log level can be set with environment variable "LOG_LEVEL". (DEBUG|INFO|ERROR)

### AWS Services Used
- S3: Used to store react webapp static content and content related to posts. Also used for serverless framework deployment storage.
- Lambda: NodeJS processing engine to handle dynamic data requests.
- RDS-MySQL: Database used to index and store metadata about posts.
- API Gateway: Endpoint to handle api calls from the webapp. Secured with API Key and configured with Usage Plan to throttle requests.
- Cloudfront: Used to securely host and quickly deliver static webapp content to the end users.
- Secrets: Stores credentials and urls for website-pf lambda.
- IAM: Custom role created for website-pf lambda in order to access needed services.

### Built With

* [Serverless](https://serverless.com/) - AWS Services Manager
* [NPM](https://www.npmjs.com/) - Node Dependency Management
* [Poetry](https://python-poetry.org/) - Python Dependency Management

### Authors

* [GitHub](https://github.com/Prestonjf) - **Preston Frazier**

### License
* GNU General Public License v3.0
