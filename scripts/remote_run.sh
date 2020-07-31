#!/bin/bash
# DO NOT EDIT THIS FILE. It is auto-generated from the template in
# ecs/template/remote_run.jsonnet

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
export DATABASE_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.database_url | jq '.Parameter["Value"]' -r)
export DATABASE_MAX_CONNECTIONS=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.database_max_connections | jq '.Parameter["Value"]' -r)
export TARGETSMART_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.targetsmart_key | jq '.Parameter["Value"]' -r)
export REDIS_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.redis_url | jq '.Parameter["Value"]' -r)
export SECRET_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.secret_key | jq '.Parameter["Value"]' -r)
export ALLOWED_HOSTS=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.allowed_hosts | jq '.Parameter["Value"]' -r)
export SENTRY_DSN=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.sentry_dsn | jq '.Parameter["Value"]' -r)
export MULTIFACTOR_ISSUER=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.multifactor_issuer | jq '.Parameter["Value"]' -r)
export ATTACHMENT_USE_S3=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.use_s3 | jq '.Parameter["Value"]' -r)
export AWS_STORAGE_BUCKET_NAME=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.public_storage_bucket | jq '.Parameter["Value"]' -r)
export AWS_STORAGE_PRIVATE_BUCKET_NAME=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.private_storage_bucket | jq '.Parameter["Value"]' -r)
export SENDGRID_API_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.sendgrid_api_key | jq '.Parameter["Value"]' -r)
export FILE_TOKEN_RESET_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.file_token_reset_url | jq '.Parameter["Value"]' -r)
export PRIMARY_ORIGIN=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.primary_origin | jq '.Parameter["Value"]' -r)
export USVOTEFOUNDATION_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.usvf_key | jq '.Parameter["Value"]' -r)
export ALLOY_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.alloy_key | jq '.Parameter["Value"]' -r)
export ALLOY_SECRET=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.alloy_secret | jq '.Parameter["Value"]' -r)
export CLOUDFLARE_ZONE=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.cloudflare_zone | jq '.Parameter["Value"]' -r)
export CLOUDFLARE_TOKEN=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.cloudflare_token | jq '.Parameter["Value"]' -r)
export CLOUDFLARE_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.cloudflare_enabled | jq '.Parameter["Value"]' -r)
export ABSENTEE_LEO_EMAIL_DISABLE=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.leo_email_disable | jq '.Parameter["Value"]' -r)
export ABSENTEE_LEO_EMAIL_OVERRIDE_ADDRESS=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.leo_email_override_address | jq '.Parameter["Value"]' -r)
export ABSENTEE_LEO_EMAIL_FROM=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.leo_email_from | jq '.Parameter["Value"]' -r)
export TWILIO_ACCOUNT_SID=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.twilio_account_sid | jq '.Parameter["Value"]' -r)
export TWILIO_AUTH_TOKEN=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.twilio_auth_token | jq '.Parameter["Value"]' -r)
export TWILIO_MESSAGING_SERVICE_SID=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.twilio_messaging_service_sid | jq '.Parameter["Value"]' -r)
export SMS_OPTIN_REMINDER_DELAY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.sms_optin_reminder_delay | jq '.Parameter["Value"]' -r)
export SMS_POST_SIGNUP_ALERT=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.sms_post_signup_alert | jq '.Parameter["Value"]' -r)
export MULTIFACTOR_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.multifactor_enabled | jq '.Parameter["Value"]' -r)
export TWO_FACTOR_SMS_NUMBER=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.two_factor_sms_number | jq '.Parameter["Value"]' -r)
export GEOCODIO_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.geocodio_key | jq '.Parameter["Value"]' -r)
export FAX_DISABLE=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.fax_disable | jq '.Parameter["Value"]' -r)
export FAX_OVERRIDE_DEST=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.fax_override_dest | jq '.Parameter["Value"]' -r)
export FAX_GATEWAY_CALLBACK_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.fax_gateway_callback_url | jq '.Parameter["Value"]' -r)
export FAX_GATEWAY_SQS_QUEUE=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.fax_gateway_sqs_queue | jq '.Parameter["Value"]' -r)
export SLACK_DATA_ERROR_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.slack_data_error_enabled | jq '.Parameter["Value"]' -r)
export SLACK_DATA_ERROR_WEBHOOK=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.slack_data_error_webhook | jq '.Parameter["Value"]' -r)
export USVF_SYNC=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.usvf_sync | jq '.Parameter["Value"]' -r)
export USVF_SYNC_HOUR=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.usvf_sync_hour | jq '.Parameter["Value"]' -r)
export USVF_GEOCODE=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.usvf_geocode | jq '.Parameter["Value"]' -r)
export DD_API_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name general.datadogkey | jq '.Parameter["Value"]' -r)
export REGISTER_CO_VRD_ID=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.register_co_vrd_id | jq '.Parameter["Value"]' -r)
export REGISTER_CO_VRD_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.register_co_vrd_enabled | jq '.Parameter["Value"]' -r)
export REGISTER_WA_VRD_ID=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.register_wa_vrd_id | jq '.Parameter["Value"]' -r)
export REGISTER_WA_VRD_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.register_wa_vrd_enabled | jq '.Parameter["Value"]' -r)
export ACTIONNETWORK_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.actionnetwork_key | jq '.Parameter["Value"]' -r)
export ACTIONNETWORK_SYNC=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.actionnetwork_sync | jq '.Parameter["Value"]' -r)
export ACTIONNETWORK_SYNC_DAILY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.actionnetwork_sync_daily | jq '.Parameter["Value"]' -r)
export ACTIONNETWORK_SYNC_HOUR=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.actionnetwork_sync_hour | jq '.Parameter["Value"]' -r)
export ACTIONNETWORK_FORM_PREFIX=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.actionnetwork_form_prefix | jq '.Parameter["Value"]' -r)
export OPTIMIZELY_SDK_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.optimizely_sdk_key | jq '.Parameter["Value"]' -r)
export OVBM_SYNC=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.ovbm_sync | jq '.Parameter["Value"]' -r)
export PA_OVR_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.pa_ovr_key | jq '.Parameter["Value"]' -r)
export PA_OVR_STAGING=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.pa_ovr_staging | jq '.Parameter["Value"]' -r)
export SLACK_SUBSCRIBER_INTEREST_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.slack_subscriber_interest_enabled | jq '.Parameter["Value"]' -r)
export SLACK_SUBSCRIBER_INTEREST_WEBHOOK=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.slack_subscriber_interest_webhook | jq '.Parameter["Value"]' -r)
export API_KEY_PEPPER=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.api_key_pepper | jq '.Parameter["Value"]' -r)
export REGISTER_RESUME_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.register_resume_url | jq '.Parameter["Value"]' -r)

