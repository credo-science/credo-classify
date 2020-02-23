#!/usr/bin/env bash

if [ "$CC_USER" == "" ]
then
  echo 'Please set CC_USER, CC_PASS and CC_HOST environment values or use settings.sh file:'
  echo '$ source ./settings.sh'
  exit
fi

echo 'Please extract "token" from below JSON file and set in CC_TOKEN environment variable:'

curl --header "Content-Type: application/json" \
  --request POST \
  --data "{\"username\":\"$CC_USER\",\"password\":\"$CC_PASS\"}" \
  "${CC_HOST}api-token-auth/"

echo
