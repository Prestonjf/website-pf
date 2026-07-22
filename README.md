# website-pf
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=alert_status)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=bugs)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=code_smells)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=coverage)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)


### Live Version: [https://prestonfrazier.net](https://prestonfrazier.net)

This README file describes how to configure and deploy the website-pf application. This is a personal portfolio and blog site. It is built on an AWS serverless architecture using ReactJS as the front-end webapp and Python with Flask framework as the back-end server. See AWS services used for full tech stack. It is deployed using serverless framework.

## Prerequisites
Before you begin, ensure you have met the following requirements:

- AWS CLI & AWS Account Console Access
- Python 3.13
- Poetry 2.1.0+
- Docker
- Node 22+
- CDK 2.1100+


## Deployment Instructions

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

## Testing / Logging

* View website-pf Lambda Cloudwatch logs for information regarding the application's APIs/back end. Log level can be set with environment variable "LOG_LEVEL". (DEBUG|INFO|ERROR)

## Built With

* [AWS CDK](https://aws.amazon.com/cdk//) - AWS Infrastructure as Code
* [Poetry](https://python-poetry.org/) - Python Dependency Management
* [NPM](https://www.npmjs.com/) - Node Dependency Management

## Styling & Linting

- Use [pylint](https://github.com/pylint-dev/pylint) for enforcing coding standards locally.
    - [pyproject.toml](pyproject.toml) is a configuration file for black
    - `uv run pylint {optional directory} --disable=I,R` to see list of linting issues

- Use [black](https://github.com/psf/black) for code formatting alongside pylint.
    - [pyproject.toml](pyproject.toml) is a configuration file for black.
    - `shift + cmd + f` to format.
    - `uv run black {file or directory name} --check` to see what would be formatted.
    - `uv run black {file or directory name}` to run black manually.

- Use [isort](https://pycqa.github.io/isort/) to sort imports.
    - [pyproject.toml](pyproject.toml) is a configuration file for isort.
    - `shift + cmd + o` to format.

## Authors

* [GitHub](https://github.com/Prestonjf) - **Preston Frazier**

## License

* [GNU General Public License v3.0](LICENSE)
