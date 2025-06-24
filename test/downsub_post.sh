#!/bin/bash

# Kullanım: ./downsub_request.sh <API_URL> <api-type: local|remote>

API_URL="$1"
API_TYPE="$2"

# Gömülü sabit değerler
# URL="https://www.youtube.com/watch?v=XTsaZWzVJ4c&t=1s"
URL="https://www.youtube.com/watch?v=va3kJ1YBBXo"
SUB_LANG="en"

# Kontroller
if [ -z "$API_URL" ] || [ -z "$API_TYPE" ]; then
  echo "Kullanım: $0 <API_URL> <api-type: local|remote>"
  exit 1
fi

if [ "$API_TYPE" != "local" ] && [ "$API_TYPE" != "remote" ]; then
  echo "Hatalı api-type: '$API_TYPE'. Sadece 'local' veya 'remote' olabilir."
  exit 1
fi

echo "İstek gönderiliyor:"
echo "API URL   : $API_URL"
echo "API Tipi  : $API_TYPE"
echo "Video URL : $URL"
echo "Dil Kodu  : $SUB_LANG"

# İstek gönder
curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "x-service: downsub-api" \
  -d "{\"url\": \"$URL\", \"sub_lang\": \"$SUB_LANG\"}"

