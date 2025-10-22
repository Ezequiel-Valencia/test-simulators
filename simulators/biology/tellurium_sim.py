import os
import tempfile
import zipfile

import pandas as pd
import requests
import tellurium as te
from roadrunner.roadrunner import RoadRunner
from biosimulators_utils.sedml.io import SedmlSimulationReader
from biosimulators_utils.sedml.data_model import SedDocument, Simulation


# Elowitz2000 - Repressilator Model, https://www.ebi.ac.uk/biomodels/BIOMD0000000012
omex_url = "https://ftp.ebi.ac.uk/pub/databases/biomodels/repository/aaa/MODEL6615351360/3/MODEL6615351360.3.omex"


def _download_and_extract_omex(tmpdir: str):
    response = requests.get(omex_url, stream=True)
    response.raise_for_status()
    omex_file = os.path.join(tmpdir, "repressilator.omex")
    with open(omex_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8024):
            f.write(chunk)
    zipfile.ZipFile(omex_file).extractall(tmpdir)


def sbml_test():
    with tempfile.TemporaryDirectory() as tmpdir:
        _download_and_extract_omex(tmpdir)
        sbml_path = os.path.join(tmpdir, "BIOMD0000000012_url.xml")

        # te.executeSEDML(inputStr=sedML)
        runner: RoadRunner = te.loadSBMLModel(sbml_path)
        results_save_dir = os.path.dirname(__file__) + "/.results"
        if not os.path.exists(results_save_dir):
            os.mkdir(results_save_dir)
        results_file = results_save_dir + "/repressilator.csv"
        runner.simulate(start=0, end=10, points=51, output_file=results_file)


def sedml_test():
    with tempfile.TemporaryDirectory() as tmpdir:
        _download_and_extract_omex(tmpdir)
        with open(os.path.join(tmpdir, "BIOMD0000000012_url.sedml"), "r") as f:
            sedml_string = f.read()

            # Needed because Omex uses relative pathing
            cur_dir = os.getcwd()
            os.chdir(tmpdir)
            te.executeSEDML(inputStr=sedml_string, outputDir=f"{cur_dir}/.results")
            os.chdir(cur_dir)


def sedml_parse_test():
    with tempfile.TemporaryDirectory() as tmpdir:
        _download_and_extract_omex(tmpdir)
        sedml_path = os.path.join(tmpdir, "BIOMD0000000012_url.sedml")
        sbml_path = os.path.join(tmpdir, "BIOMD0000000012_urn.xml")
        reader = SedmlSimulationReader()
        reader: SedmlSimulationReader
        doc: SedDocument = reader.run(filename=sedml_path)
        time_course = doc.simulations[0]

        runner: RoadRunner = te.loadSBMLModel(sbml=sbml_path)
        runner.simulate(start=time_course.output_start_time, end=time_course.output_end_time,
                        points=time_course.number_of_points, output_file=".results/tellurium_sedml_parse.csv")


sedml_parse_test()

