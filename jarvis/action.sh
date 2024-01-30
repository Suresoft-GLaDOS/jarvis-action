#!/bin/bash

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
echo "export TOKEN=$TOKEN; git clone https://$TOKEN@github.com/$GITHUB_REPOSITORY.git" > $GITHUB_ACTION_PATH/token.sh

echo "[DEBUG] OPENAI_PATH: $OPENAI_PATH"
echo "TARGET_REPO_NAME: $TARGET_REPO_NAME"

echo JARVIS_TARGET=$JARVIS_WORKSPACE/$TARGET_REPO_NAME
export JARVIS_TARGET=$JARVIS_WORKSPACE/$TARGET_REPO_NAME
echo "JARVIS_TARGET: $JARVIS_TARGET"

docker build -t ubuntu20.04_cppcheck $GITHUB_ACTION_PATH
docker run -d --name jarvis_cppcheck-ubuntu20.04 -u jarvis:jarvis -i ubuntu20.04_cppcheck

retval=$?
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval"
    docker start jarvis-ubuntu20.04_cppcheck
fi
echo "Run docker test"

docker exec -iu 0 jarvis_cppcheck-ubuntu20.04 sh -c 'echo $ACTION_CALL'

docker exec -iu 0 jarvis_cppcheck-ubuntu20.04 sh -c "mkdir openai"
docker exec -iu 0 jarvis_cppcheck-ubuntu20.04 sh -c "mkdir scripts"
retval=$?
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval"
fi
echo "mkdir test"

docker cp "$OPENAI_PATH" jarvis_cppcheck-ubuntu20.04:$JARVIS_WORKSPACE/openai/
docker cp "$GITHUB_ACTION_PATH/token.sh" jarvis_cppcheck-ubuntu20.04:$JARVIS_WORKSPACE/
docker cp "$GITHUB_ACTION_PATH/token.txt" jarvis_cppcheck-ubuntu20.04:$JARVIS_WORKSPACE/ 
docker cp "$GITHUB_ACTION_PATH/jarvis/git/" jarvis_cppcheck-ubuntu20.04:$JARVIS_WORKSPACE/scripts/
docker cp "$GITHUB_WORKSPACE" jarvis_cppcheck-ubuntu20.04:$JARVIS_WORKSPACE/
echo $ACTION_CALL

retval=$?
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval" 
fi

echo "cp test"

docker exec -iu 0 jarvis_cppcheck-ubuntu20.04 sh -c "ln -s /clang_14/lib/libclang.so /clang_14/lib/libclang-14.so"

docker exec -iu 0 jarvis_cppcheck-ubuntu20.04 sh -c "git clone http://10.10.10.75:3000/kyham/JARVIS"

echo "JARVIS clone"

docker exec -iu 0 jarvis_cppcheck-ubuntu20.04 bash -c "$JARVIS_WORKSPACE/token.sh"

docker exec -iu 0 jarvis_cppcheck-ubuntu20.04 sh -c "cd JARVIS; git checkout cppcheck; git pull"

docker exec -iu 0 jarvis_cppcheck-ubuntu20.04 sh -c "pip install -r $JARVIS_WORKSPACE/JARVIS/requirements.txt;\
                                            export JARVIS_WORKSPACE=$JARVIS_WORKSPACE; \
                                            export JARVIS_TARGET=$JARVIS_TARGET; \
                                            export CHECKER=CPPCHECK; \
                                            python3 $JARVIS_WORKSPACE/JARVIS/main.py"

retval=$?
# do_something $retval
if [ $retval -ne 0 ]; then
    echo "Return code was not zero but $retval"
fi

docker exec -iu 0 jarvis_cppcheck-ubuntu20.04 bash -c "export JARVIS_WORKSPACE=$JARVIS_WORKSPACE; \
                                            export TARGET_REPO_NAME=$TARGET_REPO_NAME;\
                                            $JARVIS_WORKSPACE/scripts/git/diff_gen.sh"

docker exec -iu 0 jarvis_cppcheck-ubuntu20.04 bash -c "export JARVIS_WORKSPACE=$JARVIS_WORKSPACE; \
                                            export JARVIS_TARGET=$JARVIS_TARGET; \
                                            export GITHUB_SHA=$GITHUB_SHA; \
                                            export GITHUB_REF_NAME=$GITHUB_REF_NAME; \
                                            export GITHUB_REPOSITORY=$GITHUB_REPOSITORY; \
                                            export TARGET_REPO_NAME=$TARGET_REPO_NAME;\
                                            $JARVIS_WORKSPACE/scripts/git/auth_and_create.sh"

docker cp jarvis_cppcheck-ubuntu20.04:$JARVIS_WORKSPACE/JARVIS/workspace/outputs/fix_violation.patch $GITHUB_ACTION_PATH/jarvis/temp/    
docker cp jarvis_cppcheck-ubuntu20.04:$JARVIS_WORKSPACE/JARVIS/workspace/outputs/ $GITHUB_ACTION_PATH/jarvis/temp/       

# python3 -m pip install --upgrade pip
# pip install gitpython

cd $GITHUB_WORKSPACE
echo $GITHUB_WORKSPACE

# python3 $GITHUB_ACTION_PATH/jarvis/git/create-pull-request-local.py                                            

echo "python3 test"

# docker rm -f jarvis-ubuntu20.04 



# source $GITHUB_ACTION_PATH/jarvis/git/config.sh
# source $GITHUB_ACTION_PATH/jarvis/git/checkout.sh
# source $GITHUB_ACTION_PATH/jarvis/git/auth.sh

# python3 $GITHUB_ACTION_PATH/jarvis/runner/runner.py
