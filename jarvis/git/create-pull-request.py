import git
import json
import os
import datetime


GITHUB_REF_NAME = os.getenv("GITHUB_REF_NAME", None)

JARVIS_WORKSPACE = os.getenv("JARVIS_WORKSPACE")
JARVIS_OUTPUT_DIR = os.path.join(JARVIS_WORKSPACE, "JARVIS", "workspace", "outputs")
JARVIS_TARGET= os.getenv("JARVIS_TARGET")

PR_INFO = dict()


def construct_pr_info():
    with open(os.path.join(JARVIS_OUTPUT_DIR, "issue_link")) as f:
        PR_INFO["issue_link"] = f.read().strip()
    PR_INFO["issue_number"] = PR_INFO["issue_link"].split("/")[-1]
    
    print(f"[DEBUG] generate pr title", flush=True)
    pr_title = f"Fixed #{PR_INFO['issue_number']}"
    PR_INFO["title"] = pr_title


def create_pull_request(patch_branch):
    pr_title = PR_INFO["title"]
    commit = os.getenv('GITHUB_SHA')
    print("[DEBUG] PR")
    pr_body = f"This PR is auto-patch by JARVIS for commit: {commit} Fixed #{PR_INFO['issue_number']}"
    pr_command = f"gh pr create -B {GITHUB_REF_NAME} -H {patch_branch} -t \"{pr_title}\" -b\"{pr_body}\""
    os.system(pr_command)


def run():
    print(f"[DEBUG] create pr", flush=True)
    output_dir = os.path.join(JARVIS_WORKSPACE, "JARVIS", "workspace", "outputs")

    patch_path = f"{output_dir}/fix_violation.patch"
    print(f"Patch path: {patch_path}")
    
    os.system("git clean -xdf")
    os.system(f"git checkout {GITHUB_REF_NAME}")
    os.system("git checkout .")
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    patch_branch = f"{GITHUB_REF_NAME}-auto-patch-{now}"
    os.system(f"git checkout -b {patch_branch}")
    os.system(f"git apply < {patch_path}")
    os.system(f"git add .")
    os.system(f"git commit -m \"Fixed automatically #{PR_INFO['issue_number']} by Vulcan\"")
    os.system(f"git remote -v")
    os.system(f"git push origin {patch_branch}")
    create_pull_request(patch_branch)
    os.system(f"git checkout {GITHUB_REF_NAME}")


construct_pr_info()
run()
