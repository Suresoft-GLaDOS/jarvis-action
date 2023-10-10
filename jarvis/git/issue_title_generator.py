import os
import json

JARVIS_OUTPUT_DIR = os.getenv("JARVIS_OUTPUT_DIR")
JARVIS_WORKSPACE = os.getenv("JARVIS_WORKSPACE")


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

    issue: Violated rule(s) {rule name} etc.
    pr:    Fixed Violation(s) {rule name} etc. (#)
    '''
    print(f"[DEBUG] create issue title", flush=True)
    output_dir = os.path.join(JARVIS_WORKSPACE, "JARVIS", "workspace", "outputs")

    with open(f"{output_dir}/violated_rules.json", "r") as rules:
        rule_str = rules.read()
        rule_info = json.load(rules)
        rule_info_dict = json.loads(rule_info)

        print(type(rules))
        print(rule_info)
        print(type(rule_info))
        print(rule_str)
        # rule_list = list(rule_info.keys())
        rule_list = list(rule_info_dict.keys())

    if len(rule_list) > 1:
        issue_title = f"Violated rule {rule_list[0]} etc."
    elif len(rule_list) == 1:
        issue_title = f"Violated rule {rule_list[0]}"
    else: # Should not happen
        issue_title = f"[CRITICAL] No violated rule"

    with open(os.path.join(output_dir, "issue_title"), "a") as title_file:
        title_file.write(issue_title)

# collect_violated_rule()
generate_issue_title()
