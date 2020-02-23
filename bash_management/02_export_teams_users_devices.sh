#!/usr/bin/env bash

if [ "$CC_TOKEN" == "" ]
then
  echo 'Please set CC_TOKEN, CC_HOST and CC_DIR environment values or use settings.sh file:'
  echo '$ source ./settings.sh'
  exit
fi

echo 'Please extract "token" from below JSON file and set in CC_TOKEN environment variable:'

for MODEL in "team" "user" "device"
do
  FN="${CC_DIR}${MODEL}_mapping.json"
  echo "Importing: $MODEL from file: $FN ..."
  curl --header "Content-Type: application/json" \
    --header "Authorization: Token $CC_TOKEN" \
    --request POST \
    --data @"$FN" \
    "${CC_HOST}api/import/${MODEL}s/"
  echo
  echo
done
