## microSecFixer

This is microSecFixer, a tool used to automatically fix security rule violations on the architectural model of a Microservice application.

microSecFixer builds on top of the groundwork laid by Simon Schneider. It evaluates using microCertiSec, whether a given Dataflow Diagram - representing an application with a Microservice architecture - violates any of a set of 25 security rules. The security rules are based on best practice recommendations by OWASP, NIST and CSA. At the core, it evaluates what parts of the Dataflow model are faulty and automatically corrects said flaws.

##### 1. Installation and configuration
Before running the tool, [Python](https://www.python.org/downloads/) version 3.x needs to be installed.
The path to the application that is to be analysed can be written in the `config/config.ini` file.
A number of repositories is already given in that file, for all of which a manually created DFD exists [here](https://github.com/tuhh-softsec/microSecEnD).
The corresponding path only needs to be un-commented for analysis (all others have to be commented out with a ";")

##### 2. Running the tool
To start the tool via the terminal, simply enter `python3 microSecFixer.py` in a command line opened in the root directory.
The extraction will start and some status messages appear on the screen.
Once the analysis is finished, the results can be found in the `output/` folder.

##### 3. Output
The tool creates multiple outputs:
- The extracted DFD is saved as a .png rendered with [PlantUML](https://plantuml.com) in `output/png/`.
An internet connection is needed for this, otherwise no PNG will be created.
- A machine-readable version of the DFD is created in JSON format in `output/json/`
- Logs are saved in `output/logs/`
- The results of the security analysis are saved in `output/results/`