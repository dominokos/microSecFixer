import os
import subprocess
import plantuml

from microSecFixer.core import convert_model


"""Renders PlantUML as svg
"""

def visualize(dfd_path: str, out_type: str, out_path: str):
    model_name = get_model_name(dfd_path)
    full_path = get_full_path(dfd_path)
    plantuml_filepath = gen_plantuml(full_path, model_name, out_type, out_path)
    output_svg(plantuml_filepath)
    output_png(plantuml_filepath)

def get_model_name(dfd_path: str) -> str:
    no_file_ending = dfd_path.split(".json")[0]
    model_name = no_file_ending.partition("models/")[2]
    return model_name

def get_full_path(dfd_path: str) -> str:
    current_wd = os.getcwd()
    return current_wd + dfd_path

def gen_plantuml(full_path: str, model_name: str, out_type: str, out_path: str) -> str:
    plantuml_directory = f"{out_path}plantuml/{model_name}/{out_type}/"
    os.makedirs(plantuml_directory, exist_ok=True)
    plantuml_filepath = f"{plantuml_directory}{model_name}.txt"
    convert_model.main(["-op", plantuml_filepath, full_path, "txt"])
    return plantuml_filepath

def output_svg(plantuml_filepath: str):
    """Renders PlantUML in SVG format."""
    try:
        subprocess.run(["java", "-jar", "plantuml.jar", "-tsvg", plantuml_filepath], check=True, timeout=30)
    except subprocess.TimeoutExpired:
        print("The command timed out.")
    except subprocess.CalledProcessError as e:
        print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
    except FileNotFoundError:
        print("The specified file or directory was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
def output_png(plantuml_filepath: str):
    """
    Converts CodeableModels output into different PlantUML graphics and renders it as PNG.
    """
    generator = plantuml.PlantUML(url = "http://www.plantuml.com/plantuml/img/")
    try:
        generator.processes_file(filename = plantuml_filepath, outfile = plantuml_filepath.replace("plantuml_source", "png").replace("txt", "png"))
    except Exception:
        print("No connection to the PlantUML server possible or malformed input to the server.")