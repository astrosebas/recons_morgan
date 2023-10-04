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

from utilities.fits_handling import get_achi_scihdr

# ==========================================================================
# Functions related to SNR calculations
# ==========================================================================


## eq.1 Toko et al. 2013
def SNR_at_order(wav,bfcont,mode,spectrum,name,plot=False):
    print("mode:", mode)
    
    # read-out noise
    R = 5.5 
    # K is number of binned pixels
    K = {'fiber':2.5,'slicer':9.} 

    # mid third of the order, where the blaze max should be
    midthird = range(int(len(bfcont)/3),int((len(bfcont)*2)/3)) 
    wav_mid = wav[midthird]
    bfcont_mid = bfcont[midthird]

    #3 pix centered in the max intensity of order
    pix3center = range(np.argmax(bfcont_mid)-1,np.argmax(bfcont_mid)+2)
    wav3pix = wav_mid[pix3center]
    #print('pix3center:', pix3center, 'Nph3pix:', wav3pix,'wav3pix:')

    # The intensity of the 3 pixels
    Nph3pix = bfcont_mid[pix3center] 
    Nph = np.mean(Nph3pix)
    SNR = Nph / np.sqrt(Nph + K[mode] * R**2)
    #print('Nph3pix:', Nph3pix,'Nph:', Nph, 'SNR:', SNR)
   
    #if plot == True:
    #    plot_SN(name,SNR,wav,spectrum,bfcont,wav_mid,bfcont_mid,wav3pix,Nph3pix)
    
    return SNR,wav3pix,Nph3pix


# S/N exposure meter - Paredes et al. 2021
def SNREM_fits(fitsfile_fp):
    hdr = get_achi_scihdr(fitsfile_fp)
    if 'EMAVG' in hdr: 
        emavg = float(hdr['EMAVG'])
        emnumsmp = float(hdr['EMNUMSMP'])
        emthresh = emavg*emnumsmp
        snr_em = np.sqrt((emthresh - 7401.973)/57.909)
    else:
        snr_em = 0.0
        
    return snr_em

def SNREM_value(emavg, emnumsmp):
    
    emavg.astype({'emavg': 'float64'}).dtypes
    emnumsmp.astype({'emnumsmp': 'float64'}).dtypes
    #emavg, emnumsmp = float(emavg), float(emnumsmp)
    
    log.info(f'============ SNR EM Calculation ============')
    #print(type(emavg), type(emavg))
    #print(emavg.dtypes, emavg.dtypes)

    #print(emavg, emnumsmp)

    snr_em_list = []
    
    for emavg_, emnumsmp_ in zip(emavg, emnumsmp):

        if emavg_ == 0.0: 
            snr_em = '0.0'
            snr_em_list.append(snr_em)

        elif emnumsmp_ == 0.0:
            snr_em = '0.0'
            snr_em_list.append(snr_em)

        else:
            emthresh = float(emavg_)*float(emnumsmp_)
            snr_em = np.sqrt((float(emthresh) - 7401.973)/57.909)
            snr_em_list.append(snr_em)

    return snr_em_list