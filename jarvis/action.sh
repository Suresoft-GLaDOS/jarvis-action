#!/bin/bash

# python3 "$GITHUB_ACTION_PATH"/jarvis/setenv.py

sh $GITHUB_ACTION_PATH/jarvis/env_sn/setenv.sh
sh $GITHUB_ACTION_PATH/jarvis/env_sn/setenv_yml.sh

echo "[DEBUG] GITHUB_ACTION_PATH: $GITHUB_ACTION_PATH"
echo "[DEBUG] JARVIS_WORKSPACE: $JARVIS_WORKSPACE"
echo "[DEBUG] GITHUB_TOKEN: $TOKEN"

docker build -t ubuntu20.04 .

docker run -d --name jarvis-ubuntu20.04 -u jarvis:jarvis -it ubuntu20.04

retval=$?
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval"
fi
echo "Run docker test"


docker exec -itu 0 jarvis-ubuntu20.04 sh -c "mkdir tbeg"
docker exec -itu 0 jarvis-ubuntu20.04 sh -c "mkdir openai"
docker exec -itu 0 jarvis-ubuntu20.04 sh -s "mkdir scripts"
retval=$?
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval"
fi
echo "mkdir test"


docker cp "$CSBUILD_PATH" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/tbeg/
docker cp "$OPENAI_PATH" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/openai/
docker cp "$GITHUB_ACTION_PATH/jarvis/env_sn/git_config.sh" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/scripts/

docker exec -itu 0 jarvis-ubuntu20.04 sh -c "$JARVIS_WORKSPACE/scripts/git_config.sh"
docker exec -itu 0 jarvis-ubuntu20.04 sh -c "$JARVIS_WORKSPACE/scripts/setenv_docker.sh"

retval=$?
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval" 
fi

echo "cp test"

docker exec -itu 0 jarvis-ubuntu20.04 sh -c "git clone http://10.10.10.75:3000/kyham/JARVIS"

echo "JARVIS clone"

docker exec -itu 0 jarvis-ubuntu20.04 sh -c "python3 "$WORKSPACE"/JARVIS/main.py"

retval=$?
# do_something $retval
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval"
fi

echo "python3 test"

# docker exec -itu 0 jarvis-ubuntu20.04 sh -c "sh /home/exec_test/docker_scripts/setenv.sh"

# retval=$?
# # do_something $retval
# if [ $retval -ne 0 ]; then
#     echo "Return code was not zero but $retval"
# fi

# echo "sh test"



# source $GITHUB_ACTION_PATH/jarvis/git/config.sh
# source $GITHUB_ACTION_PATH/jarvis/git/checkout.sh
# source $GITHUB_ACTION_PATH/jarvis/git/auth.sh

# python3 $GITHUB_ACTION_PATH/jarvis/runner/runner.py
