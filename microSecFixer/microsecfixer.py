#!/usr/bin/env python3
#
# Author: Dominik Jacob, 2024
# Contact: dominik.jacob@tuhh.de

from configparser import ConfigParser
from datetime import datetime
from microSecFixer.core.evaluation import find_all_violations

import microSecFixer.core.logger as logger
import tmp.tmp as temp


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


    now = datetime.now()
    end_time = now.strftime("%H:%M:%S")

    print("\nStarted", start_time)
    print("Finished", end_time)


def insertConfigIntoTemp(config: ConfigParser):
    logger.write_log_message("Copying config file to tmp file", "debug")
    #copying what is needed from config to temp
    for section in ["Repository", "Technology Profiles", "Analysis Settings", "DFD"]:
        if not temp.tmp_config.has_section(section):
            temp.tmp_config.add_section(section)
        for entry in config[section]:
            temp.tmp_config.set(section, entry, config[section][entry])
    


if __name__ == '__main__':
    main()