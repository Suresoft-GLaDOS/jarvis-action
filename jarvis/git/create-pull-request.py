import git
import json
import os
import subprocess
import datetime
import glob


GITHUB_REF_NAME = os.getenv("GITHUB_REF_NAME", None)
GITHUB_ACTION_PATH = os.getenv("GITHUB_ACTION_PATH")


JARVIS_WORKSPACE = os.getenv("JARVIS_WORKSPACE")
# ACTION_TEMP_DIR = os.path.join(JARVIS_WORKSPACE, "JARVIS", "workspace", "outputs")
JARVIS_OUTPUT_DIR = os.path.join(JARVIS_WORKSPACE, "JARVIS", "workspace", "outputs")
JARVIS_TARGET= os.getenv("JARVIS_TARGET")
TARGET_WORKSPACE = os.path.join(JARVIS_WORKSPACE, "JARVIS", "workspace", JARVIS_TARGET)
print("Declare Target workspace: " + TARGET_WORKSPACE)
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE", "/mnt/d/iitp/IITP_JARVIS/jarvis_workspace/actions-runner/_work/JARVIS_demo/JARVIS_demo")

PR_INFO = dict()


def construct_pr_info():
    with open(os.path.join(JARVIS_OUTPUT_DIR, "issue_link")) as f:
        PR_INFO["issue_link"] = f.read().strip()
    PR_INFO["issue_number"] = PR_INFO["issue_link"].split("/")[-1]
    
    print(f"[DEBUG] generate pr title", flush=True)
    pr_title = f"Fixed #{PR_INFO['issue_number']}"
    PR_INFO["title"] = pr_title


def _gen_diff_list():
    output_dir = JARVIS_OUTPUT_DIR
    print(f"Output temp dir: {output_dir}")
    diff_list=glob.glob(f"{output_dir}/**/*.diff", recursive=True)
    return diff_list


def create_pull_request(patch_branch):
    pr_title = PR_INFO["title"]
    commit = os.getenv('GITHUB_SHA')
    print("[DEBUG] PR")
    pr_body = f"This PR is auto-patch by JARVIS for commit: {commit} Fixed #{PR_INFO['issue_number']}"
    pr_command = f"gh pr create -B {GITHUB_REF_NAME} -H {patch_branch} -t \"{pr_title}\" -b\"{pr_body}\""
    os.system(pr_command)


def get_token():
    token = ""
    with open(os.path.join(JARVIS_WORKSPACE, "token.txt"), "r") as f:
        token = f.read()
    return token


def run():
    print(f"[DEBUG] create pr", flush=True)

    # patch_path = f"{ACTION_TEMP_DIR}/fix_violation.patch"
    # print(f"Patch path: {patch_path}")
    
    # os.system("git clean -xdf")
    
    # os.system("git checkout .")
    os.chdir(TARGET_WORKSPACE)
    print("Target workspace: " + TARGET_WORKSPACE)
    os.system(f"git checkout {GITHUB_REF_NAME}")
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    
    # diff_list = _gen_diff_list()
    # for diff in diff_list:
    #     print('Diff:' + diff)
    #     target_path = GITHUB_WORKSPACE + diff.split("outputs")[1].replace('.diff', '')
    #     print('Target:' + target_path)
    #     with open(target_path, 'rt', encoding='UTF8',  errors='ignore') as f:
    #         print("Replace!")
    #         text = f.read().replace("r\r\n", "r\n")
    #     with open(target_path, 'wt', encoding='UTF8',  errors='ignore') as f:
    #         print("Write!")
    #         f.write(text)


    
    # for diff in diff_list:
    #     os.system(f"git apply < {diff}")

    patch_branch = f"{GITHUB_REF_NAME}-auto-patch-{now}"
    print("Checkout new branch")
    os.system(f"git checkout -b {patch_branch}")
    print("Add")
    os.system(f"git add .")
    print("Commit")
    os.system(f"git commit -m \"Fixed automatically #{PR_INFO['issue_number']} by JARVIS\"")
    # print("Login")
    # os.system(f"gh auth login --with-token < {JARVIS_WORKSPACE}/token.txt")
    print("Login with token")
    os.system(f"gh auth login --with-token < {JARVIS_WORKSPACE}/token.txt; git push origin {patch_branch}")
    # create_pull_request(patch_branch)
    # os.system(f"git checkout {GITHUB_REF_NAME}")
    # print("Just check")


construct_pr_info()
run()
