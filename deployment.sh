#!/usr/bin/env bash
printf "\nDeployment started\n"

git pull origin dev

cd ./agony/

# Creates agony's infrastructural folders
DIR="${PWD}/static"
[[ ! -d ${DIR} ]] && mkdir -p ${DIR}
DIR="${PWD}/logs"
[[ ! -d ${DIR} ]] && mkdir -p ${DIR}
touch "${PWD}/logs/access.log"

# Loads agony's dependencies
if [[ ! -d "${PWD}/venv" ]]; then
    pip install --upgrade pip
    pip install virtualenv
    virtualenv venv
fi
pip install -r requirements.txt
source ./venv/bin/activate

deactivate
cd ../reapy/

# Creates reapy's infrastructural folders
DIR="${PWD}/logs"
[[ ! -d ${DIR} ]] && mkdir -p ${DIR}
DIR="${PWD}/scribbles"
[[ ! -d ${DIR} ]] && mkdir -p ${DIR}

cd ../

printf "Deployment finished\n\n"
