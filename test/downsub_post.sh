#!/bin/bash

# Kullanım: ./downsub_request.sh <YouTube_URL> <Subtitle_Language_Code> <api=local|remote>

URL="$1"
SUB_LANG="$2"
API_TARGET="$3"

if [ -z "$URL" ] || [ -z "$SUB_LANG" ] || [ -z "$API_TARGET" ]; then
  echo "Kullanım: $0 <YouTube_URL> <Subtitle_Language_Code> <api=local|remote>"
  exit 1
fi

if [ "$API_TARGET" == "local" ]; then
  API_URL="http://localhost:8080/downsub"
elif [ "$API_TARGET" == "remote" ]; then
  API_URL="https://api.omnistart.me/downsub"
else
  echo "Hatalı API hedefi: '$API_TARGET'. Sadece 'local' veya 'remote' kabul edilir."
  exit 1
fi

curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "x-service: downsub-api" \
  -d "{\"url\": \"$URL\", \"sub_lang\": \"$SUB_LANG\"}"

