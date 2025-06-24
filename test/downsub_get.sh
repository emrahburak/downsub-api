#!/bin/bash

# Kullanım: ./downsub_get.sh <api-url> <task_id> 

API_URL_BASE="$1"
TASK_ID="$2"

if [ -z "$API_URL_BASE" ] || [ -z "$TASK_ID" ]  ; then
  echo "Kullanım: $0 <api-url>  <task-id>"
  exit 1
fi


FULL_URL="${API_URL_BASE}/downsub/result/${TASK_ID}"

echo "İstek gönderiliyor:"
echo "API URL   : $FULL_URL"
echo "Task ID   : $TASK_ID"

curl -X GET -H "X-Service: downsub-api" -OJ "$FULL_URL"

