#!/bin/bash
export QQ=2537838237
export COOLQ_DIR=/data/minghao/coolq
export VNC_PORT=9000
export CQHTTP_PORT=5700
docker run -ti -d --name cqhttp-test -v ${COOLQ_DIR}:/home/user/coolq -p ${VNC_PORT}:${VNC_PORT} -p ${CQHTTP_PORT}:${CQHTTP_PORT} -e COOLQ_ACCOUNT=${QQ} richardchien/cqhttp:latest