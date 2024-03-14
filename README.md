## microSecFixer

This is microSecFixer, a tool used to automatically fix security rule violations on the architectural model of a Microservice application.

microSecFixer builds on top of the groundwork laid by Simon Schneider. It 

The tool and underlying approach are presented in a publication in the Journal of Systems and Software (JSS). You can find the paper on arXiv or the publisher's website. If you use the tool in a scientific context, please cite as:

@article{Code2DFD23,
  title = {Automatic Extraction of Security-Rich Dataflow Diagrams for Microservice Applications written in Java},
  journal = {Journal of Systems and Software},
  volume = {202},
  pages = {111722},
  year = {2023},
  issn = {0164-1212},
  doi = {https://doi.org/10.1016/j.jss.2023.111722},
  author = {Simon Schneider and Riccardo Scandariato},
  keywords = {Dataflow diagram, Automatic extraction, Security, Microservices, Architecture reconstruction, Feature detection}
}

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
- The results of the security analysis are saved in `output/result`