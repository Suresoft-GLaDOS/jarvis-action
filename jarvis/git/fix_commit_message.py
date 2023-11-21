import openai
import json
import os
from dotenv import load_dotenv

base_messages = [
    {"role": "system", 
    "content": "I want you to act as a C langague code corrector."},
    {"role": "user", 
    "content": "You have fixed violations of MISRA rules. \
    Now, I will show you the changes you've made to the code using a diff file. \
    Please briefly explain this diff file. \
    You must explain only the parts that you fixed in relation to the MISRA rules I provided, specifically those related to the diff. \
    # Please explain only the parts that were fixed in relation to the MISRA rule I provided."
    # This diff file contains the changes you made to correct the code that violated MISRA rules, saved in a diff format. \
    #Please explain only the parts that were fixed in relation to the MISRA rule."
    }
]

def modify_commit_msg(diff, rule_info_dict):
    # get Open API Key
    load_dotenv()
    openai.api_key= os.getenv("OPENAI_API_KEY")
    JARVIS_WORKSPACE = os.getenv("JARVIS_WORKSPACE")
    THRESHOLD = os.getenv("THRESHOLD", None)
    print(f"{JARVIS_WORKSPACE}/openai/openai_key")
    with open(f"{JARVIS_WORKSPACE}/openai/openai_key", "r") as f:
        OPENAI_API_KEY = f.readline().strip()
    print(f"Open AI KEY: {OPENAI_API_KEY[-5:]}")
    openai.api_key = OPENAI_API_KEY

    issue_msg = ""

    print("Rule info dict: " + str(rule_info_dict))

    print("Sending...\n")
    print("[+] target: ", diff)
    print("[+] rule : ", str(rule_info_dict))

    violated_rule_in_file = rule_info_dict[diff]
    print("[+] rule in this file : ", str(violated_rule_in_file))    

    with open(diff, "r+") as f:
        diff_contents = f.read()

    print("\n[+] diff_contents : \n\n", diff_contents)

    # diff 파일 설명을 위한 messages 구성
    messages = base_messages + \
    [{"role": "user",
        "content": 
        "Rule:" f"{str(violated_rule_in_file)}" "\n"
        "The next contents are from a diff file.\n"
        f"{diff_contents}"
    }]

    print("----------------------------------------\n")
    # gpt에게 설명 요청
    response = openai.ChatCompletion.create(
    model="gpt-4-1106-preview",
    messages=messages,
    )

    issue_msg += response.choices[0].message.content
    issue_msg += "\n"
    print(response.choices[0].message.content)
    print("=====================================================\n\n")

    return issue_msg

