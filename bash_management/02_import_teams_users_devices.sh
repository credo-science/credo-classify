#!/usr/bin/env bash

if [ "$CC_TOKEN" == "" ]
then
  echo 'Please set CC_TOKEN, CC_HOST and CC_DIR environment values or use settings.sh file:'
  echo '$ source ./settings.sh'
  exit
fi

for MODEL in "team" "user" "device"
do
  FN="${CC_DIR}${MODEL}_mapping.json"
  echo "Importing: $MODEL from file: $FN ..."
  time curl --header "Content-Type: application/json" \
    --header "Authorization: Token $CC_TOKEN" \
    --request POST \
    --data @"$FN" \
    "${CC_HOST}api/import/${MODEL}s/?nocheck=1"
  echo
  echo
done
