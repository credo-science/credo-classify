#!/usr/bin/env bash

if [ "$CC_TOKEN" == "" ]
then
  echo 'Please set CC_TOKEN and CC_HOST environment values or use settings.sh file:'
  echo '$ source ./settings.sh'
  exit
fi

for FN in "$@"
do
  echo "Importing: pings from file: $FN ..."
  time curl --header "Content-Type: application/json" \
    --header "Authorization: Token $CC_TOKEN" \
    --request POST \
    --data @"$FN" \
    "${CC_HOST}api/import/pings/?nocheck=1"
  echo
  echo
done
