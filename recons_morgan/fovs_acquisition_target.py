import sys, argparse, logging
import os
import pathlib
import glob

import numpy as np
import pandas as pd

from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord

from prince.config import config_data
from prince.utils.report_and_log import (StatusId, LogLevel,
                                    log,
                                    register_to_logger,
                                    degree_to_dms,
                                    degree_to_hms,
                                    degree_to_mas,
                                    escape_underscore)


# Funcion change hour angles to degree
def hr_to_deg(ra,dec):
    
    RA_fields =  ra
    DEC_fields =  dec
    coords_str = str(RA_fields)+' '+str(DEC_fields)
    
    c = SkyCoord(coords_str, unit=(u.hourangle, u.deg))
    RA_ = c.ra / u.deg
    DEC_ = c.dec / u.deg
        
    return RA_,DEC_


# Funtion to import coordinates from stacked mediants FITS
def fov_coords(dataset_root,out_name):
    # Creates a list with the name of all the folders
    datasets = [dI for dI in os.listdir(dataset_root) if os.path.isdir(os.path.join(dataset_root,dI))]
    log.info('Datasets retrieved')

    # Creates a list with the paths to the best_LC files.    
    path_median_ = []
    
    for dataset in datasets:
        filename = (pathlib.Path(dataset_root) / dataset / "Median" ).glob("*_stacked_median.fits")
        path_median_.extend(filename)
    
    # The list would have blank elements, so this remove blank elements    
    path_median = list(filter(None, path_median_))
    log.info('List of paths to stacked_median.fits complete')

    RA = []
    DEC = []
    EXPTIME = []
    ACQ_TARGET = []
    DATE = []
    
    for path in path_median:
        
        path_ = str(path)
        a = path_.split("/")
        
        dataset = a[9]
        
        acq_tgt_ = a[11].split("_")
        acq_tgt = acq_tgt_[0]
        
        # Importing the FOV's center coordinates
        acq_median = fits.open(path)
        hdu = acq_median['PRIMARY'].header
               
        # Check for keywords existence
        if 'RA' and 'DEC' in hdu:  
            hdu_RA, hdu_DEC = hr_to_deg(hdu['RA'],hdu['DEC'])
            RA.append(hdu_RA)
            DEC.append(hdu_DEC)
            
            DATE.append(dataset)
            ACQ_TARGET.append(acq_tgt)
            
            if 'EXPTIME' in hdu: 
                EXPTIME.append(hdu['EXPTIME'])
                
            else:
                EXPTIME.append(None)
                log.warn('EXPTIME keyword not found from: {}'.format(path))
                pass
            
            #if 'OBJECT' in hdu:
            #    ACQ_TARGET.append(hdu['OBJECT']) 
            #    
            #else:
            #    ACQ_TARGET.append(None)
            #    ACQ_TARGET.warn('OBJECT keyword not found from: {}'.format(path))
            #    pass
            
        elif 'CRVAL1' and 'CRVAL2' in hdu:
            # CRVAL1: RA of reference point
            RA.append(hdu['CRVAL1'])
            # CRVAL2: DEC of reference point
            DEC.append(hdu['CRVAL2'])
            
            DATE.append(dataset)
            ACQ_TARGET.append(acq_tgt)
            
            if 'EXPTIME' in hdu: #'DATE' in hdu:
                EXPTIME.append(hdu['EXPTIME'])
                
            else:
                EXPTIME.append(None)
                log.warn('EXPTIME keyword not found from: {}'.format(path))
                pass
            
            #if 'OBJECT' in hdu:
            #    ACQ_TARGET.append(hdu['OBJECT']) 
            #    
            #else:
            #    ACQ_TARGET.append(None)
            #    ACQ_TARGET.warn('OBJECT keyword not found from: {}'.format(path))
            #    pass
            
            log.warn('RA and DEC keywords not found.')
            log.info('CRVAL1 and CRVAL2 keywords used instead.')
                      
        else:
            log.warn('Coordinates were unable to retreive from: {}'.format(path))
            pass             
        
    coords_ = pd.DataFrame(columns=["RA", "DEC", "EXPTIME", "DATE","ACQ_TARGET"])
        
    coords_["RA"] = RA
    coords_["DEC"] = DEC
    coords_["EXPTIME"] = EXPTIME    
    coords_["DATE"] = DATE
    coords_["ACQ_TARGET"] = ACQ_TARGET
                         
    coords = coords_.drop_duplicates(subset=["RA","DEC"], keep='first')
        
    coords.to_csv(out_name , sep=",", index=False)
    log.info('FOV\'s center coordinates list done')

    
def main(): 
    
    # directory
    out_dir = "targetlist/seb_test/"
    out_name = out_dir + 'fovs_acq_targets.txt'

    # Creating directory
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    parser = argparse.ArgumentParser(description='Search for FOVs')

    parser.add_argument("-p",
                        "--pipeline",
                        action='store_true',
                        help='run analysis and reporting as when running the pipeline',
                        default=False)

    args = parser.parse_args()

    dataset_root = config_data['dataset_root']
    working_dir = pathlib.Path(dataset_root) 

    log.init_global(working_dir)

    if args.pipeline:
        log.warn("Failed.")
    else:
        fov_coords(dataset_root,out_name)
        log.info("FOVs retreived.")

if __name__ == '__main__':

     main()

