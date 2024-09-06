#!/usr/bin/env python3
#
# Author: Dominik Jacob, 2024
# Contact: dominik.jacob@tuhh.de

import argparse
import os
from configparser import ConfigParser
from datetime import datetime

from microCertiSec.core.model import CModel
import microSecFixer.core.visualizer as visualizer
from microSecFixer.core.evaluation import find_all_violations, find_violation
import microSecFixer.core.logger as logger
from microSecFixer.core.rule_map import RuleMap
import microSecFixer.tmp.tmp as temp
from microCertiSec.microCertiSec import model_api

# For CLI
arg_parser = argparse.ArgumentParser(prog = "microSecFixer",
                                    description = "Takes a architectural model in JSON format and generates an \"ideal\" model which fulfills the rules introduced in microCertiSec.")

arg_parser.add_argument("input_path",
                        metavar = "input-path",
                        type = str,
                        help = "Path to the model file.")

arg_parser.add_argument("rule_to_check",
                        metavar = "rule-to-check",
                        type = int,
                        help = "The rule that should be checked. Options are: 1 through 25 (Check microSecFixer/docs/rules_ordered.md for what each rule is)")

arg_parser.add_argument("-op",
                        metavar = "--output-path",
                        type = str,
                        help = "Path where output file should be stored.")


def get_model(model_path: str) -> CModel:
    return model_api(model_path, None)

def visualize_dfd(dfd_path: str, out_type: str, out_path: str):
    visualizer.visualize(dfd_path, out_type, out_path)

def insertConfigIntoTemp(config: ConfigParser):
    logger.write_log_message("Copying config file to tmp file", "debug")
    #copying what is needed from config to temp
    for section in ["Repository", "Technology Profiles", "Analysis Settings", "DFD"]:
        if not temp.tmp_config.has_section(section):
            temp.tmp_config.add_section(section)
        for entry in config[section]:
            temp.tmp_config.set(section, entry, config[section][entry])

def fix_one(dfd_path: str, rule_to_check: int,  output_path: str):
    visualize_dfd(dfd_path, "original", output_path)

    result_dir, verdict = find_violation(dfd_path, rule_to_check, output_path)
    if verdict:
        print("The rule is already adhered to by the provided model.")
        visualize_dfd(dfd_path, "ideal", output_path)
        return
    
    results = os.listdir(result_dir)
    fixing_map = RuleMap.get_fixes()
    model_path = dfd_path
    rule = results[0][:3]
    dfd_path = fixing_map[rule](get_model(model_path), output_path)

    result_dir, verdict = find_violation(dfd_path, rule_to_check, output_path)
    if not verdict:
        print("Something went horribly wrong.")
        return
    
    



def fix_all(dfd_path: str, output_path: str):
    visualize_dfd(dfd_path, "original", output_path)

    # calling microCertiSec to evaluate the security of the model and saving the results under output/results/{model name}
    result_dir = find_all_violations(dfd_path, output_path)
    results = os.listdir(result_dir)
    fixing_map = RuleMap.get_fixes()
    while(results):
        model_path = dfd_path
        rule = results[0][:3]
        dfd_path = fixing_map[rule](get_model(model_path), output_path)
        result_dir = find_all_violations(dfd_path, output_path)
        results = os.listdir(result_dir)

    visualize_dfd(dfd_path, "ideal", output_path) 

def main(args):
    now = datetime.now()
    start_time = now.strftime("%H:%M:%S")
    logger.write_log_message("*** New execution ***", "info")
    print("\nStarted", start_time)

    arguments = arg_parser.parse_args(args)

    if arguments.input_path:
        dfd_path = arguments.input_path
    else:
        ini_config = ConfigParser()
        ini_config.read('config/config.ini')
        insertConfigIntoTemp(ini_config)
        dfd_path = temp.tmp_config.get("Repository", "dfd_path")

    if arguments.op:
        output_path = arguments.op
    else:
        output_path = "./output/"

    if arguments.rule_to_check:
        fix_one(dfd_path, arguments.rule_to_check, output_path)
    else:
        fix_all(dfd_path, output_path)
    

    now = datetime.now()
    end_time = now.strftime("%H:%M:%S")

    print("Finished", end_time)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])