#!/bin/bash
set -e

APP_DIR="$(pwd)"

# Setup CF CLI
if [ ! -f "$APP_DIR/cf" ]; then
  echo -e "Downloading/unpackingting Cloud Foundry CLI"
  curl -L 'https://cli.run.pivotal.io/stable?release=linux64-binary&source=github' | tar -zx &&
  echo -e "Installing collected packages: Cloud Foundry CLI"
  echo -e "\033[32mSuccessfully \033[0minstalled Cloud Foundry CLI\n"
fi

# Setup CF for abacus helper
CF_API_DEFAULT=$($APP_DIR/cf target |  awk '{if (NR == 1) {print $3}}')
CF_USER_DEFAULT=$($APP_DIR/cf target |  awk '{if (NR == 3) {print $2}}')
CF_ORG_DEFAULT=$($APP_DIR/cf target | awk '{if (NR == 4) {print $2}}')
CF_SPACE_DEFAULT=$($APP_DIR/cf target | awk '{if (NR == 5) {print $2}}')

read -p "Enter your API URL [$CF_API_DEFAULT]: " CF_API
CF_API="${CF_API:-$CF_API_DEFAULT}"
if [[ -z $CF_API ]]; then
  echo 'Missing API URL! Did you login?'
  exit 1
fi

read -p "Enter your user name [$CF_USER_DEFAULT]: " CF_USER
CF_USER="${CF_USER:-$CF_USER_DEFAULT}"
if [[ -z $CF_USER ]]; then
  echo 'Missing user name! Did you login?'
  exit 1
fi

read -p "Enter your organization [$CF_ORG_DEFAULT]: " CF_ORG
CF_ORG="${CF_ORG:-$CF_ORG_DEFAULT}"
if [[ -z $CF_ORG ]]; then
  echo 'Missing organization; Did you target an org?'
  exit 1
fi

read -p "Enter your space [$CF_SPACE_DEFAULT]: " CF_SPACE
CF_SPACE="${CF_SPACE:-$CF_SPACE_DEFAULT}"
if [[ -z $CF_SPACE ]]; then
  echo 'Missing space! Did you target a space?'
  exit 1
fi

read -p "Enter your password: " CF_PASSWORD
CF_PASSWORD="$CF_PASSWORD"
if [[ -z $CF_PASSWORD ]]; then
  echo 'Missing password!?'
  exit 1
fi

# Point the CF CLI to your local Cloud Foundry deployment
$APP_DIR/cf login --skip-ssl-validation -a $CF_API -u $CF_USER -p $CF_PASSWORD -o $CF_ORG -s $CF_SPACE

# Generate manifest
if [ $? -eq 0 ]; then
  echo -e "\033[32mSuccessfully \033[0mlogged in Cloud Foundry\n"
  echo -e "Generating abacus-helper manifest"
  sed "s|CF_API_ENDPOINT:|& $CF_API|" manifest-stub.yml > manifest.yml
  sed -i "s|CF_USER:|& $CF_USER|" manifest.yml
  sed -i "s|CF_PASSWORD:|& $CF_PASSWORD|" manifest.yml
fi
echo -e "\033[32mSuccessfully \033[0memitted manifest.yml\n"
