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
from microSecFixer.core.evaluation import find_next_violation, find_violation, find_all_violations
import microSecFixer.core.logger as logger
from microSecFixer.core.rule_map import RuleMap
import microSecFixer.tmp.tmp as temp
from microCertiSec.microCertiSec import model_api

# For CLI
arg_parser = argparse.ArgumentParser(prog = "microSecFixer",
                                    description = "Takes a architectural model in JSON format and generates an \"ideal\" model which fulfills the rules introduced in microCertiSec.")

arg_parser.add_argument("-rtc",
                        metavar = "--rule-to-check",
                        type = int,
                        help = "The rule that should be checked. Options are: 1 through 25 (Check microSecFixer/docs/rules_ordered.md for what each rule is)")

arg_parser.add_argument("-so",
                        metavar = "--store-original",
                        help = "Store the results of the original analysis")


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

    rule, verdict = find_violation(dfd_path, rule_to_check, output_path)
    if verdict:
        print("The rule is already adhered to by the provided model.")
        visualize_dfd(dfd_path, "ideal", output_path)
        return
    
    fixing_map = RuleMap.get_fixes()
    dfd_path = fixing_map[rule](get_model(dfd_path), output_path)
    
    visualize_dfd(dfd_path, "ideal", output_path)
    rule, verdict = find_violation(dfd_path, rule_to_check, output_path)
    if not verdict:
        raise Exception("Something went wrong. We couldn't fix your model.")

def fix_all(dfd_path: str, output_path: str):
    visualize_dfd(dfd_path, "original", output_path)

    # calling microCertiSec to evaluate the security of the model and saving the results under ./output/results/{model name}
    rule_to_fix = find_next_violation(dfd_path, output_path)
    fixing_map = RuleMap.get_fixes()
    while(rule_to_fix != None):
        fixed_until = int(rule_to_fix[1:])
        dfd_path = fixing_map[rule_to_fix](get_model(dfd_path), output_path)
        rule_to_fix = find_next_violation(dfd_path, output_path, fixed_until)

    visualize_dfd(dfd_path, "ideal", output_path) 
    final_check = find_next_violation(dfd_path, output_path)
    if final_check != None:
        raise Exception("Something went wrong. We couldn't fix your model.")

def main(args):
    now = datetime.now()
    start_time = now.strftime("%H:%M:%S")
    
    logger.write_log_message("*** New execution ***", "info")
    print("Started", start_time)

    output_path = "./output/"

    ini_config = ConfigParser()
    ini_config.read('config/config.ini')
    insertConfigIntoTemp(ini_config)
    dfd_path = f".{temp.tmp_config.get("Repository", "dfd_path")}"

    arguments = arg_parser.parse_args(args)

    if arguments.so:
        find_all_violations(dfd_path, output_path)

    if arguments.rtc:
        fix_one(dfd_path, arguments.rtc, output_path)
    else:
        fix_all(dfd_path, output_path)

    now = datetime.now()
    end_time = now.strftime("%H:%M:%S")

    print("Finished", end_time)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])