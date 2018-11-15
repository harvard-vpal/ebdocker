# ebdocker
Deploy utilities for Django apps on AWS Elastic Beanstalk Multicontainer Docker

Used for django apps that have the following container architecture:
* web
* nginx
* worker (optional)

## Files

* `bin/`:
    * `build_and_push`: Build images and push to container registry (i.e. ECR)
    * `deploy`: Generate Dockerrun.aws.json and deploy using EB CLI
    * `head_commit`: Helper script to get current head commit hash of the app
* `scripts`:
    * `generate_dockerrun_aws_json.py`: Used by `bin/deploy` to generate `Dockerrun.aws.json` file
* `nginx`
    * `Dockerfile`: Dockerfile that can be used to build nginx image


## Configuration

### Environment variables
An `.env` file should be set up (working directory where these scripts will be called from; typically not in this repo) which should include:

* `ECR_REGISTRY`
* `AWS_DEFAULT_REGION`
* `APP_IMAGE`
* `APP_CONTEXT`
* `APP_DOCKERFILE`
* `NGINX_IMAGE`
* `NGINX_CONTEXT`
* `NGINX_DOCKERFILE`
* `APP_SETTINGS_DOCKERFILE`
* `EBDOCKER_CONTEXT`
* `DOCKERRUN_TEMPLATE`

Example `.env` file:
```
ECR_REGISTRY=361808764124.dkr.ecr.us-east-1.amazonaws.com
AWS_DEFAULT_REGION=us-east-1
APP_IMAGE=361808764124.dkr.ecr.us-east-1.amazonaws.com/bridge/app
APP_CONTEXT=/Users/me/bridge-adaptivity/bridge_adaptivity
APP_DOCKERFILE=/Users/me/ebdeploy-bridge-adaptivity/app/Dockerfile
NGINX_IMAGE=361808764124.dkr.ecr.us-east-1.amazonaws.com/bridge/nginx
NGINX_CONTEXT=nginx
NGINX_DOCKERFILE=ebdocker/nginx/Dockerfile
APP_SETTINGS_DOCKERFILE=/Users/me/ebdeploy-bridge-adaptivity/app/Dockerfile_settings
EBDOCKER_CONTEXT=/Users/me/ebdocker
DOCKERRUN_TEMPLATE=/Users/me/ebdeploy-bridge-adaptivity/dockerrun/Dockerrun.aws.template.json
```
