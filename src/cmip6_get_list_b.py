
#
# Script to generate list of ESGF dataset ids for CMIP6, based on directory list generate by cmip6_get_list_a.py
#

# USAGE : python3.6 cmip6_get_list_b.py

import os, glob

oo = open( 'ds_list_urls_plus.txt', 'w' )
ooe = open( 'ds_list_esgfid.txt', 'w' )

for l in open( 'ds_list_urls.txt', 'r' ).readlines():
  base = l.strip()
  dd = glob.glob( base + '/*' )
  if len( dd ) != 0:
    if os.path.isdir( base + '/gr' ):
       lnk = os.readlink( base + '/gr/latest' )
       g = 'gr'
    elif os.path.isdir( base + '/gr1' ):
       lnk = os.readlink( base + '/gr1/latest' )
       g = 'gr1'
    elif os.path.isdir( base + '/gn' ):
       lnk = os.readlink( base + '/gn/latest' )
       g = 'gn'
    else:
       print( '%s: no gr,gn, gr1' % base )
       print( dd )
       break
    v = lnk.strip().split('/')[-1]
    oo.write( '%s/%s/%s\n' % (base,g,v) )
    ##/badc/cmip6/data/CMIP6/CMIP/CSIRO-ARCCSS/ACCESS-CM2/historical/r1i1p1f1/day/rsds/gn/v20191108
    inst, model, expt, variant_id, table, var = base.split('/')[6:12]
    esgf_ds_id = "CMIP6.CMIP.%s.%s.%s.%s.%s.%s.%s.%s" % (inst,model,expt,variant_id,table,var,g,v)
    ooe.write( esgf_ds_id + '\n' )
    
oo.close()
ooe.close()
