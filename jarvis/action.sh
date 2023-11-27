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
echo $GITHUB_ACTION_PATH/token.txt
echo $TOKEN > $GITHUB_ACTION_PATH/token.txt

echo "[DEBUG] CSBUILD_PATH: $CSBUILD_PATH"
echo "[DEBUG] OPENAI_PATH: $OPENAI_PATH"

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
docker cp "$OPENAI_PATH" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/openai/
docker cp "$GITHUB_ACTION_PATH/token.txt" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/ 
docker cp "$CSBUILD_PATH/repo_token.txt" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/ 
docker cp "$GITHUB_ACTION_PATH/jarvis/env_sh/git_config.sh" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/scripts/
docker cp "$GITHUB_ACTION_PATH/jarvis/env_sh/setenv_docker.sh" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/scripts/
docker cp "$GITHUB_ACTION_PATH/jarvis/git/" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/scripts/
docker cp "$GITHUB_WORKSPACE" jarvis-ubuntu20.04:$JARVIS_WORKSPACE/

docker exec -iu 0 jarvis-ubuntu20.04 sh -c "cd $JARVIS_WORKSPACE; git add .; git commit -m 'newline'"

export CSBUILD_DOCKER="$JARVIS_WORKSPACE/tbeg/apps/csbuild-ubuntu-20.04_v1.2.0/bin"

docker exec -iu 0 jarvis-ubuntu20.04 sh -c "$JARVIS_WORKSPACE/scripts/setenv_docker.sh"
echo $ACTION_CALL

retval=$?
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval" 
fi

echo "cp test"

docker exec -iu 0 jarvis-ubuntu20.04 sh -c "git clone http://10.10.10.75:3000/kyham/JARVIS"

echo "JARVIS clone"

docker exec -iu 0 jarvis-ubuntu20.04 sh -c "cd JARVIS; git checkout master; git pull"

docker exec -iu 0 jarvis-ubuntu20.04 sh -c "echo '$CSBUILD_USER_OPTION'"

if [ "" == "$CSBUILD_USER_OPTION" ]; then
echo "Do not use csbuild option"
docker exec -iu 0 jarvis-ubuntu20.04 sh -c "pip install -r $JARVIS_WORKSPACE/JARVIS/requirements.txt;\
                                            export JARVIS_WORKSPACE=$JARVIS_WORKSPACE; \
                                            export JARVIS_TARGET=$JARVIS_TARGET; \
                                            python3 $JARVIS_WORKSPACE/JARVIS/main.py"
else
echo "Use csbuild option"
docker exec -iu 0 jarvis-ubuntu20.04 sh -c "pip install -r $JARVIS_WORKSPACE/JARVIS/requirements.txt;\
                                            export JARVIS_WORKSPACE=$JARVIS_WORKSPACE; \
                                            export JARVIS_TARGET=$JARVIS_TARGET; \
                                            export CSBUILD_USER_OPTION='$CSBUILD_USER_OPTION'; \
                                            python3 $JARVIS_WORKSPACE/JARVIS/main.py"
fi                                            


retval=$?
# do_something $retval
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval"
fi

docker exec -iu 0 jarvis-ubuntu20.04 bash -c "export JARVIS_WORKSPACE=$JARVIS_WORKSPACE; \
                                            export TARGET_REPO_NAME=$TARGET_REPO_NAME;\
                                            $JARVIS_WORKSPACE/scripts/git/diff_gen.sh"

docker exec -iu 0 jarvis-ubuntu20.04 bash -c "export JARVIS_WORKSPACE=$JARVIS_WORKSPACE; \
                                            export JARVIS_TARGET=$JARVIS_TARGET; \
                                            export GITHUB_SHA=$GITHUB_SHA; \
                                            export GITHUB_REF_NAME=$GITHUB_REF_NAME; \
                                            export GITHUB_REPOSITORY=$GITHUB_REPOSITORY; \
                                            export TARGET_REPO_NAME=$TARGET_REPO_NAME;\
                                            $JARVIS_WORKSPACE/scripts/git/auth_and_create.sh"

docker cp jarvis-ubuntu20.04:$JARVIS_WORKSPACE/JARVIS/workspace/outputs/fix_violation.patch $GITHUB_ACTION_PATH/jarvis/temp/    
docker cp jarvis-ubuntu20.04:$JARVIS_WORKSPACE/JARVIS/workspace/outputs/ $GITHUB_ACTION_PATH/jarvis/temp/       

python3 -m pip install --upgrade pip
pip install gitpython

cd $GITHUB_WORKSPACE
python3 $GITHUB_ACTION_PATH/jarvis/git/create-pull-request-local.py                                            

echo "python3 test"

# docker rm -f jarvis-ubuntu20.04 

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
