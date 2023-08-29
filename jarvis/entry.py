import datetime
import os
import pprint
import sys
import yaml


GITHUB_ACTION_PATH = os.getenv("GITHUB_ACTION_PATH", "/")
GITHUB_ACTOR = os.getenv("GITHUB_ACTOR")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
VULCAN_TARGET_NAME = os.getenv("VULCAN_TARGET")

VULCAN_TARGET = os.path.join(GITHUB_WORKSPACE, VULCAN_TARGET_NAME) if VULCAN_TARGET_NAME else GITHUB_WORKSPACE
VULCAN_TARGET_NAME = VULCAN_TARGET_NAME if VULCAN_TARGET_NAME else os.path.basename(VULCAN_TARGET)
VULCAN_YML_PATH = os.path.join(VULCAN_TARGET, "vulcan.yml")
VULCAN_SUFFIX = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
VULCAN_OUTPUT_DIR = os.path.realpath(os.path.join(GITHUB_WORKSPACE, "..", "..", "output", GITHUB_ACTOR, GITHUB_REPOSITORY, VULCAN_SUFFIX))


