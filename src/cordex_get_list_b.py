#
# Script to generate list of ESGF dataset ids for CORDEX, based on directory list generate by cordex_get_list_a.py
#

# USAGE : python3.6 cordex_get_list_b.py



import os, glob

oo = open( 'cordex_ds_list_urls_plus.txt', 'w' )
ooe = open( 'cordex_ds_list_esgfid.txt', 'w' )

for l in open( 'cordex_ds_list.txt', 'r' ).readlines():
  base = l.strip()
  lnk = os.readlink( base + '/latest' )
  v = lnk.strip().split('/')[-1]
  oo.write( '%s/%s\n' % (base,v) )
    ##/badc/cmip6/data/CMIP6/CMIP/CSIRO-ARCCSS/ACCESS-CM2/historical/r1i1p1f1/day/rsds/gn/v20191108
   ##/badc/cordex/data/cordex/output/EUR-11/MOHC/NCC-NorESM1-M/rcp85/r1i1p1/MOHC-HadREM3-GA7-05/v1/day/tasmin
   ##cordex.output.EUR-11.MOHC.CNRM-CERFACS-CNRM-CM5.rcp85.r1i1p1.HadREM3-GA7-05.v2.mon.ta500.v20210113

  region, inst, model1, expt, variant, model2, v1, tab, var = base.split('/')[6:15]
  esgf_ds_id = "cordex.output.%s.%s.%s.%s.%s.%s.%s.%s.%s.%s" % (region, inst, model1, expt, variant, model2, v1, tab, var, v )
  ooe.write( esgf_ds_id + '\n' )
    

oo.close()
ooe.close()
