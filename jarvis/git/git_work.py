import json
import os
import shutil
import sys
import yaml
from issue_body_generator import generate_issue_body
from issue_title_generator import collect_violated_rule, generate_issue_title


JARVIS_OUTPUT_DIR = os.getenv("JARVIS_OUTPUT_DIR")
JARVIS_WORKSPACE = os.getenv("JARVIS_WORKSPACE")

generate_issue_body()
generate_issue_title()
