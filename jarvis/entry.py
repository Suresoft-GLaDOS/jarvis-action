import datetime
import os
import pprint
import sys
import yaml
import subprocess


GITHUB_ACTION_PATH = os.getenv("GITHUB_ACTION_PATH", "/")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
TARGET_DIR = os.getenv("TARGET_DIR")
TARGET_REPO_NAME = os.getenv("TARGET_REPO_NAME")

JARVIS_TARGET = os.path.join(GITHUB_WORKSPACE, TARGET_REPO_NAME) if TARGET_REPO_NAME else GITHUB_WORKSPACE
JARVIS_YML_PATH = os.path.join(TARGET_DIR, "jarvis.yml")
JARVIS_SUFFIX = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
JARVIS_OUTPUT_DIR = os.path.realpath(os.path.join(GITHUB_WORKSPACE, "..", "..", "output", GITHUB_REPOSITORY, GITHUB_REPOSITORY, JARVIS_SUFFIX))

# reset some environment variables

os.environ["TARGET_DIR"] = TARGET_DIR
os.environ["JARVIS_OUTPUT_DIR"] = JARVIS_OUTPUT_DIR


def setenv_writer():
    with open(fr"{GITHUB_ACTION_PATH}/jarvis/docker_setenv_scripts/setenv.sh", "w"):
        dockerfile_data = f"""
                            #!/bin/bash
                            
                            export GITHUB_ACTION_PATH={os.getenv("GITHUB_ACTION_PATH", "/")}
                            export GITHUB_REPOSITORY={os.getenv("GITHUB_REPOSITORY")}
                            export GITHUB_REPOSITORY={os.getenv("GITHUB_REPOSITORY")}
                            export GITHUB_WORKSPACE={os.getenv("GITHUB_WORKSPACE")}
                            export TARGET_DIR={os.getenv("TARGET_DIR")}
                            export TARGET_REPO_NAME={os.getenv("TARGET_REPO_NAME")}
                            
                            export JARVIS_TARGET={os.path.join(GITHUB_WORKSPACE, TARGET_REPO_NAME) if TARGET_REPO_NAME else GITHUB_WORKSPACE}
                            export JARVIS_YML_PATH={os.path.join(TARGET_DIR, "jarvis.yml")}
                            export JARVIS_SUFFIX={datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}
                            export JARVIS_OUTPUT_DIR={os.path.realpath(os.path.join(GITHUB_WORKSPACE, "..", "..", "output", GITHUB_REPOSITORY, GITHUB_REPOSITORY, JARVIS_SUFFIX))}
                            
                            # reset some environment variables
                            
                            export TARGET_DIR={TARGET_DIR}
                            export JARVIS_OUTPUT_DIR={JARVIS_OUTPUT_DIR}

                        """
    # docker_exec_cmd = ["docker", "exec", "jarvis-ubuntu20.04", fr"{GITHUB_ACTION_PATH}/jarvis/scripts/setenv.sh"]
    # try:
    #     build_ret = subprocess.run(docker_exec_cmd, stderr=None, stdout=None)
    # except:
    #     print("Couldn't run setenv.sh")


def setenv_yml_writer(yml):
    with open(fr"{GITHUB_ACTION_PATH}/jarvis/docker_scripts/setenv_yml.sh", "w"):
        dockerfile_data = f"""
                                #!/bin/bash
                                
                                export JARVIS_YML_NAME={yml["name"]}
                                export JARVIS_YML_DOCKER_IMAGE={yml["docker-imageif"] if "docker-image" in yml else ""}
                                export JARVIS_YML_TIME_OUT={yml["time-out"]}
                                export JARVIS_YML_OUTDIR={yml["output-dirif"] if "output-dir" in yml else ""}

                        """
    # docker_exec_cmd = ["docker", "exec", "jarvis-ubuntu20.04", fr"{GITHUB_ACTION_PATH}/jarvis/scripts/setenv_yml.sh"]
    # try:
    #     build_ret = subprocess.run(docker_exec_cmd, stderr=None, stdout=None)
    # except:
    #     print("Couldn't run setenv_yml.sh")


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

    return yml


def main():
    token = os.getenv("TOKEN", None)
    csbuild_path = os.getenv("CSBUILD_PATH", None)
    openai_path = os.getenv("OPENAI_PATH", None)
    if token is None:
        print("Requires jarvis action input: token", flush=True)
        print("Vulcan action with: token: ${{ secrets.GITHUB_TOKEN }}", flush=True)
        exit(1)

    if csbuild_path is None:
        print("Requires jarvis action input: csbuild_path", flush=True)
        exit(1)

    if openai_path is None:
        print("Requires jarvis action input: openai_path", flush=True)
        exit(1)

    if not os.path.exists(JARVIS_YML_PATH):
        print("Requires jarvis.yml in your repository", flush=True)
        exit(1)

    os.makedirs(JARVIS_OUTPUT_DIR, exist_ok=True)
    yml = _parse_yaml()
    setenv_writer()
    setenv_yml_writer(yml)
    sys.stdout.flush()
    entry_sh_path = os.path.join(GITHUB_ACTION_PATH, "jarvis", "entry.sh")
    os.system(f"bash {entry_sh_path}")


main()
