#!/bin/sh

iaas="mock"
script_path=""
if [ "$(uname)" == "Darwin" ]; then
    script_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    script_path="$( cd -P "$( dirname "$SOURCE" )" && pwd )/`dirname $0`"
else
   echo "Unknown operating system"
   exit
fi
common_folder="${script_path}/../common"

bash ${common_folder}/deploy.sh ${iaas}
