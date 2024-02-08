import os
import datetime
import os
import pprint
import sys
import yaml


os.getenv("JARVIS_WORKSPACE")

if os.getenv("JARVIS_WORKSPACE") != None:
    print("JARVIS_WORKSPACE is not None")
else:
    print("JARVIS_WORKSPACE is None")

JARVIS_WORKSPACE=os.getenv("JARVIS_WORKSPACE") if os.getenv("JARVIS_WORKSPACE") != None else "/home/workspace" # Workspace in docker container. Target repository will be cloned here.
print(JARVIS_WORKSPACE)
WORKSPACE=JARVIS_WORKSPACE

GITHUB_ACTION_PATH = os.getenv("GITHUB_ACTION_PATH", "./")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY") # Repository name action running
GITHUB_REPOSITORY_OWNER = os.getenv("GITHUB_REPOSITORY_OWNER")
GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
GITHUB_SHA=os.getenv("GITHUB_SHA")
GITHUB_REF_NAME=os.getenv("GITHUB_REF_NAME", None)

JARVIS_TARGET = os.path.join(JARVIS_WORKSPACE, GITHUB_REPOSITORY) if GITHUB_REPOSITORY else JARVIS_WORKSPACE
JARVIS_YML_PATH = os.path.join(GITHUB_WORKSPACE, "jarvis.yml")
JARVIS_SUFFIX = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
JARVIS_OUTPUT_DIR = os.path.realpath(os.path.join(JARVIS_WORKSPACE, "..", "..", "output", GITHUB_REPOSITORY, JARVIS_SUFFIX))

TARGET_REPO_NAME=GITHUB_REPOSITORY.replace(f"{GITHUB_REPOSITORY_OWNER}/", "")

# reset some environment variables

os.environ["JARVIS_TARGET"] = JARVIS_TARGET
os.environ["JARVIS_OUTPUT_DIR"] = JARVIS_OUTPUT_DIR


def setenv_writter():
    with open(fr"{GITHUB_ACTION_PATH}/jarvis/env_sh/setenv.sh", "w") as f:
        setenv_data = f"""#!/bin/bash

export GITHUB_ACTION_PATH="{os.getenv("GITHUB_ACTION_PATH", "/")}"
export GITHUB_REPOSITORY="{os.getenv("GITHUB_REPOSITORY")}"
export GITHUB_REPOSITORY_OWNER="{GITHUB_REPOSITORY_OWNER}"
export GITHUB_WORKSPACE="{os.getenv("GITHUB_WORKSPACE")}"
export TARGET_REPO_NAME="{TARGET_REPO_NAME}"

export JARVIS_WORKSPACE="{JARVIS_WORKSPACE}"
export JARVIS_TARGET="{os.path.join(JARVIS_WORKSPACE, GITHUB_REPOSITORY) if GITHUB_REPOSITORY else JARVIS_WORKSPACE}"
export JARVIS_YML_PATH="{os.path.join(JARVIS_TARGET, "jarvis.yml")}"
export JARVIS_OUTPUT_DIR="{os.path.join(JARVIS_WORKSPACE, "output", GITHUB_REPOSITORY, JARVIS_SUFFIX)}"
export TARGET_DIR="{JARVIS_TARGET}"

export GITHUB_SHA="{GITHUB_SHA}"
export GITHUB_REF_NAME="{GITHUB_REF_NAME}"

                        """
        f.write(setenv_data)


def setenv_yml_writter(yml):
    with open(fr"{GITHUB_ACTION_PATH}/jarvis/env_sh/setenv_yml.sh", "w") as f:
        setenv_yml_data = f"""#!/bin/bash

export JARVIS_YML_NAME="{os.getenv("JARVIS_YML_NAME")}"
export JARVIS_YML_DOCKER_IMAGE="{os.getenv("JARVIS_YML_DOCKER_IMAGE")}"
export JARVIS_YML_TIME_OUT="{os.getenv("JARVIS_YML_TIME_OUT")}"
export JARVIS_YML_OUTDIR="{os.getenv("JARVIS_YML_OUTDIR")}"
export JARVIS_WORKSPACE="{JARVIS_WORKSPACE}"

export CSBUILD_PATH="{os.getenv("CSBUILD_PATH")}"
export OPENAI_PATH="{os.getenv("OPENAI_PATH")}"

export CHECKER="{os.getenv("CHECKER")}"
export LANGUAGE="{os.getenv("LANGUAGE")}"

export CSBUILD_USER_OPTION="{os.getenv("CSBUILD_USER_OPTION")}"

                        """
        f.write(setenv_yml_data)


