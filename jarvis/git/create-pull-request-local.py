import git
import json
import os
import subprocess
import datetime
import glob


GITHUB_REF_NAME = os.getenv("GITHUB_REF_NAME", None)
GITHUB_ACTION_PATH = os.getenv("GITHUB_ACTION_PATH")
ACTION_TEMP_DIR = os.path.join(GITHUB_ACTION_PATH, "jarvis", "temp", "outputs")

JARVIS_WORKSPACE = os.getenv("JARVIS_WORKSPACE")
JARVIS_OUTPUT_DIR = os.path.join(JARVIS_WORKSPACE, "JARVIS", "workspace", "outputs")
JARVIS_TARGET= os.getenv("JARVIS_TARGET")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
TOKEN = os.getenv("TOKEN")

PR_INFO = dict()


def construct_pr_info():
    with open(os.path.join(ACTION_TEMP_DIR, "issue_link")) as f:
        PR_INFO["issue_link"] = f.read().strip()
    PR_INFO["issue_number"] = PR_INFO["issue_link"].split("/")[-1]
    
    print(f"[DEBUG] generate pr title", flush=True)
    pr_title = f"Fixed #{PR_INFO['issue_number']}"
    PR_INFO["title"] = pr_title


def _gen_diff_list():
    output_dir = ACTION_TEMP_DIR
    print(f"Output temp dir: {output_dir}")
    diff_list = glob.glob(f"{output_dir}/*.diff")
    print(diff_list)

    return diff_list


def create_pull_request(patch_branch):
    pr_title = PR_INFO["title"]
    commit = os.getenv('GITHUB_SHA')
    print("[DEBUG] PR")
    pr_body = f"This PR is auto-patch by JARVIS for commit: {commit} Fixed #{PR_INFO['issue_number']}"
    pr_command = f"gh pr create -B {GITHUB_REF_NAME} -H {patch_branch} -t \"{pr_title}\" -b\"{pr_body}\""
    os.system(pr_command)


def run():
    print(f"[DEBUG] create pr", flush=True)

    patch_path = f"{ACTION_TEMP_DIR}/fix_violation.patch"
    print(f"Patch path: {patch_path}")
    
    os.system("git clean -xdf")
    os.system(f"git checkout {GITHUB_REF_NAME}")
    os.system("git checkout .")
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    patch_branch = f"{GITHUB_REF_NAME}-auto-patch-{now}"
    os.system(f"git checkout -b {patch_branch}")
    diff_list = _gen_diff_list()
    for diff in diff_list:
        print(diff)
        os.system(f"git apply < {diff}")
    os.system(f"git add .")
    os.system(f"git commit -m \"Fixed automatically #{PR_INFO['issue_number']} by JARVIS\"")
    os.system(f"gh auth login --with-token < {GITHUB_ACTION_PATH}/token.txt")
    os.system(f"git push origin {patch_branch}")
    create_pull_request(patch_branch)
    os.system(f"git checkout {GITHUB_REF_NAME}")


construct_pr_info()
run()
