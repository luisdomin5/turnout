local secrets = import 'include/secrets.libsonnet';

local env_vars = secrets.for_env('$ENVIRONMENT');

local ssm_name_from_arn(ssm_param_arn) = std.splitLimit(ssm_param_arn, '/', 1)[1];

local export_line(env_var_name, ssm_param_arn) =
  'export ' +
  env_var_name +
  '=$(aws ssm get-parameter --region $REGION --with-decryption --name ' +
  ssm_name_from_arn(ssm_param_arn) +
  " | jq '.Parameter[\"Value\"]' -r)";

local export_lines = [
  export_line(env.name, env.valueFrom)
  for env in env_vars
];

local docker_env_line(env_var_name) =
  '    -e ' + env_var_name + ' \\';

local docker_env_lines = [
  docker_env_line(env.name)
  for env in env_vars
];


|||
  #!/bin/bash
  # DO NOT EDIT THIS FILE. It is auto-generated from the template in
  # ecs/template/remote_run.jsonnet
  set -euo pipefail

  REGION=${REGION:-us-west-2}
  ENVIRONMENT=${ENVIRONMENT:-staging}
  DOCKER_REPO_NAME=${DOCKER_REPO_NAME:-turnout}
  DEBUG=${DEBUG:-true}
  ACCOUNT_ID=$(aws sts get-caller-identity | jq -r ".Account")

  if [ $1 ]; then

    echo "Logging into ECR"
    if aws --version | grep -q aws-cli/1; then
      eval $(aws ecr get-login --no-include-email --region $REGION)
    else
      aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
    fi

  fi

  echo "Account ID: $ACCOUNT_ID"
||| + std.join('\n', export_lines) + |||


  echo "Parameters Acquired"


  if aws sts get-caller-identity | grep -q assumed-role; then
    echo 'using EC2 credentials'
  else
    AWS_CRED_DETAILS=$(aws sts get-session-token --duration-seconds 86400)
    export AWS_ACCESS_KEY_ID=$(echo $AWS_CRED_DETAILS | jq '.Credentials["AccessKeyId"]' -r)
    export AWS_SECRET_ACCESS_KEY=$(echo $AWS_CRED_DETAILS | jq '.Credentials["SecretAccessKey"]' -r)
    export AWS_DEFAULT_REGION=$REGION
    echo "AWS Credentials Acquired"
  fi


  if [ $1 ]; then

  IMAGE=$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$DOCKER_REPO_NAME:$1

  else

  echo "Building From Local"
  docker build --cache-from voteamerica/turnout-ci-cache:latest --build-arg TAG_ARG=local --build-arg BUILD_ARG=0 -t turnout_full .
  IMAGE=turnout_full:latest

  fi

  echo "Running Image $IMAGE"
  docker run -i -t \
||| + std.join('\n', docker_env_lines) + |||

  -e DEBUG=$DEBUG \
  -p 8000:8000 \
  $IMAGE \
  /bin/bash
|||
