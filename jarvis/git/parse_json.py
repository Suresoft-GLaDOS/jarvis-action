import json
import os

WORKSPACE = '/mnt/d/iitp/IITP_JARVIS/save/1123/outputs'

def __read_result_file(workspace_prj):
    try:
        with open(workspace_prj + '/violations.json', 'r') as f:
            result = json.load(f)

        result_json = result
        return result

    except Exception as e: 
        print("CODE_FIX | __read_result_file | {}".format(str(e)))
        raise AssertionError("Abnormal Exit")
    
def parse_json():
    result = __read_result_file(WORKSPACE)
    revised_file_list = []

    violated_rules = set()

    violated_per_file_dict = {}
    violated_rules_dict = {}

    print("Length of result: " + str(len(result)))

    for i in range(len(result)):
        violated_rules_per_file = set()
        for func in result[i]['defects']:

            for defect in result[i]['defects'][func]:
                violated_rules_per_file.add(f"{defect['name']}: {defect['title']}\n")

        # logger.info("Per File: " + result[i]['path'])
        violated_per_file_dict[result[i]['path']] = list(violated_rules_per_file)

    #logger.info(violated_rules)
    violated_rules_str = []
    for rule in violated_rules:
        violated_rules_dict[rule[0]] = rule[1]

    violated_rules_json = json.dumps(violated_per_file_dict)
    # violated_rules_json = json.dumps(violated_rules_dict)

    with open("/mnt/d/iitp/IITP_JARVIS/save/1123/outputs/violated_rules_check.json", 'w') as outfile:
        print("Was it written?\n")
        json.dump(violated_rules_json, outfile)

parse_json()