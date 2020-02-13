#!/usr/bin/env bash

# Return Codes:
#   1 - Unable to produce distributions
#   2 - Twine was unable to run or threw an error
#   3 - A distribution failed the twine check
#   4 - Pip failed to install the distribution
#   5 - Unable to set version string

python="/usr/bin/env python3"
uname=$(uname)




function build () {
    printf "Starting the build process\n"
    # build new distributions
    $python setup.py sdist bdist_wheel
    ec=$?
    if [ $ec -ne 0 ]; then
        printf "Setup.py was unable to build the distributions with exit code ${ec}. Exiting!\n"
        exit 1
    fi
}

# test the distributions with twine
function check_dist () {
    printf "Checking the produced distributions\n"
    $python -m twine check dist/*
    ec=$?
    if [ $ec -ne 0 ]; then 
        printf "Twine exited with code ${ec}. Build Failed!\n"
        exit 2
    fi
}

function getver () {
    if [ "${uname}" = "Darwin" ]; then 
        version=$(egrep -oe 'version="(\d+\.\d+\.\d+)"' setup.py | egrep -oe '\d+\.\d+\.\d+')
    elif [ "${uname}" = "Linux" ]; then
        version=$(grep setup.py -Poe '(?<=version=")(\d+\.\d+\.\d+)(?=",)')
    else
        printf "Unexpected OS. Unable to parse version string from setup.py. Build Failed!\n"
        exit 5
    fi

    if [ -z $version ]; then
        printf "Unable to parse version string. Build Failed!\n"
        exit 5
    fi
    export $version
}

function install () {
    printf "Installing the distribution version: ${version}\n"
    # install the produced archive
    $python -m pip install "./dist/reme-${version}.tar.gz"
    ec=$?
    if [ $ec -ne 0 ]; then
        printf "Pip failed to install the distribution with exit code ${ec}. Build Failed!\n"
        exit 4
    fi
}

# Delete any existing distributions
if [ -d ./dist ]; then
    rm -rfv ./dist/*
fi

getver
printf "Reme Version: ${version}\n"
# build the distributions
build
# test the distributions
check_dist
# install the produced archive
install 