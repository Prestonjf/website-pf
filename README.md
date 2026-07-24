# website-pf

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=alert_status)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=bugs)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=code_smells)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Prestonjf_website-pf&metric=coverage)](https://sonarcloud.io/dashboard?id=Prestonjf_website-pf)


### Live Version: [https://prestonfrazier.net](https://prestonfrazier.net)

This repository contains the website-pfcapplication. This is a personal portfolio and blog site. It is built on an AWS serverless architecture using ReactJS as the frontend webapp and Python with Flask framework utilizing AWS Apigateway and lambda as the backend. See AWS services used for full tech stack. It is deployed using AWS CDK for cloud resources orchestarted with bash scripts. Github actions provide code quality and deployment pipelines.

## Prerequisites
Before you begin, ensure you have met the following requirements:

- AWS CLI & AWS Account Console Access
- Python 3.13
- Poetry 2.1.0+
- Docker
- Node 22+
- CDK 2.1100+


## Branches & Pipeline Actions

This repository uses trunk based development where main is the primary branch. New features and bug work should be completed on branches from main. A pull request should be opened from the feature branch to main when ready for integration.

- `pr`: Runs build, unit tests, and Sonarqube scan.
- `main`: Runs build, unit tests, and Sonarqube scan.
- `release`: Deploys to the configured production stage of the AWS account. Branches should be created from main with the naming schema `release/vX.X.X`


## Deployment Instructions

To deploy website-pf, follow these steps:

1. The following AWS SSM parameters (and subsequent services) need to be configured to allow deployment of website-pf. {stage} represents the stage (or environment name) you are deploying the project for.

```
**/{stage}/domain/name** - Existing route53 hostname that will point to the webapp (Cloudfront Distribution)
**/{stage}/domain/acm/arn** - Existing Amazon Certifiacte Manage certificat arn for the above hostname

**/{stage}/vpc/id**  -  Existing AWS account vpc id where application will be deployed
**/{stage}/vpc/subnet/id** -  Existing AWS account subnet id inside vpc where application will be deployed
**/{stage}/vpc/sg/id**  -  Existing AWS security group id that application lambdas and reosurces will be attached to

**/{stage}/waf/cloudfront/arn** - Optional. If exists, cloudfront distribution will be associated to the Web Application firewall referenced by the arn.

**/{stage}website-pf/rds/hostname** - hostname of MySQL database
**/{stage}website-pf/rds/schema** - schema for application inside MySQL database
**/{stage}website-pf/rds/username** - username of MySQL database
**/{stage}website-pf/rds/password** - password of MySQL database (Use SecureString to protect credential)
```

2. Fetch application resources:

```
$ git clone https://github.com/Prestonjf/website-pf.git
```

3. Deploy project to the desired stage. Your terminal must be authenticated to the AWS account hosting the given stage.

```
$ ./scripts/deploy.sh {stage}
```

## Run Unit Tests

Run the below helper script which will ensure Python and Node dependencies are installed before executing the backend and frontend tests.

```
$ ./scripts/test.sh
```


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
