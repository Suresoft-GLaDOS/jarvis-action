import json
import os
import shutil
import sys
import yaml

import pyfiglet
from dotenv import load_dotenv


GITHUB_ACTION_PATH = os.getenv("GITHUB_ACTION_PATH", "/")
JARVIS_OUTPUT_DIR = os.getenv("JARVIS_OUTPUT_DIR")
JARVIS_TARGET_NAME = os.getenv("JARVIS_TARGET_NAME")
JARVIS_TARGET = os.getenv("JARVIS_TARGET")
# JARVIS_YML_SUBDIR = os.getenv("JARVIS_YML_SUBDIR")
JARVIS_YML_PATH = os.path.join(JARVIS_TARGET, "jarvis.yml")
JARVIS_YML_TIME_OUT = os.getenv("JARVIS_YML_TIME_OUT")
# JARVIS_YML_TEST_TIME_OUT = os.getenv("JARVIS_YML_TEST_TIME_OUT")
RUN_RULECHECK = os.getenv("RUN_RULECHECK")
# RUN_APR = os.getenv("RUN_APR")
# VALIDATOR = os.getenv("VALIDATOR", None)

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

    # OPENAI_API_KEY가 있는지 체크
    # 없을 경우 종료
    # OPENAI_API_KEY를 환경변수로 추가하거나 .env에 추가 필요
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TARGET_DIR = os.getenv("TARGET_DIR")

    if OPENAI_API_KEY == None:
        print("[!] Error: OPENAI_API_KEY is not set. Please export it as 'export OPENAI_API_KEY=<Your_API_Key>'.")
        exit(-1)

    if TARGET_DIR == None:
        print("[!] Error: TARGET_DIR is not set. Please export it as 'export TARGET_DIR=<TARGET_ABSOLUTE_DIR>'.")
        exit(-1)


def run_create_issue():
    os.chdir(TARGET_DIR) #copied repository로
    create_issue_sh_path = os.path.join(GITHUB_ACTION_PATH, "jarvis", "git", "create-issue.sh")
    create_issue_cmd = f"bash {create_issue_sh_path}"
    ret = os.system(create_issue_cmd)
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
    run_create_pull_request() # Nonzero면 일단 코드 수정은 잘 됐단 것 같은데.... 확실치 않으므로 결과 정리하는 logic이 필요할지도


run_rulecheck()
