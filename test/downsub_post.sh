#!/bin/bash

# Kullanım: ./downsub_post.sh <API_URL> <YOUTUBE_URL> <SUB_LANG>

API_URL="$1"
VIDEO_URL="$2"
SUB_LANG="$3"

if [ -z "$API_URL" ] || [ -z "$VIDEO_URL" ] || [ -z "$SUB_LANG" ]; then
  echo "Kullanım: $0 <API_URL> <YOUTUBE_URL> <SUB_LANG>"
  exit 1
fi

FULL_URL="${API_URL}/downsub"

echo "İstek gönderiliyor:"
echo "API URL   : $API_URL"
echo "Video URL : $VIDEO_URL"
echo "Dil Kodu  : $SUB_LANG"

# İstek gönder
curl -X POST "$FULL_URL" \
  -H "Content-Type: application/json" \
  -H "x-service: downsub-api" \
  -d "{\"url\": \"$VIDEO_URL\", \"sub_lang\": \"$SUB_LANG\"}"

