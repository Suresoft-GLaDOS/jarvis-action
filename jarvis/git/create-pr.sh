#!/bin/bash

os.system("git clean -xdf")
os.system(f"git checkout {GITHUB_REF_NAME}")
os.system("git checkout .")
now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
patch_branch = f"{GITHUB_REF_NAME}-auto-patch-{now}"
os.system(f"git checkout -b {patch_branch}")
patch_full_path = os.path.join(MSV_PATCH_DIFF_PATH, p)
os.system(f"patch -p0 < {patch_full_path}")
os.system(f"git add .")
os.system(f"git commit -m \"Fixed automatically #{PR_INFO['issue_number']} by Vulcan\"")
os.system(f"git push origin {patch_branch}")
create_pull_request(patch_branch)
os.system(f"git checkout {GITHUB_REF_NAME}")