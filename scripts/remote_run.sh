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
export DATABASE_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.database_url | jq '.Parameter["Value"]' -r)
export READONLY_DATABASE_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.readonly_database_url | jq '.Parameter["Value"]' -r)
export DATABASE_MAX_CONNECTIONS=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.database_max_connections | jq '.Parameter["Value"]' -r)
export REDIS_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.redis_url | jq '.Parameter["Value"]' -r)
export AMQP_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.amqp_url | jq '.Parameter["Value"]' -r)
export SECRET_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.secret_key | jq '.Parameter["Value"]' -r)
export SENTRY_DSN=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.sentry_dsn | jq '.Parameter["Value"]' -r)
export USVF_SYNC=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.usvf_sync | jq '.Parameter["Value"]' -r)
export USVF_SYNC_HOUR=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.usvf_sync_hour | jq '.Parameter["Value"]' -r)
export ACTIONNETWORK_SYNC=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.actionnetwork_sync | jq '.Parameter["Value"]' -r)
export ACTIONNETWORK_SYNC_DAILY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.actionnetwork_sync_daily | jq '.Parameter["Value"]' -r)
export ACTIONNETWORK_SYNC_HOUR=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.actionnetwork_sync_hour | jq '.Parameter["Value"]' -r)
export OVBM_SYNC=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.ovbm_sync | jq '.Parameter["Value"]' -r)
export UPTIME_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.uptime_enabled | jq '.Parameter["Value"]' -r)
export FILE_PURGE_DAYS=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.file_purge_days | jq '.Parameter["Value"]' -r)
export STATE_TOOL_REDIRECT_SYNC=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.state_tool_redirect_sync | jq '.Parameter["Value"]' -r)
export TARGETSMART_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.targetsmart_key | jq '.Parameter["Value"]' -r)
export ALLOWED_HOSTS=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.allowed_hosts | jq '.Parameter["Value"]' -r)
export MULTIFACTOR_ISSUER=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.multifactor_issuer | jq '.Parameter["Value"]' -r)
export ATTACHMENT_USE_S3=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.use_s3 | jq '.Parameter["Value"]' -r)
export AWS_STORAGE_BUCKET_NAME=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.public_storage_bucket | jq '.Parameter["Value"]' -r)
export AWS_STORAGE_PRIVATE_BUCKET_NAME=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.private_storage_bucket | jq '.Parameter["Value"]' -r)
export SENDGRID_API_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.sendgrid_api_key | jq '.Parameter["Value"]' -r)
export FILE_TOKEN_RESET_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.file_token_reset_url | jq '.Parameter["Value"]' -r)
export PRIMARY_ORIGIN=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.primary_origin | jq '.Parameter["Value"]' -r)
export WWW_ORIGIN=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.www_origin | jq '.Parameter["Value"]' -r)
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
export SMS_OPTOUT_NUMBER=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.sms_optout_number | jq '.Parameter["Value"]' -r)
export SMS_OPTOUT_POLL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.sms_optout_poll | jq '.Parameter["Value"]' -r)
export MULTIFACTOR_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.multifactor_enabled | jq '.Parameter["Value"]' -r)
export TWO_FACTOR_SMS_NUMBER=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.two_factor_sms_number | jq '.Parameter["Value"]' -r)
export GEOCODIO_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.geocodio_key | jq '.Parameter["Value"]' -r)
export FAX_DISABLE=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.fax_disable | jq '.Parameter["Value"]' -r)
export FAX_OVERRIDE_DEST=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.fax_override_dest | jq '.Parameter["Value"]' -r)
export FAX_GATEWAY_CALLBACK_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.fax_gateway_callback_url | jq '.Parameter["Value"]' -r)
export FAX_GATEWAY_SQS_QUEUE=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.fax_gateway_sqs_queue | jq '.Parameter["Value"]' -r)
export SLACK_DATA_ERROR_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.slack_data_error_enabled | jq '.Parameter["Value"]' -r)
export SLACK_DATA_ERROR_WEBHOOK=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.slack_data_error_webhook | jq '.Parameter["Value"]' -r)
export USVF_GEOCODE=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.usvf_geocode | jq '.Parameter["Value"]' -r)
export DD_API_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name general.datadogkey | jq '.Parameter["Value"]' -r)
export REGISTER_CO_VRD_ID=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.register_co_vrd_id | jq '.Parameter["Value"]' -r)
export REGISTER_CO_VRD_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.register_co_vrd_enabled | jq '.Parameter["Value"]' -r)
export REGISTER_WA_VRD_ID=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.register_wa_vrd_id | jq '.Parameter["Value"]' -r)
export REGISTER_WA_VRD_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.register_wa_vrd_enabled | jq '.Parameter["Value"]' -r)
export ACTIONNETWORK_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.actionnetwork_key | jq '.Parameter["Value"]' -r)
export OPTIMIZELY_SDK_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.optimizely_sdk_key | jq '.Parameter["Value"]' -r)
export SLACK_SUBSCRIBER_INTEREST_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.slack_subscriber_interest_enabled | jq '.Parameter["Value"]' -r)
export SLACK_SUBSCRIBER_INTEREST_WEBHOOK=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.slack_subscriber_interest_webhook | jq '.Parameter["Value"]' -r)
export API_KEY_PEPPER=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.api_key_pepper | jq '.Parameter["Value"]' -r)
export DIGITALOCEAN_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.digitalocean_key | jq '.Parameter["Value"]' -r)
export UPTIME_TWITTER_CONSUMER_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.uptime_twitter_consumer_key | jq '.Parameter["Value"]' -r)
export UPTIME_TWITTER_CONSUMER_SECRET=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.uptime_twitter_consumer_secret | jq '.Parameter["Value"]' -r)
export UPTIME_TWITTER_ACCESS_TOKEN=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.uptime_twitter_access_token | jq '.Parameter["Value"]' -r)
export UPTIME_TWITTER_ACCESS_TOKEN_SECRET=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.uptime_twitter_access_token_secret | jq '.Parameter["Value"]' -r)
export SLACK_UPTIME_WEBHOOK=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.slack_uptime_webhook | jq '.Parameter["Value"]' -r)
export PROXY_SSH_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.proxy_ssh_key | jq '.Parameter["Value"]' -r)
export PROXY_SSH_PUB=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.proxy_ssh_pub | jq '.Parameter["Value"]' -r)
export PROXY_SSH_KEY_ID=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.proxy_ssh_key_id | jq '.Parameter["Value"]' -r)
export PROXY_TAG=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.proxy_tag | jq '.Parameter["Value"]' -r)
export SELENIUM_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.selenium_url | jq '.Parameter["Value"]' -r)
export REGISTER_RESUME_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.register_resume_url | jq '.Parameter["Value"]' -r)
export FILE_TOKEN_PURGED_URL=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.file_token_purged_url | jq '.Parameter["Value"]' -r)
export PDF_GENERATION_LAMBDA_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.pdf_generation_lambda_enabled | jq '.Parameter["Value"]' -r)
export PDF_GENERATION_LAMBDA_FUNCTION=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.pdf_generation_lambda_function | jq '.Parameter["Value"]' -r)
export LOB_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.lob_key | jq '.Parameter["Value"]' -r)
export LOB_LETTER_WEBHOOK_SECRET=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.lob_letter_webhook_secret | jq '.Parameter["Value"]' -r)
export RETURN_ADDRESS=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.return_address | jq '.Parameter["Value"]' -r)
export BEAT_STATS_METRIC_NAMESPACE=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.beat_stats_metric_namespace | jq '.Parameter["Value"]' -r)
export I90_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.i90_key | jq '.Parameter["Value"]' -r)
export MOVER_ID=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.mover_id | jq '.Parameter["Value"]' -r)
export MOVER_SECRET=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.mover_secret | jq '.Parameter["Value"]' -r)
export MOVER_SOURCE=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.mover_source | jq '.Parameter["Value"]' -r)
export MOVER_LEADS_ENDPOINT=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.mover_leads_endpoint | jq '.Parameter["Value"]' -r)
export SLACK_ALLOY_UPDATE_ENABLED=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.slack_alloy_update_enabled | jq '.Parameter["Value"]' -r)
export SLACK_ALLOY_UPDATE_WEBHOOK=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.slack_alloy_update_webhook | jq '.Parameter["Value"]' -r)
export MAPBOX_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.mapbox_key | jq '.Parameter["Value"]' -r)
export MMS_ATTACHMENT_BUCKET=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.mms_attachment_bucket | jq '.Parameter["Value"]' -r)
export CIVIC_KEY=$(aws ssm get-parameter --region $REGION --with-decryption --name turnout.$ENVIRONMENT.civic_key | jq '.Parameter["Value"]' -r)

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

