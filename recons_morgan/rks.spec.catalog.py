#############################################################



#############################################################

import sys, argparse, logging
import os
import pathlib
import glob

import numpy as np
import pandas as pd

from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord

from utilities.terminal_log import (log,
                                degree_to_dms,
                                degree_to_hms,
                                degree_to_mas,
                                )

from utilities.config import config_data
from science.spec_retreiver import rks_catalog


# PATHS
## Public reduced data
data_pub = 'ftp/pub/SMARTS'
## Already reduced data from pipepline
data_piped = "/nfs/morgan/chiron/tous/mir7/fitspec"
## Sample
sample = 'samples/'
# RKS masterlist
#masterlist = pd.read_csv(sample+'RKScatalog50pc_all.csv')

## FUNCTIONS



def main(): 
    
    # directory
    out_dir = "paths_sp/"
    out_name = out_dir + 'rks_catalog.f_20231002'
    p = pathlib.Path('.')

    # Creating directorys
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    parser = argparse.ArgumentParser(description='Search for Paths')

    parser.add_argument("-p",
                        "--pipeline",
                        action='store_true',
                        help='run analysis and reporting as when running the pipeline',
                        default=False)

    args = parser.parse_args()

    dataset_root = config_data['dataset_root']
    working_dir = pathlib.Path(dataset_root) 
    print(working_dir)
    log.init_global(working_dir)

    if args.pipeline:
        log.warn("Failed.")
    else:
        #RKS_spec(dataset_root,out_name)
        log.info(f'Spectra root in {dataset_root}')
        rks_catalog(dataset_root,out_name)
        log.info("RKS spectra found.")

if __name__ == '__main__':

     main()
