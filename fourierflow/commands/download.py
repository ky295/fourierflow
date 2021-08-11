import os

import gdown
import typer

app = typer.Typer()


@app.command()
def fno():
    """Download some google datasets.

    Copied from a shell script:

    mkdir data/fourier && cd data/fourier
    gdown --id 16a8od4vidbiNR3WtaBPCSZ0T3moxjhYe # Burgers_R10.zip
    gdown --id 1nzT0-Tu-LS2SoMUCcmO1qyjQd6WC9OdJ # Burgers_v100.zip
    gdown --id 1G9IW_2shmfgprPYISYt_YS8xa87p4atu # Burgers_v1000.zip
    gdown --id 1ViDqN7nc_VCnMackiXv_d7CHZANAFKzV # Darcy_241.zip
    gdown --id 1Z1uxG9R8AdAGJprG5STcphysjm56_0Jf # Darcy_421.zip
    gdown --id 1r3idxpsHa21ijhlu3QQ1hVuXcqnBTO7d # NavierStokes_V1e-3_N5000_T50.zip
    gdown --id 1pr_Up54tNADCGhF8WLvmyTfKlCD5eEkI # NavierStokes_V1e-4_N20_T50_R256_test.zip
    gdown --id 1RmDQQ-lNdAceLXrTGY_5ErvtINIXnpl3 # NavierStokes_V1e-4_N10000_T30.zip
    gdown --id 1lVgpWMjv9Z6LEv3eZQ_Qgj54lYeqnGl5 # NavierStokes_V1e-5_N1200_T20.zip
    unzip *.zip && rm -rf *.zip
    """
    fno_datasets = {
        "16a8od4vidbiNR3WtaBPCSZ0T3moxjhYe": "Burgers_R10.zip",
        "1nzT0-Tu-LS2SoMUCcmO1qyjQd6WC9OdJ": "Burgers_v100.zip",
        "1G9IW_2shmfgprPYISYt_YS8xa87p4atu": "Burgers_v1000.zip",
        "1ViDqN7nc_VCnMackiXv_d7CHZANAFKzV": "Darcy_241.zip",
        "1Z1uxG9R8AdAGJprG5STcphysjm56_0Jf": "Darcy_421.zip",
        "1r3idxpsHa21ijhlu3QQ1hVuXcqnBTO7d": "NavierStokes_V1e-3_N5000_T50.zip",
        "1pr_Up54tNADCGhF8WLvmyTfKlCD5eEkI": "NavierStokes_V1e-4_N20_T50_R256_test.zip",
        "1RmDQQ-lNdAceLXrTGY_5ErvtINIXnpl3": "NavierStokes_V1e-4_N10000_T30.zip",
        "1lVgpWMjv9Z6LEv3eZQ_Qgj54lYeqnGl5": "NavierStokes_V1e-5_N1200_T20.zip",
    }

    startdir = os.getcwd()
    workdir = os.path.expandvars('$FNO_DATA_ROOT')
    os.makedirs(workdir, exist_ok=True)
    try:
        os.chdir(workdir)
        for shareid, fname in fno_datasets.items():
            # This is slightly faster with cached_download but CSIRO HPC hates
            # the massive cache folder.
            gdown.download(f'https://drive.google.com/uc?id={shareid}', fname)
            gdown.extractall(fname)
            os.unlink(fname)
    finally:
        os.chdir(startdir)


if __name__ == "__main__":
    app()