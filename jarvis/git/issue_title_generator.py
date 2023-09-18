import os
import json

JARVIS_OUTPUT_DIR = os.getenv("JARVIS_OUTPUT_DIR")


def collect_violated_rule():
    print(f"[DEBUG] collect violated rule", flush=True)
    defect_info_dir = os.path.join(JARVIS_OUTPUT_DIR, "defect_info.json")
    with open(os.path.join(JARVIS_OUTPUT_DIR, "violated.rule"), "a") as rules:
        with open(defect_info_dir) as defect_info_json:
            defect_info = json.load(defect_info_json)
            for defect in defect_info['defects']:
                rules.write(str(defect['rule']) + "\n")


def generate_issue_title():
    '''

    issue: Failed test(s) {test command} etc.
    pr:    Fixed test(s) {test command} etc. (#)
    '''
    print(f"[DEBUG] create issue title", flush=True)
    defect_info_dir = os.path.join(JARVIS_OUTPUT_DIR, "defect_info.json")
    with open(os.path.join(JARVIS_OUTPUT_DIR, "violated.rule"), "a") as rules:
        with open(defect_info_dir) as defect_info_json:
            defect_info = json.load(defect_info_json)
            if len(defect_info) > 1:
                issue_title = f"Failed tests {defect_info['rule'][0]['rule']} etc."
            elif len(defect_info) == 1:
                issue_title = f"Failed test {defect_info['rule'][0]['rule']}"
            else: # Should not happen
                issue_title = f"[CRITICAL] No violated rule"
        rules.write(issue_title)


collect_violated_rule()
generate_issue_title()
