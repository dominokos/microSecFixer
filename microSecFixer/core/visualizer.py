import os
import subprocess

from microSecFixer.core import convert_model


"""Renders PlantUML as svg
"""
def get_model_name(dfd_path: str) -> str:
    no_file_ending = dfd_path.split(".")[0]
    model_name = no_file_ending.partition("models/")[2]
    return model_name

def get_full_path(dfd_path: str) -> str:
    current_wd = os.getcwd()
    return current_wd + dfd_path

def gen_plantuml(full_path: str, model_name: str):
    plantuml_directory = f"./output/plantuml/{model_name}/"
    os.makedirs(plantuml_directory, exist_ok=True)
    plantuml_filepath = f"{plantuml_directory}{model_name}.txt"
    convert_model.main(["-op", plantuml_filepath, full_path, "txt"])

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
