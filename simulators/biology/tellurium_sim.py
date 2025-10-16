import os
import tempfile
import zipfile

import pandas as pd
import requests
import tellurium as te
from roadrunner.roadrunner import RoadRunner


# Elowitz2000 - Repressilator Model, https://www.ebi.ac.uk/biomodels/BIOMD0000000012
omex_url = "https://ftp.ebi.ac.uk/pub/databases/biomodels/repository/aaa/MODEL6615351360/3/MODEL6615351360.3.omex"

with tempfile.TemporaryDirectory() as tmpdir:
    request = requests.Request(method="GET", url=omex_url)
    response = requests.get(omex_url, stream=True)
    response.raise_for_status()
    omex_file = os.path.join(tmpdir, "repressilator.omex")
    with open(omex_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8024):
            f.write(chunk)
    zipfile.ZipFile(omex_file).extractall(tmpdir)
    sbml_path = os.path.join(tmpdir, "BIOMD0000000012_url.xml")

    # te.executeSEDML(inputStr=sedML)
    runner: RoadRunner = te.loadSBMLModel(sbml_path)
    results_save_dir = os.path.dirname(__file__) + "/.results"
    if not os.path.exists(results_save_dir):
        os.mkdir(results_save_dir)
    results_file = results_save_dir + "/repressilator.csv"
    results = runner.simulate(start=0, end=10, points=51, output_file=results_file)

