## microSecFixer

This is microSecFixer, a tool used to automatically fix security rule violations on the architectural model of a Microservice application.

microSecFixer builds on top of the groundwork laid by Simon Schneider. It evaluates using microCertiSec, whether a given Dataflow Diagram - representing an application with a Microservice architecture - violates any of a set of 25 security rules. The security rules are based on best practice recommendations by OWASP, NIST, and CSA. At the core, it evaluates what parts of the Dataflow model are faulty and automatically corrects said flaws.

### 1. Installation

#### Prerequisites
- [Python](https://www.python.org/downloads/): Ensure you have Python version 3.x installed. You can download it from the official website.
- [Java Runtime Environment (JRE)](https://www.java.com/de/download/manual.jsp): Ensure you have JRE installed (necessary for rendering PlantUML).
- [Git](https://git-scm.com/downloads): Ensure you have Git installed.
- [pip](https://pip.pypa.io/en/stable/cli/pip_download/): Ensure you have pip installed.

#### Setup
1. Make sure to clone the repository using git into your local working directory.
2. Run `pip install -r requirements.txt` to install all required libraries.
3. The path to the application that is to be analyzed has to be written in the `config/config.ini` file.
    - A number of repositories is already given in that file, for all of which manually created DFDs exist [here](https://github.com/tuhh-softsec/microSecEnD). The corresponding path only needs to be uncommented for analysis (all others have to be commented out with a ";").

### 2. Running the tool

To start the tool via the terminal, simply enter `python ./microSecFixer/microsecfixer.py` in a command line opened in the root directory. The extraction will start, and some status messages will appear on the terminal. Once the analysis is finished, the results can be found in the `output/` folder.

### 3. Output

The tool creates multiple outputs:

- The DFD is converted into [PlantUML](https://plantuml.com) and stored in `output/plantuml/{model_name}` as pure PlantUML text and as an SVG file.
    - PlantUML can be converted into .png as needed, using the command `java -jar plantuml.jar -tpng "Path/To/file.txt"`.
- A machine-readable version of the improved DFD is stored in JSON format under `output/json/{model_name}`.
- Logs are saved in `output/logs/`.
- The results of the security analysis are saved in `output/results/{model_name}`.
