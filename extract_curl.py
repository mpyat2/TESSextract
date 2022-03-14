# This script extracts curl commands from a bulk download script
# for a list of TESS IDs

import numpy as np

# list of TESS IDs (TESS ID in the first column)
list_of_ids = 'ID_Vmag6.0-7.0.txt'

# input script: light curves
# https://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_ffi-tp-lc-dv.html
input_script = 'tesscurl_sector_15_lc.sh'

# output script that contains selected IDs only
output_script = 'sector15/Vmag6.0-7.0/tesscurl_sector_15_lc_short.sh'

ids = np.loadtxt(list_of_ids, comments='#', delimiter='\t')
                
with open(input_script, 'r')  as data:
    lines = data.readlines()

with open(output_script, 'w', newline='\n') as outf:
    for s in lines:
        s0 = s.strip();
        s = s0
        if s != '' and s[0] != '#':
            id = int(s[40:56])
            if id in ids:
                outf.write(s0 + '\n')
        else:
            outf.write(s0 + '\n')