if [ "$2" ]; then
  docker run \
    -e DATABASE_URL \
    -e READONLY_DATABASE_URL \
    -e DATABASE_MAX_CONNECTIONS \
    -e REDIS_URL \
    -e AMQP_URL \
    -e SECRET_KEY \
    -e SENTRY_DSN \
    -e USVF_SYNC \
    -e USVF_SYNC_HOUR \
    -e ACTIONNETWORK_SYNC \
    -e ACTIONNETWORK_SYNC_DAILY \
    -e ACTIONNETWORK_SYNC_HOUR \
    -e OVBM_SYNC \
    -e UPTIME_ENABLED \
    -e FILE_PURGE_DAYS \
    -e STATE_TOOL_REDIRECT_SYNC \
    -e TARGETSMART_KEY \
    -e ALLOWED_HOSTS \
    -e MULTIFACTOR_ISSUER \
    -e ATTACHMENT_USE_S3 \
    -e AWS_STORAGE_BUCKET_NAME \
    -e AWS_STORAGE_PRIVATE_BUCKET_NAME \
    -e SENDGRID_API_KEY \
    -e FILE_TOKEN_RESET_URL \
    -e PRIMARY_ORIGIN \
    -e WWW_ORIGIN \
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
    -e SMS_OPTOUT_NUMBER \
    -e SMS_OPTOUT_POLL \
    -e MULTIFACTOR_ENABLED \
    -e TWO_FACTOR_SMS_NUMBER \
    -e GEOCODIO_KEY \
    -e FAX_DISABLE \
    -e FAX_OVERRIDE_DEST \
    -e FAX_GATEWAY_CALLBACK_URL \
    -e FAX_GATEWAY_SQS_QUEUE \
    -e SLACK_DATA_ERROR_ENABLED \
    -e SLACK_DATA_ERROR_WEBHOOK \
    -e USVF_GEOCODE \
    -e DD_API_KEY \
    -e REGISTER_CO_VRD_ID \
    -e REGISTER_CO_VRD_ENABLED \
    -e REGISTER_WA_VRD_ID \
    -e REGISTER_WA_VRD_ENABLED \
    -e ACTIONNETWORK_KEY \
    -e OPTIMIZELY_SDK_KEY \
    -e SLACK_SUBSCRIBER_INTEREST_ENABLED \
    -e SLACK_SUBSCRIBER_INTEREST_WEBHOOK \
    -e API_KEY_PEPPER \
    -e DIGITALOCEAN_KEY \
    -e UPTIME_TWITTER_CONSUMER_KEY \
    -e UPTIME_TWITTER_CONSUMER_SECRET \
    -e UPTIME_TWITTER_ACCESS_TOKEN \
    -e UPTIME_TWITTER_ACCESS_TOKEN_SECRET \
    -e SLACK_UPTIME_WEBHOOK \
    -e PROXY_SSH_KEY \
    -e PROXY_SSH_PUB \
    -e PROXY_SSH_KEY_ID \
    -e PROXY_TAG \
    -e SELENIUM_URL \
    -e REGISTER_RESUME_URL \
    -e FILE_TOKEN_PURGED_URL \
    -e PDF_GENERATION_LAMBDA_ENABLED \
    -e PDF_GENERATION_LAMBDA_FUNCTION \
    -e LOB_KEY \
    -e LOB_LETTER_WEBHOOK_SECRET \
    -e RETURN_ADDRESS \
    -e BEAT_STATS_METRIC_NAMESPACE \
    -e I90_KEY \
    -e MOVER_ID \
    -e MOVER_SECRET \
    -e MOVER_SOURCE \
    -e MOVER_LEADS_ENDPOINT \
    -e SLACK_ALLOY_UPDATE_ENABLED \
    -e SLACK_ALLOY_UPDATE_WEBHOOK \
    -e MAPBOX_KEY \
    -e MMS_ATTACHMENT_BUCKET \
    -e CIVIC_KEY \