echo "Parameters Acquired"


AWS_CRED_DETAILS=$(aws sts get-session-token --duration-seconds 86400)
export AWS_ACCESS_KEY_ID=$(echo $AWS_CRED_DETAILS | jq '.Credentials["AccessKeyId"]' -r)
export AWS_SECRET_ACCESS_KEY=$(echo $AWS_CRED_DETAILS | jq '.Credentials["SecretAccessKey"]' -r)
export AWS_DEFAULT_REGION=$REGION

echo "AWS Credentials Acquired"


if [ $1 ]; then

IMAGE=$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$DOCKER_REPO_NAME:$1

else

echo "Building From Local"
docker build --cache-from voteamerica/turnout-ci-cache:latest --build-arg TAG_ARG=local --build-arg BUILD_ARG=0 -t turnout_full .
IMAGE=turnout_full:latest

fi

echo "Running Image $IMAGE"
docker run -i -t \
    -e DATABASE_URL \
    -e DATABASE_MAX_CONNECTIONS \
    -e TARGETSMART_KEY \
    -e REDIS_URL \
    -e SECRET_KEY \
    -e ALLOWED_HOSTS \
    -e SENTRY_DSN \
    -e MULTIFACTOR_ISSUER \
    -e ATTACHMENT_USE_S3 \
    -e AWS_STORAGE_BUCKET_NAME \
    -e AWS_STORAGE_PRIVATE_BUCKET_NAME \
    -e SENDGRID_API_KEY \
    -e FILE_TOKEN_RESET_URL \
    -e PRIMARY_ORIGIN \
    -e USVOTEFOUNDATION_KEY \
    -e ALLOY_KEY \
    -e ALLOY_SECRET \
    -e CLOUDFLARE_ZONE \
    -e CLOUDFLARE_TOKEN \
    -e CLOUDFLARE_ENABLED \
    -e ABSENTEE_LEO_EMAIL_DISABLE \
    -e ABSENTEE_LEO_EMAIL_OVERRIDE_ADDRESS \
    -e ABSENTEE_LEO_EMAIL_FROM \
    -e TWILIO_ACCOUNT_SID \
    -e TWILIO_AUTH_TOKEN \
    -e TWILIO_MESSAGING_SERVICE_SID \
    -e SMS_OPTIN_REMINDER_DELAY \
    -e SMS_POST_SIGNUP_ALERT \
    -e MULTIFACTOR_ENABLED \
    -e TWO_FACTOR_SMS_NUMBER \
    -e GEOCODIO_KEY \
    -e FAX_DISABLE \
    -e FAX_OVERRIDE_DEST \
    -e FAX_GATEWAY_CALLBACK_URL \
    -e FAX_GATEWAY_SQS_QUEUE \
    -e SLACK_DATA_ERROR_ENABLED \
    -e SLACK_DATA_ERROR_WEBHOOK \
    -e USVF_SYNC \
    -e USVF_SYNC_HOUR \
    -e USVF_GEOCODE \
    -e DD_API_KEY \
    -e REGISTER_CO_VRD_ID \
    -e REGISTER_CO_VRD_ENABLED \
    -e REGISTER_WA_VRD_ID \
    -e REGISTER_WA_VRD_ENABLED \
    -e ACTIONNETWORK_KEY \
    -e ACTIONNETWORK_SYNC \
    -e ACTIONNETWORK_SYNC_DAILY \
    -e ACTIONNETWORK_SYNC_HOUR \
    -e ACTIONNETWORK_FORM_PREFIX \
    -e OPTIMIZELY_SDK_KEY \
    -e OVBM_SYNC \
    -e PA_OVR_KEY \
    -e PA_OVR_STAGING \
    -e SLACK_SUBSCRIBER_INTEREST_ENABLED \
    -e SLACK_SUBSCRIBER_INTEREST_WEBHOOK \
    -e API_KEY_PEPPER \
    -e REGISTER_RESUME_URL \
-e DEBUG=$DEBUG \
-p 8000:8000 \
$IMAGE \
/bin/bash

