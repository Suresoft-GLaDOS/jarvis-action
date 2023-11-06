from fix_commit_message import modify_commit_msg

### 각각의 룰 정보와 diff 정보 제공
def test1():
    diff_list = {"diff_suite/result1.diff":"MISRA_C_2012_03_01",
                "diff_suite/result2.diff":"MISRA_C_2012_09_02",
                "diff_suite/result3.diff":"MISRA_C_2012_16_03",
                "diff_suite/result4.diff":"MISRA_C_2012_07_03",
                }
    modify_commit_msg(diff_list)


### 룰 정보 미제공, diff 제공 => Hallucination occurred. :(
def test2():
    diff_list = {"diff_suite/result1.diff":"",
                "diff_suite/result2.diff":"",
                "diff_suite/result3.diff":"",
                "diff_suite/result4.diff":"",
                }
    modify_commit_msg(diff_list)


## diff 각각에 모든 룰 이름 정보
def test3():
    rule_info = ["MISRA_C_2012_03_01", "MISRA_C_2012_09_02", "MISRA_C_2012_16_03", "MISRA_C_2012_07_03"]
    diff_list = {"diff_suite/result1.diff": rule_info ,
                "diff_suite/result2.diff": rule_info ,
                "diff_suite/result3.diff": rule_info ,
                "diff_suite/result4.diff": rule_info ,
                }
    modify_commit_msg(diff_list)


## diff 각각에 모든 룰 정보
def test4():
    base_rules = "MISRA_C_2012_09_02: The initializer for an aggregate or union shall be enclosed in braces violated. \
                MISRA_C_2012_07_03: The lowercase character “l” shall not be used in a literal suffix violated. \
                MISRA_C_2012_16_03: An unconditional break statement shall terminate every switch-clause violated. \
                MISRA_C_2012_03_01: The character sequences /* and // shall not be used within acomment violated. \
                MISRA_C_2012_08_06: A function with external linkage use_int8_ptr has no definition. \
                MISRA_C_2012_08_02: Even though the parameter of function main is not existed, a void type parameter has not been declared explicitly. \
                MISRA_C_2012_08_05: The extern variable R_22_main_support is declared more than once in a translation unit(Previous declared at[line:mc3_header.h, file:248]). \
                "
    diff_list = {"diff_suite/result1.diff":base_rules,
                "diff_suite/result2.diff":base_rules,
                "diff_suite/result3.diff":base_rules,
                "diff_suite/result4.diff":base_rules,
                }
    modify_commit_msg(diff_list)


if __name__ == '__main__':
     test4()