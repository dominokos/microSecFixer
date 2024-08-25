#!/usr/bin/env python3
#
# Author: Dominik Jacob, 2024
# Contact: dominik.jacob@tuhh.de

import os
from configparser import ConfigParser
from datetime import datetime

from microSecFixer.core.evaluation import find_all_violations
import microSecFixer.core.logger as logger
import microSecFixer.tmp.tmp as temp
import microSecFixer.core.convert_model as convert_model


def get_model_name(dfd_path: str) -> str:
    no_file_ending = dfd_path.split(".")[0]
    model_name = no_file_ending.partition("models/")[2]
    return model_name

def get_full_path(dfd_path):
    current_wd = os.getcwd()
    return current_wd + dfd_path

def gen_plantuml(full_path: str, model_name: str):
    plantuml_directory = "./output/plantuml/"
    os.makedirs(plantuml_directory, exist_ok=True)
    convert_model.main(["-op", "output/plantuml/"+model_name+".txt", full_path, "txt"])

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

    # calling microCertiSec to evaluate the security of the model and saving the results under output/results
    find_all_violations(dfd_path)
    model_name = get_model_name(dfd_path)
    full_path = get_full_path(dfd_path)
    gen_plantuml(full_path, model_name)


    now = datetime.now()
    end_time = now.strftime("%H:%M:%S")

    print("\nStarted", start_time)
    print("Finished", end_time)

if __name__ == '__main__':
    main()