def setenv_docker_writter(): # To set variable in docker environment
    with open(fr"{GITHUB_ACTION_PATH}/jarvis/env_sh/setenv_docker.sh", "w") as f:
        setenv_docker_data = f"""#!/bin/bash

export GITHUB_REPOSITORY="{os.getenv("GITHUB_REPOSITORY")}"
export GITHUB_WORKSPACE="{os.getenv("GITHUB_WORKSPACE")}"
export TARGET_REPO_NAME="{os.getenv("TARGET_REPO_NAME")}"

export JARVIS_WORKSPACE="{JARVIS_WORKSPACE}"
export COPIED_WORKSPACE="{JARVIS_WORKSPACE[1:]}"

export JARVIS_TARGET="{os.path.join(JARVIS_WORKSPACE, GITHUB_REPOSITORY) if GITHUB_REPOSITORY else JARVIS_WORKSPACE}"
export JARVIS_YML_PATH="{os.path.join(JARVIS_TARGET, "jarvis.yml")}"
export JARVIS_OUTPUT_DIR="{os.path.join(JARVIS_WORKSPACE, "output", GITHUB_REPOSITORY, JARVIS_SUFFIX)}"
export ACTION_CALL=TRUE
echo $JARVIS_WORKSPACE
echo $ACTION_CALL

                        """
        f.write(setenv_docker_data)


def git_config_writter():
    with open(fr"{GITHUB_ACTION_PATH}/jarvis/env_sh/git_config.sh", "w") as f:
        git_config_data = f"""#!/bin/bash

export JARVIS_WORKSPACE={JARVIS_WORKSPACE}
export JARVIS_TARGET={JARVIS_TARGET}

echo "$JARVIS_TARGET"

cd "$JARVIS_WORKSPACE"

git clone https://{os.getenv("TOKEN")}@github.com/{os.getenv("GITHUB_REPOSITORY")}.git {os.getenv("GITHUB_REPOSITORY")}

git config --global --add safe.directory "$JARVIS_TARGET"
git config --global user.email "jarvis@action"
git config --global user.name "jarvis-action"

cd "$JARVIS_TARGET"

DESTINATION_BRANCH={os.getenv('GITHUB_REF_NAME')}

echo ==========Switching to $DESTINATION_BRANCH==========
git checkout $DESTINATION_BRANCH
git clean -f > /dev/null
echo ==================================

echo ==========gh auth login==========
echo {os.getenv("TOKEN")} > {JARVIS_WORKSPACE}/scripts/token
gh auth login --with-token < {JARVIS_WORKSPACE}/scripts/token
gh auth status
rm {JARVIS_WORKSPACE}/scripts/token
echo ==================================

                        """
        f.write(git_config_data)


# def setenv_docker_writter(yml):
#     with open(fr"{GITHUB_ACTION_PATH}jarvis/temp/setenv_yml.sh", "w") as f:
#         setenv_yml_data = f"""
# #!/bin/bash


#                         """
#         f.write(setenv_yml_data)

def _parse_yaml():
    with open(JARVIS_YML_PATH) as f:
        yml = yaml.safe_load(f)


    for k, v in yml.items():
        if v is None:
            yml[k] = ""
        if type(v) is not str:
            yml[k] = str(v)

    pprint.pprint(yml)

    os.environ["JARVIS_YML_NAME"] = yml["name"]
    os.environ["JARVIS_YML_DOCKER_IMAGE"] = yml["docker-image"] if "docker-image" in yml else ""
    os.environ["JARVIS_YML_EXTRA_BUILD_ENV_SETTING_COMMAND"] = yml["extra-build-env-setting-commands"] if "extra-build-env-setting-commands" in yml else "" #??? 필요할까?
    os.environ["JARVIS_YML_TIME_OUT"] = yml["time-out"]
    os.environ["JARVIS_YML_BUILD_SUBDIR"] = yml["build-subdir"] if "build-subdir" in yml else "" #??? 필요할까?
    os.environ["JARVIS_YML_OUTDIR"] = yml["output-dir"] if "output-dir" in yml else ""
    os.environ["JARVIS_WORKSPACE"] = yml["workspace"] if "workspace" in yml else ""
    os.environ["CSBUILD_PATH"] = yml["csbuild-path"]
    os.environ["OPENAI_PATH"] = yml["openai-path"]
    os.environ["CHECKER"] = yml["checker"]
    os.environ["LANGUAGE"] = yml["language"]
    os.environ["CSBUILD_USER_OPTION"] = yml["csbuild-option"] if "csbuild-option" in yml else ""
    print("User option: " + os.getenv("CSBUILD_USER_OPTION")) 

    return yml


os.chdir(f"{GITHUB_ACTION_PATH}/jarvis")
os.mkdir("env_sh")
target_yml = _parse_yaml()
setenv_writter()
setenv_yml_writter(target_yml)
setenv_docker_writter()
git_config_writter()