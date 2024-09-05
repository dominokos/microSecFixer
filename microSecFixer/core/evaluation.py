import json
import os
from microCertiSec import microCertiSec
from microSecFixer.core.rule_map import RuleMap

def evaluate_dfd(model_path: str, traceability_path: str, rule: str):
    return microCertiSec.microCertiSec_API(model_path, traceability_path, rule)

def clear_result_dir(result_dir: str):
    filelist = [ f for f in os.listdir(result_dir) ]
    for f in filelist:
        os.remove(os.path.join(result_dir, f))

def find_all_violations(dfd_path: str) -> str:
    repo_name_json = dfd_path.split("models/")[1] 
    model_path = f".{dfd_path}"
    traceability_path = model_path.replace(".json", "_traceability.json")
    rule_map = RuleMap.get_rules()
    result_directory = f"./output/results/{repo_name_json}/"
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


