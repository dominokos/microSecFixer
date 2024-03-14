#!/usr/bin/env python3
#
# Author: Dominik Jacob, 2024
# Contact: dominik.jacob@tuhh.de

import json
from configparser import ConfigParser
from datetime import datetime
from microCertiSec import microCertiSec

import core.logger as logger
import tmp.tmp as tmp


def main():
    now = datetime.now()
    start_time = now.strftime("%H:%M:%S")

    logger.write_log_message("*** New execution ***", "info")
    logger.write_log_message("Copying config file to tmp file", "debug")

    # Copy config to tmp file
    ini_config = ConfigParser()
    ini_config.read('config/config.ini')
    #copying what is needed from config to temp
    for section in ["Repository", "Technology Profiles", "Analysis Settings", "DFD"]:
        if not tmp.tmp_config.has_section(section):
            tmp.tmp_config.add_section(section)
        for entry in ini_config[section]:
            tmp.tmp_config.set(section, entry, ini_config[section][entry])

    dfd_path = tmp.tmp_config.get("Repository", "dfd_path")
    repo_name = dfd_path.split("models/")[1] 

    model_path = "." + dfd_path
    traceability_path = model_path.replace(".json", "") + "_traceability.json"

    # calling microCertiSec to evaluate the security of the model and collecting the results
    result = microCertiSec.microCertiSec_API(model_path, traceability_path, "r01")
    with open(f"./output/{repo_name}", "w") as output_file:
        json.dump(result.property_check_evidence_json, output_file)


    print(json.dumps(result.property_check_evidence_json, indent=4))

    now = datetime.now()
    end_time = now.strftime("%H:%M:%S")

    print("\nStarted", start_time)
    print("Finished", end_time)


if __name__ == '__main__':
    main()