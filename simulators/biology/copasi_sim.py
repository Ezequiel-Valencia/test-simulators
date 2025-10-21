import os
import tempfile

import basico
import pandas as pd
import requests


omex_url = "https://ftp.ebi.ac.uk/pub/databases/biomodels/repository/aaa/MODEL6615351360/3/MODEL6615351360.3.omex"

with tempfile.TemporaryDirectory() as tmpDir:

    basico.load_model_from_url(omex_url)
    data_frame: pd.DataFrame = basico.run_time_course()
    data_frame.to_csv(".results/copasi_sim.csv")