-e DEBUG=$DEBUG \
-p 8000:8000 \
$IMAGE \
/bin/bash -c "$2"
else
  docker run -i -t \
    -e DATABASE_URL \
    -e READONLY_DATABASE_URL \
    -e DATABASE_MAX_CONNECTIONS \
    -e REDIS_URL \
    -e AMQP_URL \
    -e SECRET_KEY \
    -e SENTRY_DSN \
    -e USVF_SYNC \
    -e USVF_SYNC_HOUR \
    -e ACTIONNETWORK_SYNC \
    -e ACTIONNETWORK_SYNC_DAILY \
    -e ACTIONNETWORK_SYNC_HOUR \
    -e OVBM_SYNC \
    -e UPTIME_ENABLED \
    -e FILE_PURGE_DAYS \
    -e STATE_TOOL_REDIRECT_SYNC \
    -e TARGETSMART_KEY \
    -e ALLOWED_HOSTS \
    -e MULTIFACTOR_ISSUER \
    -e ATTACHMENT_USE_S3 \
    -e AWS_STORAGE_BUCKET_NAME \
    -e AWS_STORAGE_PRIVATE_BUCKET_NAME \
    -e SENDGRID_API_KEY \
    -e FILE_TOKEN_RESET_URL \
    -e PRIMARY_ORIGIN \
    -e WWW_ORIGIN \
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
    -e SMS_OPTOUT_NUMBER \
    -e SMS_OPTOUT_POLL \
    -e MULTIFACTOR_ENABLED \
    -e TWO_FACTOR_SMS_NUMBER \
    -e GEOCODIO_KEY \
    -e FAX_DISABLE \
    -e FAX_OVERRIDE_DEST \
    -e FAX_GATEWAY_CALLBACK_URL \
    -e FAX_GATEWAY_SQS_QUEUE \
    -e SLACK_DATA_ERROR_ENABLED \
    -e SLACK_DATA_ERROR_WEBHOOK \
    -e USVF_GEOCODE \
    -e DD_API_KEY \
    -e REGISTER_CO_VRD_ID \
    -e REGISTER_CO_VRD_ENABLED \
    -e REGISTER_WA_VRD_ID \
    -e REGISTER_WA_VRD_ENABLED \
    -e ACTIONNETWORK_KEY \
    -e OPTIMIZELY_SDK_KEY \
    -e SLACK_SUBSCRIBER_INTEREST_ENABLED \
    -e SLACK_SUBSCRIBER_INTEREST_WEBHOOK \
    -e API_KEY_PEPPER \
    -e DIGITALOCEAN_KEY \
    -e UPTIME_TWITTER_CONSUMER_KEY \
    -e UPTIME_TWITTER_CONSUMER_SECRET \
    -e UPTIME_TWITTER_ACCESS_TOKEN \
    -e UPTIME_TWITTER_ACCESS_TOKEN_SECRET \
    -e SLACK_UPTIME_WEBHOOK \
    -e PROXY_SSH_KEY \
    -e PROXY_SSH_PUB \
    -e PROXY_SSH_KEY_ID \
    -e PROXY_TAG \
    -e SELENIUM_URL \
    -e REGISTER_RESUME_URL \
    -e FILE_TOKEN_PURGED_URL \
    -e PDF_GENERATION_LAMBDA_ENABLED \
    -e PDF_GENERATION_LAMBDA_FUNCTION \
    -e LOB_KEY \
    -e LOB_LETTER_WEBHOOK_SECRET \
    -e RETURN_ADDRESS \
    -e BEAT_STATS_METRIC_NAMESPACE \
    -e I90_KEY \
    -e MOVER_ID \
    -e MOVER_SECRET \
    -e MOVER_SOURCE \
    -e MOVER_LEADS_ENDPOINT \
    -e SLACK_ALLOY_UPDATE_ENABLED \
    -e SLACK_ALLOY_UPDATE_WEBHOOK \
    -e MAPBOX_KEY \
    -e MMS_ATTACHMENT_BUCKET \
    -e CIVIC_KEY \
-e DEBUG=$DEBUG \
-p 8000:8000 \
$IMAGE \
/bin/bash
fi

