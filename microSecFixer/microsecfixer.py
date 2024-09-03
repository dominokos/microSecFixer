#!/usr/bin/env python3
#
# Author: Dominik Jacob, 2024
# Contact: dominik.jacob@tuhh.de

import os
from configparser import ConfigParser
from datetime import datetime

from microCertiSec.core.model import CModel
import microSecFixer.core.visualizer as visualizer
from microSecFixer.core.evaluation import find_all_violations_between
import microSecFixer.core.logger as logger
from microSecFixer.core.rule_map import RuleMap
import microSecFixer.tmp.tmp as temp
from microCertiSec.microCertiSec import model_api

def get_model(model_path: str) -> CModel:
    return model_api(model_path, None)

def visualize_dfd(dfd_path: str, out_location: str):
    visualizer.visualize(dfd_path, out_location)

def insertConfigIntoTemp(config: ConfigParser):
    logger.write_log_message("Copying config file to tmp file", "debug")
    #copying what is needed from config to temp
    for section in ["Repository", "Technology Profiles", "Analysis Settings", "DFD"]:
        if not temp.tmp_config.has_section(section):
            temp.tmp_config.add_section(section)
        for entry in config[section]:
            temp.tmp_config.set(section, entry, config[section][entry])
    

def main():
    now = datetime.now()
    start_time = now.strftime("%H:%M:%S")

    logger.write_log_message("*** New execution ***", "info")
    
    ini_config = ConfigParser()
    ini_config.read('config/config.ini')
    insertConfigIntoTemp(ini_config)

    dfd_path = temp.tmp_config.get("Repository", "dfd_path")
    visualize_dfd(dfd_path, "original")

    # calling microCertiSec to evaluate the security of the model and saving the results under output/results/{model name}
    result_dir = find_all_violations_between(dfd_path, 1, 26)
    results = os.listdir(result_dir)
    fixing_map = RuleMap.get_fixes()
    while(results):
        model_path = f".{dfd_path}"
        rule = results[0][:3]
        dfd_path = fixing_map[rule](get_model(model_path))
        rule_number = int(rule[-2:])
        upper_bound = 26
        if len(results) > 1:
            next_failing_rule = results[1][:3]
            upper_bound = min(26, int(next_failing_rule[-2:])+2)
        result_dir = find_all_violations_between(dfd_path, rule_number, upper_bound)
        results = os.listdir(result_dir)

    visualize_dfd(dfd_path, "ideal")
    now = datetime.now()
    end_time = now.strftime("%H:%M:%S")

    print("\nStarted", start_time)
    print("Finished", end_time)

if __name__ == '__main__':
    main()