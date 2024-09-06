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

def find_all_violations(dfd_path: str, output_path: str) -> str:
    repo_name_json = dfd_path.split("/")[-1:][0]
    model_path = os.getcwd() + dfd_path
    traceability_path = model_path.replace(".json", "_traceability.json")
    rule_map = RuleMap.get_rules()
    result_directory = f"{output_path}results/{repo_name_json}/"
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)
    clear_result_dir(result_directory)

    for i in range(1, 26):
        result = evaluate_dfd(model_path, traceability_path, rule_map[i])
        # Skip if the verdict is positive (rule is adhered to)
        verdict = None
        for rule in result.property_check_evidence_json.values():
            if rule.get("verdict"):
                verdict = rule["verdict"]
                break
            elif rule.get(next(iter(rule))):
                verdict = rule[next(iter(rule))]["verdict"]
                break
        if verdict:
            continue
        if(i // 10 < 1):
            with open(f"{result_directory}r0{i}{repo_name_json}", "w") as output_file:
                json.dump(result.property_check_evidence_json, output_file)
        else:
            with open(f"{result_directory}r{i}{repo_name_json}", "w") as output_file:
                json.dump(result.property_check_evidence_json, output_file)
    return result_directory

def find_violation(dfd_path: str, rule_to_check: str, output_path: str) -> tuple[str, bool]:
    repo_name_json = dfd_path.split("/")[-1:][0]
    model_path = os.getcwd() + dfd_path
    rule_map = RuleMap.get_rules()
    result_directory = f"{output_path}results/{repo_name_json}/"
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)
    clear_result_dir(result_directory)
    result = evaluate_dfd(model_path, rule_map[rule_to_check])
    # Skip if the verdict is positive (rule is adhered to)
    verdict = None
    for rule in result.property_check_evidence_json.values():
        if rule.get("verdict"):
            verdict = rule["verdict"]
            break
        elif rule.get(next(iter(rule))):
            verdict = rule[next(iter(rule))]["verdict"]
            break
    if(rule_to_check // 10 < 1):
        with open(f"{result_directory}r0{rule_to_check}{repo_name_json}", "w") as output_file:
            json.dump(result.property_check_evidence_json, output_file)
    else:
        with open(f"{result_directory}r{rule_to_check}{repo_name_json}", "w") as output_file:
            json.dump(result.property_check_evidence_json, output_file)
    return (result_directory, verdict)


