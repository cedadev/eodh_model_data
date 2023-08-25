#
# Script to find list of CMIP6 directories associated with a selection of variables and experiments
#

# USAGE: python3.6 cmip6_get_list_a.py

import os, collections, glob


## setup -- define lists of variables of interest
mip = 'CMIP'
expt = 'historical'
mip = "ScenarioMIP"
expts = ["ssp119", "ssp126", "ssp245", "ssp585"]
vars_str = 'clt, hurs, huss, pr, prsn, psl, rls, rss, rlds, rlus, rsds, rsus, sfcWind, snw, tas, tasmax, tasmin, uas, vas'
tt3hr = dict( sfcWind="E3hr", psl="CF3hr" )
vars = [x.strip() for x in vars_str.split(',') ]
tabs = ['3hr','CF3hr','E3hr','day', 'CFday', 'Eday','Amon']
freq = dict( mon=dict( Amon=vars ), day=dict( day=vars ) )

vdict = collections.defaultdict( lambda: collections.defaultdict( set ) )
mdict = collections.defaultdict( lambda: collections.defaultdict( set ) )

f3 = dict( E3hr=['sfcWind'], CF3hr=['psl'] )
f3["3hr"]=[v for v in vars if v not in ['sfcWind','psl']]
freq["3hr"] = f3

# = /badc/cmip6/data/CMIP6/CMIP/IPSL/IPSL-CM6A-LR-INCA/historical//r1i1p1f1/3hr/
ft0 = "/badc/cmip6/data/CMIP6/%(mip)s/*/*/%(expt)s/"
#ft = "/badc/cmip6/data/CMIP6/CMIP/*/*/historical/"


## define a function to do the work for a specific MIP and experiment

def run(mip,expt,oo_list):
  ft = ft0 % locals()

  l1 = os.popen( "ls -1 -d %s > .tmp" % ft ).read()
  ll = sorted( open( ".tmp" ).readlines() )
  print ( 'Number of models with %s simulations = %s' % (expt,len(ll)) )
  models = []
  institutions = collections.defaultdict(list)
  models = collections.defaultdict(list)
  for l in ll:
    i,m = l.split('/')[6:8]
    models[m].append(l.strip())
    institutions[i].append(m)

  _models = sorted( list( models.keys() ) )

  rl = []
  for m in _models:
   xx = sorted( glob.glob( models[m][0] + "r1i*" ) )
   if len(xx) > 0:
     print( m,xx[0] )
     for f,dd in freq.items():
       for t,vl in dd.items():
         base = xx[0] + '/' + t
         if os.path.isdir( base ):
           dd = [x.split('/')[-1].strip() for x in glob.glob( base + '/*' )]
           v0 = [v for v in vl if v in dd]
           print ( '   --- ',t,v0)
           for v in v0:
             oo_list.write( '%s/%s\n' % (base,v) )
             vdict[v][f].add(m)
             mdict[m][f].add(v)
   else:
     print ( m, '--',  models[m][0] )
   
  

  oo = open( 'model_count_by_var_%s.csv' % expt, 'w' )
  oo.write( 'Variable, 3hr, day, mon,\n' )
  for v in vars:
    ss = [str(len(vdict[v][f])) for f in ['3hr','day','mon'] ]
    oo.write( ','.join( [v,] + ss ) + '\n' )
  oo.close()

  oo = open( 'var_count_by_model_%s.csv' % expt, 'w' )
  oo.write( 'Model, 3hr, day, mon,\n' )
  for m in sorted(list(mdict.keys())):
    ss = [str(len(mdict[m][f])) for f in ['3hr','day','mon'] ]
    oo.write( ','.join( [m,] + ss ) + '\n' )
  oo.close()

## loop over all mips and experiments

oox = open( 'ds_list_urls.txt', 'w' )
run( 'CMIP', 'historical',oox )
for e in expts:
  run( mip, e, oox )
oox.close()
