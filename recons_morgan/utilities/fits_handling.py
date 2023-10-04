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


# ==========================================================================
# Functions to manage FITS files
# ==========================================================================


def get_achi_scihdr(fitsfile_fp):
    scihdu = fits.open(fitsfile_fp)
    scihdr = scihdu[0].header
    scihdu.close()
    return scihdr

