import json
import os
from microCertiSec import microCertiSec
from microSecFixer.core.rule_map import RuleMap

def evaluate_dfd(model_path: str, rule: str, traceability_path: str = None):
    return microCertiSec.microCertiSec_API(model_path, rule, traceability_path)

def clear_result_dir(result_dir: str):
    filelist = [ f for f in os.listdir(result_dir) ]
    for f in filelist:
        os.remove(os.path.join(result_dir, f))

def find_next_violation(dfd_path: str, output_path: str, lower_bound: int = 1) -> str:
    model_file = dfd_path.split("/")[-1:][0]
    traceability_path = dfd_path.replace(".json", "_traceability.json")
    rule_map = RuleMap.get_rules()
    result_directory = f"{output_path}results/{model_file}/"
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)
    clear_result_dir(result_directory)

    for i in range(lower_bound, 26):
        result = evaluate_dfd(dfd_path, rule_map[i], traceability_path)
        # Skip if the verdict is positive (rule is adhered to)
        verdict = None
        for rule in result.property_check_evidence_json.values():
            if rule.get("verdict"):
                verdict = rule["verdict"]
                break
            elif rule.get(next(iter(rule))):
                verdict = rule[next(iter(rule))]["verdict"]
                break
        is_i_single_digit = i // 10 < 1
        if(is_i_single_digit):
            with open(f"{result_directory}r0{i}{model_file}", "w") as output_file:
                json.dump(result.property_check_evidence_json, output_file)
            if not verdict:
                return f"r0{i}"
        else:
            with open(f"{result_directory}r{i}{model_file}", "w") as output_file:
                json.dump(result.property_check_evidence_json, output_file)
            if not verdict:
                return f"r{i}"
    return None

def find_violation(dfd_path: str, rule_to_check: str, output_path: str) -> tuple[str, bool]:
    model_file = dfd_path.split("/")[-1:][0]
    rule_map = RuleMap.get_rules()
    result_directory = f"{output_path}results/{model_file}/"
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)
    clear_result_dir(result_directory)
    result = evaluate_dfd(dfd_path, rule_map[rule_to_check])
    # Skip if the verdict is positive (rule is adhered to)
    verdict = None
    for rule in result.property_check_evidence_json.values():
        if rule.get("verdict"):
            verdict = rule["verdict"]
            break
        elif rule.get(next(iter(rule))):
            verdict = rule[next(iter(rule))]["verdict"]
            break
    is_rtc_single_digit = rule_to_check // 10 < 1
    if(is_rtc_single_digit):
        with open(f"{result_directory}r0{rule_to_check}{model_file}", "w") as output_file:
            json.dump(result.property_check_evidence_json, output_file)
        return (f"r0{rule_to_check}", verdict)
    else:
        with open(f"{result_directory}r{rule_to_check}{model_file}", "w") as output_file:
            json.dump(result.property_check_evidence_json, output_file)
        return (f"r{rule_to_check}", verdict)


