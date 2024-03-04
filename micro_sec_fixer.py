#!/usr/bin/env python3
#
# Author: Dominik Jacob, 2024
# Contact: dominik.jacob@tuhh.de

import sys
import os
from configparser import ConfigParser
from datetime import datetime

import core.logger as logger
import tmp.tmp as tmp
import core.file_handler as fh


def main():
    now = datetime.now()
    start_time = now.strftime("%H:%M:%S")

    logger.write_log_message("*** New execution ***", "info")
    logger.write_log_message("Copying config file to tmp file", "debug")

    # Copy config to tmp file
    ini_config = ConfigParser()
    ini_config.read('config/config.ini')
    #copying what is needed from config to temp
    for section in ["Analysis Settings", "Repository", "Technology Profiles", "DFD"]:
        if not tmp.tmp_config.has_section(section):
            tmp.tmp_config.add_section(section)
        for entry in ini_config[section]:
            tmp.tmp_config.set(section, entry, ini_config[section][entry])
    arguments = sys.argv
    invocation_command = "python3"
    for argument in arguments:
        invocation_command += " " + argument
    tmp.tmp_config.set("Repository", "invocation_command", invocation_command)

    if len(arguments) == 1:
        repo_path = tmp.tmp_config["Repository"]["path"]
        print("No repository given as parameter. \
                \n   You can provide the path as: > python3 code2dfd.py repository/path \
                \nAnalysing " + repo_path + " as specified in config/config.ini")
    elif len(arguments) == 2:
        repo_path = arguments[1]
        tmp.tmp_config.set("Repository", "path", repo_path)
    elif len(arguments) >2:
        print("Please specify the repository paths one by one.")
        return

    # Create analysed_repositories folder in case it doesn't exist yet (issue #2)
    os.makedirs(os.path.dirname("./analysed_repositories"), exist_ok=True)

    local_path = "./analysed_repositories/" + ("/").join(repo_path.split("/")[1:])
    tmp.tmp_config.set("Repository", "local_path", local_path)
    
    if not fh.is_repo_downloaded(local_path):
        fh.download_repo(repo_path)

    # calling the actual extraction
    #dfd_extraction.perform_analysis()

    now = datetime.now()
    end_time = now.strftime("%H:%M:%S")

    print("\nStarted", start_time)
    print("Finished", end_time)