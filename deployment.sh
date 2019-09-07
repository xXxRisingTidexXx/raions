#!/usr/bin/env bash
printf "\nDeployment started\n"

git pull origin dev

# Edit YamJam config

# Create agony's infrastructural folders
cd ./agony/
DIR="${PWD}/static"
[[ ! -d ${DIR} ]] && mkdir -p ${DIR}
DIR="${PWD}/logs"
[[ ! -d ${DIR} ]] && mkdir -p ${DIR}
touch "${PWD}/logs/access.log"

# Load agony's dependencies
if [[ ! -d "${PWD}/venv" ]]; then
    pip install --upgrade pip
    pip install virtualenv
    virtualenv venv
fi
pip install -r requirements.txt
STATUS=$?;
if [[ ${STATUS} != 0 ]]; then
    exit ${STATUS};
fi
source ./venv/bin/activate

# Migrate the databases

# Test the API
./manage.py test
./manage.py test --reverse

# Collect static files

# Finalize agony's configuration

deactivate

# Create reapy's infrastructural folders
cd ../reapy/
DIR="${PWD}/logs"
[[ ! -d ${DIR} ]] && mkdir -p ${DIR}
DIR="${PWD}/scribbles"
[[ ! -d ${DIR} ]] && mkdir -p ${DIR}
cd ../

printf "Deployment finished\n\n"
