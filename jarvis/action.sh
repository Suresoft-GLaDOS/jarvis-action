#!/bin/bash

# python3 "$GITHUB_ACTION_PATH"/jarvis/setenv.py

echo $GITHUB_ACTION_PATH

source $GITHUB_ACTION_PATH/jarvis/env_sh/setenv.sh
source $GITHUB_ACTION_PATH/jarvis/env_sh/setenv_yml.sh

retval=$?
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval"
fi
echo "Run shell script test"

echo "[DEBUG] GITHUB_ACTION_PATH: $GITHUB_ACTION_PATH"
echo "[DEBUG] JARVIS_WORKSPACE: $JARVIS_WORKSPACE"
echo "[DEBUG] GITHUB_TOKEN: $TOKEN"

export JARVIS_TARGET="$JARVIS_WORKSPACE/$TARGET_REPO_NAME"


docker build -t ubuntu20.04 $GITHUB_ACTION_PATH
docker run -d --name jarvis-ubuntu20.04 -u jarvis:jarvis -i ubuntu20.04


retval=$?
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval"
    docker start jarvis-ubuntu20.04
fi
echo "Run docker test"

docker exec -iu 0 jarvis-ubuntu20.04 sh -c 'echo $ACTION_CALL'

docker exec -iu 0 jarvis-ubuntu20.04 sh -c "mkdir openai"
docker exec -iu 0 jarvis-ubuntu20.04 sh -c "mkdir scripts"
retval=$?
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval"
fi
echo "mkdir test"


docker cp "$CSBUILD_PATH" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/
# docker cp "$OPENAI_PATH" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/openai/
docker cp "/mnt/d/iitp/IITP_JARVIS/openai_key" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/openai/
docker cp "$GITHUB_ACTION_PATH/jarvis/env_sh/git_config.sh" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/scripts/
docker cp "$GITHUB_ACTION_PATH/jarvis/env_sh/setenv_docker.sh" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/scripts/
docker cp "/mnt/d/iitp/IITP_JARVIS/jarvis_workspace/actions-runner/_work/JARVIS_demo/JARVIS_demo" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/

# docker run -d -iu ubuntu20.04:latest bash -s "source $JARVIS_WORKSPACE/scripts/setenv_docker.sh"
export CSBUILD_DOCKER="$JARVIS_WORKSPACE/tbeg/apps/csbuild-ubuntu-20.04_v1.2.0/bin"
# docker exec -iu 0 -e PATH=$JARVIS_WORKSPACE jarvis-ubuntu20.04

docker exec -iu 0 jarvis-ubuntu20.04 "source $JARVIS_WORKSPACE/scripts/git_config.sh"
docker exec -iu 0 jarvis-ubuntu20.04 bash -c "source $JARVIS_WORKSPACE/scripts/setenv_docker.sh"
echo $ACTION_CALL
# docker run -rm jarvis-ubuntu20.04 ". $JARVIS_WORKSPACE/scripts/setenv_docker.sh"


retval=$?
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval" 
fi

echo "cp test"

docker exec -iu 0 jarvis-ubuntu20.04 sh -c "git clone http://10.10.10.75:3000/kyham/JARVIS"

echo "JARVIS clone"

docker exec -iu 0 jarvis-ubuntu20.04 sh -c "cd JARVIS; git checkout action_check; git pull"

docker exec -iu 0 jarvis-ubuntu20.04 sh -c "export JARVIS_WORKSPACE=$JARVIS_WORKSPACE; \
                                            export JARVIS_TARGET=$JARVIS_TARGET; \
                                            python3 "$JARVIS_WORKSPACE"/JARVIS/main.py"

retval=$?
# do_something $retval
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval"
fi

echo "python3 test"

docker rm -f jarvis-ubuntu20.04 

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
