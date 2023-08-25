#
# Script to generate list of directories for CORDEX data
#

# USAGE : python3.6 cordex_get_list_b.py

import os, collections, glob

vars_str = 'clt, hurs, huss, pr, prsn, psl, rls, rss, rlds, rlus, rsds, rsus, sfcWind, snw, tas, tasmax, tasmin, uas, vas'
vars = [x.strip() for x in vars_str.split(',') ]
tabs = ['3hr','day']



# = /badc/cmip6/data/CMIP6/CMIP/IPSL/IPSL-CM6A-LR-INCA/historical//r1i1p1f1/3hr/
#/badc/cordex/data/cordex/output/EUR-11/MOHC/ECMWF-ERAINT/evaluation/r1i1p1/MOHC-HadREM3-GA7-05/v1/3hr/
ft0 = "/badc/cordex/data/cordex/output/EUR-11/MOHC/*/*/r1i1p1/"
#ft = "/badc/cmip6/data/CMIP6/CMIP/*/*/historical/"

l1 = [x.strip() for x in open( 'cordex_dirs.txt' ).readlines() ]

oox = open( 'cordex_ds_list.txt', 'w' )
for d in l1:
  for f in tabs:
    for g in glob.glob( '%s%s/*' % (d,f) ):
      v = g.split('/')[-1]
      if v in vars:
        print(g)
        oox.write( g + '\n' )

oox.close()
