## Generate TESS thumbnails
## Author: Maksym Pyatnytskyy (PMAK (AAVSO)) ##

from astropy.io import fits
from astropy.coordinates import get_constellation
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt

#==============================================================================

## Directory with TESS light curve FITS
fits_dir = "sector15/Vmag6.0-7.0/"
## List of FITS files with optional column 'tessmag'. Empty lines and lines prepended by # are ignored.
fits_list = "fits_list.txt"

# TESS magnitude range: process stars withing thi range (TESS mag!)
brightest_mag = -99
faintest_mag  = 99

# if specified, process stars within constellation only
constellation_short_name = None

# "PDCSAP_FLUX" or "SAP_FLUX"
flux_column = "PDCSAP_FLUX"

#==============================================================================

with open(fits_dir + fits_list, "r") as fits_lc_list_file:
    fits_lc_files = fits_lc_list_file.readlines()

fits_lc_files = [s.strip() for s in fits_lc_files]
fits_lc_files = [s for s in fits_lc_files if s != "" and s[0] != "#"]

with open(fits_dir + "TESS_LOG.txt", "w+") as log_file:
    log_file.write("N\tFITS\tTESSMAG\tOBJECT\tCoord\n")
    counter0 = 0
    counter = 0
    for fits_list_line in fits_lc_files:
        counter0 += 1
        fits_params = fits_list_line.split("\t")
        name = fits_params[0]
        if len(fits_params) > 1:
            tess_mag_from_list = float(fits_params[1])
        else:
            tess_mag_from_list = None
        if tess_mag_from_list == None or (tess_mag_from_list >= brightest_mag and tess_mag_from_list < faintest_mag):
            fits_lc_filename = fits_dir + name
            with fits.open(fits_lc_filename, mode="readonly", memmap=False) as hdulist:
                tess_mag = hdulist[0].header["TESSMAG"]
                if tess_mag_from_list != None or (tess_mag >= brightest_mag and tess_mag < faintest_mag):
                    obj_name = hdulist[0].header["OBJECT"]
                    ra_obj   = hdulist[0].header["RA_OBJ"]
                    dec_obj  = hdulist[0].header["DEC_OBJ"]
                    coord = SkyCoord(ra_obj, dec_obj, frame='icrs', unit='deg')
                    constellation = get_constellation(coord, short_name=True)
                    if constellation_short_name == None or constellation == constellation_short_name:
                        counter += 1
                        log_file.write(str(counter) + "\t" + fits_lc_filename + "\t" + str(tess_mag))
                        print("LC #" + str(counter))
                        print("FITS: " + name)
                        print("Object: " + obj_name)
                        print("RA Dec (Decimal)    : " + str(ra_obj) + " " + str(dec_obj))
                        print("RA Dec (Sexagesimal): " + coord.to_string(style="hmsdms", sep=" "))
                        print("Constellation: " + constellation)
                        tess_bjds = hdulist[1].data["TIME"]
                        flux = hdulist[1].data[flux_column]
                        t1 = tess_bjds[0]
                        t2 = tess_bjds[-1]
                        fig, ax = plt.subplots()
                        ax.plot(tess_bjds, flux, "ko", markersize=1)
                        ax.set_xlim(t1, t2)
                        fig.suptitle(obj_name + ", TESS_mag= " + str(tess_mag))
                        ax.set_ylabel(flux_column)
                        ax.set_xlabel("Time (TBJD)")
                        plt.subplots_adjust(left=0.15)
                        plt.show()
                        log_file.write("\t" + obj_name + "\t" + coord.to_string(style="hmsdms", sep=" ") + "\n")
                        log_file.flush()
