import os
import json

JARVIS_OUTPUT_DIR = os.getenv("JARVIS_OUTPUT_DIR")
JARVIS_WORKSPACE = os.getenv("JARVIS_WORKSPACE")

def generate_issue_title():
    '''
    issue: Violated rule(s) {rule name} etc.
    pr:    Fixed Violation(s) {rule name} etc. (#)
    '''
    print(f"[DEBUG] create issue title", flush=True)
    output_dir = os.path.join(JARVIS_WORKSPACE, "JARVIS", "workspace", "outputs")

    with open(f"{output_dir}/violated_rules.json", "r") as rules:
        rule_info = json.load(rules)
        rule_info_dict = json.loads(rule_info)

        print(type(rules))
        print(rule_info)
        print(type(rule_info))
        print(rule_info_dict)
        rule_list = list(rule_info_dict.keys())

    if len(rule_list) > 1:
        issue_title = f"Violated rule {rule_info_dict[rule_list[0]][0]} etc."
    elif len(rule_list) == 1:
        issue_title = f"Violated rule {rule_info_dict[rule_list[0]][0]}"
    else: # Should not happen
        issue_title = f"[CRITICAL] No violated rule"

    with open(os.path.join(output_dir, "issue_title"), "a") as title_file:
        title_file.write(issue_title)

generate_issue_title()
