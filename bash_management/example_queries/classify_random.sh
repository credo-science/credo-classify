#!/usr/bin/env bash

if [ "$CC_TOKEN" == "" ]
then
  echo 'Please set CC_TOKEN, CC_HOST and CC_DIR environment values or use settings.sh file:'
  echo '$ source ./settings.sh'
  exit
fi

time curl --header "Content-Type: application/json" \
  --header "Authorization: Token $CC_TOKEN" \
  --request GET \
  "${CC_HOST}api/classify/random/"
echo
echo
