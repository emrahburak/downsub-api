#!/bin/bash

# Kullanım: ./downsub_get.sh <task_id> <api=local|remote>

TASK_ID="$1"
API_TARGET="$2"

if [ -z "$TASK_ID" ] || [ -z "$API_TARGET" ]; then
  echo "Kullanım: $0 <task_id> <api=local|remote>"
  exit 1
fi

if [ "$API_TARGET" == "local" ]; then
  API_URL="http://localhost:8080/downsub/result/$TASK_ID"
elif [ "$API_TARGET" == "remote" ]; then
  API_URL="https://api.omnistart.me/downsub/result/$TASK_ID"
else
  echo "Hatalı API hedefi: '$API_TARGET'. Sadece 'local' veya 'remote' kabul edilir."
  exit 1
fi

curl -X GET -H "X-Service: downsub-api" -OJ "$API_URL"

