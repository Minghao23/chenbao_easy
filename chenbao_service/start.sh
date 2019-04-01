#!/bin/bash
basepath=$(cd `dirname $0`; pwd)
export PROJECTNAME=chenbao_service
export PROJECTDIR=${basepath}
export PROCESSNAME=${PROJECTDIR}/manage.py
export VENVDIR=${PROJECTDIR}/venv
export PORT=8012

pid=`ps -ef | grep "${PROCESSNAME}" | grep -v "grep" | awk '{print $2}'`
if [[ $pid ]]; then
    echo -e "[\033[31mERROR\033[0m] The ${PROJECTNAME} process is still running and pid=${pid}"
else
    exec ${VENVDIR}/bin/python ${PROJECTDIR}/manage.py runserver 0.0.0.0:${PORT} --noreload > log.file 2>&1 &
    echo -e "[\033[32mOK\033[0m] Succeed to start ${PROJECTNAME}"
fi
