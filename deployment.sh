#!/usr/bin/env bash
echo "Deployment started"

# Exit the script if the previous command failed
check () {
    STATUS=$?
    if [[ ${STATUS} != 0 ]]; then
        echo ${1}
        exit ${STATUS}
    fi
}

# Pull updates
echo ""
git pull origin master
check "Failed to pull the updates"

# Creates the target directory if it's absent
mkdir_if_absent () {
    DIR="${PWD}/${1}"
    [[ ! -d ${DIR} ]] && mkdir -p ${DIR}
}

# Create agony's infrastructural folders & files
cd ./agony/
mkdir_if_absent ".yamjam"
mkdir_if_absent "static"
mkdir_if_absent "logs"
touch "${PWD}/logs/access.log"

# Load all required python packages
load_dependencies () {
    if [[ ! -d "${PWD}/venv" ]]; then
        echo ""
        sudo pip install --upgrade pip
        sudo pip install virtualenv
        virtualenv venv
    fi
    source ./venv/bin/activate
    echo ""
    pip install -r requirements.txt
    check "Dependencies' loading failed"
}

# Load agony's dependencies
load_dependencies

# Create yamjam config if absent and lint it
lint_yamjam () {
    CONFIG="${PWD}/.yamjam/config.yaml"
    if [[ ! -f ${CONFIG} ]]; then
        cp "./config-template.yaml" ${CONFIG}
        nano ${CONFIG}
    fi
    echo ""
    yjlint ${CONFIG}
    check "Configuration linting failed"
}

# Lint agony's secrets
lint_yamjam

# Migrate the databases
echo ""
echo "Default database is being migrated..."
./manage.py migrate
check "Default database migration failed"
echo "Testing database is being migrated..."
./manage.py migrate --database=testing
check "Testing database migration failed"

# Test the API
echo ""
./manage.py test
check "Direct API tests failed"
echo ""
./manage.py test --reverse
check "Reverse API tests failed"

# Collect static files
echo ""
./manage.py collectstatic
check "Static files weren't collected"

# Finalize agony's deployment
deactivate
cd ../
echo ""
echo "Gunicorn & nginx are being restarted..."
sudo systemctl restart gunicorn
check "Gunicorn wasn't restarted"
sudo systemctl restart nginx
check "Nginx wasn't restarted"

# Create reapy's infrastructural folders
cd ./reapy/
mkdir_if_absent ".yamjam"
mkdir_if_absent "logs"
mkdir_if_absent "scribbles"

# Load reapy's dependencies
load_dependencies

# Lint reapy's secrets
lint_yamjam

# Test reapy
echo ""
pytest -q -x --timeout=5 ./tests/
check "Pytest failed"

# Write cron jobs
./schedule.py
check "Cron schedule failed"
deactivate
cd ../

echo ""
echo "Deployment finished"
echo ""
