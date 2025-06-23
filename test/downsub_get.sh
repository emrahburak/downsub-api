#!/bin/bash

# Kullanım: ./downsub_get.sh <task_id> <api-type: local|remote> <api-url>

TASK_ID="$1"
API_TYPE="$2"
API_URL_BASE="$3"

if [ -z "$TASK_ID" ] || [ -z "$API_TYPE" ] || [ -z "$API_URL_BASE" ]; then
  echo "Kullanım: $0 <task_id> <api-type: local|remote> <api-url>"
  exit 1
fi

if [ "$API_TYPE" != "local" ] && [ "$API_TYPE" != "remote" ]; then
  echo "Hatalı api-type: '$API_TYPE'. Sadece 'local' veya 'remote' olabilir."
  exit 1
fi

FULL_URL="${API_URL_BASE}/downsub/result/${TASK_ID}"

echo "İstek gönderiliyor:"
echo "API URL   : $FULL_URL"
echo "API Tipi  : $API_TYPE"
echo "Task ID   : $TASK_ID"

curl -X GET -H "X-Service: downsub-api" -OJ "$FULL_URL"

