import json
import os
import shutil
import sys
import yaml
import subprocess

import pyfiglet
from dotenv import load_dotenv


GITHUB_ACTION_PATH = os.getenv("GITHUB_ACTION_PATH", "/")
JARVIS_OUTPUT_DIR = os.getenv("JARVIS_OUTPUT_DIR")
JARVIS_TARGET_NAME = os.getenv("JARVIS_TARGET_NAME")
JARVIS_TARGET = os.getenv("JARVIS_TARGET")
# JARVIS_YML_SUBDIR = os.getenv("JARVIS_YML_SUBDIR")
JARVIS_YML_PATH = os.path.join(JARVIS_TARGET, "jarvis.yml")
JARVIS_YML_TIME_OUT = os.getenv("JARVIS_YML_TIME_OUT")
JARVIS_ON_DOCKER = os.getenv("JARVIS_ON_DOCKER")
# JARVIS_YML_TEST_TIME_OUT = os.getenv("JARVIS_YML_TEST_TIME_OUT")
RUN_RULECHECK = os.getenv("RUN_RULECHECK")
# RUN_APR = os.getenv("RUN_APR")
# VALIDATOR = os.getenv("VALIDATOR", None)

GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
OPENAI_API_KEY = ""
TARGET_DIR = ""


# for JARVIS
JARVIS_REPO = os.environ["JARVIS_REPO"] = r"/home/workspace/JARVIS"

# mutable environment variables
MUTABLE_ENV = dict()


def handle_error(return_value, error_message, additional_command=None):
    if return_value != 0:
        print(f"[ERROR] {error_message}", flush=True)
        if additional_command:
            print(f"[DEBUG] {additional_command}", flush=True)
            os.system(additional_command)
        sys.exit(return_value)


def set_environments(jarvis_output_path):
    ascii_banner = pyfiglet.figlet_format("JARVIS")
    print(ascii_banner)

    # OPENAI_API_KEY가 있는지 체크... 이걸 input으로 받아야 하나? 공개할 순 없잖
    # 없을 경우 종료
    # OPENAI_API_KEY를 환경변수로 추가하거나 .env에 추가 필요
    load_dotenv()
    OPENAI_PATH = os.getenv("OPENAI_PATH")
    CSBUILD_PATH = os.getenv("CSBUILD_PATH")
    TARGET_DIR = os.getenv("TARGET_DIR")

    if OPENAI_PATH == None:
        print("[!] Error: OPENAI_PATH is not set. Please export it as 'export OPENAI_API_KEY=<Your_API_Key>'.")
        exit(-1)

    if CSBUILD_PATH == None:
        print("[!] Error: CSBUILD_PATH is not set. Please export it as 'export CSBUILD_PATH=<CSBUILD path in your localhost>'.")
        exit(-1)

    if TARGET_DIR == None:
        print("[!] Error: TARGET_DIR is not set. Please export it as 'export TARGET_DIR=<TARGET_ABSOLUTE_DIR>'.")
        exit(-1)


def run_dockerfile(workspace="/home/workspace", mount_dir=None):
    with open(fr"{workspace}/Dockerfile", "w"):
        dockerfile_data = f"""
                            FROM ubuntu:20.04 \

                            RUN apt update \
                            RUN apt install -y vim binutils gcc g++ make python3 \
                            RUN apt-get -y install python3-pip \

                            RUN useradd --home-dir {workspace} jarvis \
                            WORKDIR {workspace} \

                        """
    docker_build_cmd = ["docker", "build", "-t", "ubuntu20.04", "."] #이렇게 해 두긴 했는데... 향후에는 필요한 거 전부(STATIC, openai key만 빼고) 세팅된 docker image를 제공하자
    if mount_dir is None:
        docker_run_cmd = ["docker", "run", "--name", "jarvis-ubuntu20.04", "-u", "jarvis:jarvis", "-itu", "ubuntu20.04"]
    else:
        docker_run_cmd = ["docker", "run", "--name", "jarvis-ubuntu20.04", "-u", "jarvis:jarvis", "-v", f"{mount_dir}/:{workspace}/", "-itu", "ubuntu20.04"]
    build_ret = subprocess.run(docker_build_cmd, stderr=None, stdout=None)
    run_ret = subprocess.run(docker_run_cmd, stderr=None, stdout=None)


def copy_dependencies(csbuild_path, openai_path):
    docker_copy_setenv_cmd = f"docker cp {GITHUB_WORKSPACE}/docker_scripts/ jarvis-ubuntu20.04:/home/workspace/"
    subprocess.run(docker_copy_setenv_cmd)
    docker_copy_csbuild_cmd = f"docker cp {csbuild_path} jarvis-ubuntu20.04:/home/workspace/tbeg/"
    subprocess.run(docker_copy_csbuild_cmd)
    docker_copy_openai_cmd = f"docker cp {openai_path} jarvis-ubuntu20.04:/home/workspace/tbeg/"
    subprocess.run(docker_copy_openai_cmd)


def run_setenv():
    docker_exec_cmd = ["docker", "exec", "jarvis-ubuntu20.04", fr"{GITHUB_WORKSPACE}/docker_scripts/setenv.sh"]
    build_ret = subprocess.run(docker_exec_cmd, stderr=None, stdout=None)


def run_setenv_yml():
    docker_exec_cmd = ["docker", "exec", "jarvis-ubuntu20.04", fr"{GITHUB_WORKSPACE}/docker_scripts/setenv_yml.sh"]
    build_ret = subprocess.run(docker_exec_cmd, stderr=None, stdout=None)


def run_create_issue():
    os.chdir(TARGET_DIR) #copied repository로
    create_issue_sh_path = os.path.join(GITHUB_ACTION_PATH, "jarvis", "git", "create-issue.sh")
    create_issue_cmd = f"bash {create_issue_sh_path}"
    ret = os.system(create_issue_cmd
                    )
    handle_error(ret, "[ERROR] issue return non-zero")


def run_create_pull_request():
    create_pull_request_py_path = os.path.join(GITHUB_ACTION_PATH, "jarvis", "git", "create-pull-request.py")
    create_pr_cmd = f"python3 {create_pull_request_py_path}"
    ret = os.system(create_pr_cmd)
    handle_error(ret, "[ERROR] pull-request return non-zero")


def run_rulecheck():
    set_environments(JARVIS_OUTPUT_DIR)
    if RUN_RULECHECK:
        os.chdir(JARVIS_REPO)
        jarvis_cmd = f"python3 main.py"
        print(f"[DEBUG] {jarvis_cmd}", flush=True)
        ret = os.system(jarvis_cmd)
        handle_error(ret, "jarvis return non-zero")
    run_create_issue()

    code_fixed = True # Nonzero면 일단 코드 수정은 잘 됐단 것 같은데.... 확실치 않으므로 결과 정리하는 logic이 필요할지도
    if code_fixed:
        run_create_pull_request()


run_rulecheck()
