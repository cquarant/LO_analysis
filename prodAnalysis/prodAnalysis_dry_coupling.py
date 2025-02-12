import pandas as pd
import numpy as np
import matplotlib as mp
import ROOT as R
import os
import json
import argparse
import math as m

parser = argparse.ArgumentParser()
parser.add_argument('--json',dest='json')
parser.add_argument('--firstArray',dest='firstArray')
parser.add_argument('--lastArray',dest='lastArray')
args = parser.parse_args()

if not args.json:
    parser.error('missing input json file')
if not args.firstArray:
    parser.error('missing first array to analyze')
if not args.lastArray:
    parser.error('missing last array to analyze')

meas=pd.read_json(args.json,orient='records')
#split the tag name with '_'
meas[['tag%d'%s for s in range(0,10)]]=meas['tag'].str.split('_',expand=True)
meas['lyNorm']=meas['ly']/meas['lyRef']
meas['xt']=meas['xtLeft']+meas['xtRight']

print(meas.info())


meas['producer']=meas['producer'].str.replace('prod99','prod8')
arrays=set(meas['id'])
bars=set(meas['bar'])
prods=sorted(set(meas['producer'].str.replace('prod','').astype(int)))
producers=[ 'prod%d'%p for p in prods ]
iarr=set(meas['tag3'])
geo=set(meas['geometry'])

histos={}

histos['h1_ly_byProd_ratio']=R.TH1F('h1_ly_byProd_ratio','h1_ly_arrayRms_byProd_norm',60,0.,1.2)
histos['h1_lyNorm_byProd_ratio']=R.TH1F('h1_lyNorm_byProd_ratio','h1_lyNorm_byProd_norm',60,0.,1.2)
histos['h1_sigmaT_byProd_ratio']=R.TH1F('h1_sigmaT_byProd_ratio','h1_sigmaT_byProd_norm',60,0.,1.2)
histos['h1_ctr_byProd_ratio']=R.TH1F('h1_ctr_byProd_ratio','h1_ctr_byProd_norm',60,0.,1.2)
histos['h1_xt_byProd_ratio']=R.TH1F('h1_xt_byProd_ratio','h1_xt_byProd_norm',120,0.,1.2)
histos['h1_temp_byProd_ratio']=R.TH1F('h1_temp_byProd_ratio','h1_temp_byProd_norm',60,0.,1.5)
histos['h1_err_sigmaT_byProd_ratio']=R.TH1F('h1_err_sigmaT_byProd_ratio','h1_err_sigmaT_byProd_norm',60,0.,1.2)

for prod in producers:
    prod_arrays=set(meas[ (meas['producer']==prod) & (meas['tag8'].str.contains('PREIRR'))]['id'])
    print(str(prod),len(prod_arrays))

    histos['h1_ly_byProd_%s_ratio'%prod]=R.TH1F('h1_ly_byProd_%s_ratio'%prod,'h1_ly_byProd_%s_norm'%prod,100,0.5,1.5)
    histos['h1_lyNorm_byProd_%s_ratio'%prod]=R.TH1F('h1_lyNorm_byProd_%s_ratio'%prod,'h1_ly_byProd_%s_norm'%prod,100,0.5,1.5)
    histos['h1_sigmaT_byProd_%s_ratio'%prod]=R.TH1F('h1_sigmaT_byProd_%s_ratio'%prod,'h1_sigmaT_byProd_%s_norm'%prod,100,0.5,1.5)
    histos['h1_ctr_byProd_%s_ratio'%prod]=R.TH1F('h1_ctr_byProd_%s_ratio'%prod,'h1_ctr_byProd_%s_norm'%prod,100,0.5,1.5)
    histos['h1_xt_byProd_%s_ratio'%prod]=R.TH1F('h1_xt_byProd_%s_ratio'%prod,'h1_xt_byProd_%s_norm'%prod,50,0.,1.)
    histos['h1_temp_byProd_%s_ratio'%prod]=R.TH1F('h1_temp_byProd_%s_ratio'%prod,'h1_temp_byProd_%s_norm'%prod,100,2.,7.)
    histos['h1_err_sigmaT_byProd_%s_ratio'%prod]=R.TH1F('h1_err_sigmaT_byProd_%s_ratio'%prod,'h1_err_sigmaT_byProd_%s_norm'%prod,100,0.5,1.5)


    histos['h1_ly_arrayRms_byProd_%s_ratio'%prod]=R.TH1F('h1_ly_arrayRms_byProd_%s_ratio'%prod,'h1_ly_arrayRms_byProd_%s_norm'%prod,100,0.,0.2)
    histos['h1_lyNorm_arrayRms_byProd_%s_ratio'%prod]=R.TH1F('h1_lyNorm_arrayRms_byProd_%s_ratio'%prod,'h1_lyNorm_arrayRms_byProd_%s_norm'%prod,100,0.,0.2)
    histos['h1_sigmaT_arrayRms_byProd_%s_ratio'%prod]=R.TH1F('h1_sigmaT_arrayRms_byProd_%s_ratio'%prod,'h1_sigmaT_arrayRms_byProd_%s_norm'%prod,100,0.,0.2)
    histos['h1_ctr_arrayRms_byProd_%s_ratio'%prod]=R.TH1F('h1_ctr_arrayRms_byProd_%s_ratio'%prod,'h1_ctr_arrayRms_byProd_%s_norm'%prod,100,0.,0.2)
    histos['h1_xt_arrayRms_byProd_%s_ratio'%prod]=R.TH1F('h1_xt_arrayRms_byProd_%s_ratio'%prod,'h1_xt_arrayRms_byProd_%s_norm'%prod,100,0.,0.2)
    histos['h1_temp_arrayRms_byProd_%s_ratio'%prod]=R.TH1F('h1_temp_arrayRms_byProd_%s_ratio'%prod,'h1_temp_arrayRms_byProd_%s_norm'%prod,100,0.,1.)
    histos['h1_err_sigmaT_arrayRms_byProd_%s_ratio'%prod]=R.TH1F('h1_err_sigmaT_arrayRms_byProd_%s_ratio'%prod,'h1_err_sigmaT_arrayRms_byProd_%s_norm'%prod,100,0.,0.2)

    histos['h1_ly_array_byProd_%s_ratio'%prod]=R.TH1F('h1_ly_array_byProd_%s_ratio'%prod,'h1_ly_array_byProd_%s_norm'%prod,100,0.5,1.5)
    histos['h1_lyNorm_array_array_byProd_%s_ratio'%prod]=R.TH1F('h1_lyNorm_array_byProd_%s_ratio'%prod,'h1_ly_array_byProd_%s_norm'%prod,100,0.5,1.5)
    histos['h1_sigmaT_array_byProd_%s_ratio'%prod]=R.TH1F('h1_sigmaT_array_byProd_%s_ratio'%prod,'h1_sigmaT_array_byProd_%s_norm'%prod,100,0.5,1.5)
    histos['h1_ctr_array_byProd_%s_ratio'%prod]=R.TH1F('h1_ctr_array_byProd_%s_ratio'%prod,'h1_ctr_array_byProd_%s_norm'%prod,100,0.5,1.5)
    histos['h1_xt_array_byProd_%s_ratio'%prod]=R.TH1F('h1_xt_array_byProd_%s_ratio'%prod,'h1_xt_array_byProd_%s_norm'%prod,50,0.,1.)
    histos['h1_temp_array_byProd_%s_ratio'%prod]=R.TH1F('h1_temp_array_byProd_%s_ratio'%prod,'h1_temp_array_byProd_%s_norm'%prod,100,2.,7.)
    histos['h1_err_sigmaT_array_byProd_%s_ratio'%prod]=R.TH1F('h1_err_sigmaT_array_byProd_%s_ratio'%prod,'h1_err_sigmaT_array_byProd_%s_norm'%prod,100,0.5,1.5)

    for tag in ['PREIRR']:
    #    prod_arrays=set(meas[ (meas['producer']==prod) & (meas['tag8'].str.contains('PREIRR'))]['id'])
    #    print(str(prod),len(prod_arrays))

        histos['h1_ly_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_ly_byProd_%s_%s'%(prod,tag),'h1_ly_byProd_%s_%s'%(prod,tag),200,40,100.)
        histos['h1_lyNorm_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_lyNorm_byProd_%s_%s'%(prod,tag),'h1_ly_byProd_%s_%s'%(prod,tag),200,0.5,1.5)
        histos['h1_sigmaT_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_sigmaT_byProd_%s_%s'%(prod,tag),'h1_sigmaT_byProd_%s_%s'%(prod,tag),200,110.,210.)
        histos['h1_ctr_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_ctr_byProd_%s_%s'%(prod,tag),'h1_ctr_byProd_%s_%s'%(prod,tag),200,150.,250.)
        histos['h1_xt_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_xt_byProd_%s_%s'%(prod,tag),'h1_xt_byProd_%s_%s'%(prod,tag),100,0.,0.5)
        histos['h1_temp_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_temp_byProd_%s_%s'%(prod,tag),'h1_temp_byProd_%s_%s'%(prod,tag),100,2.,7.)
	histos['h1_err_sigmaT_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_err_sigmaT_byProd_%s_%s'%(prod,tag),'h1_err_sigmaT_byProd_%s_%s'%(prod,tag),200,0.,10.)


        histos['h1_ly_array_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_ly_array_byProd_%s_%s'%(prod,tag),'h1_ly_array_byProd_%s_%s'%(prod,tag),200,40,100.)
        histos['h1_lyNorm_array_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_lyNorm_array_byProd_%s_%s'%(prod,tag),'h1_ly_array_byProd_%s_%s'%(prod,tag),200,0.5,1.5)
        histos['h1_sigmaT_array_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_sigmaT_array_byProd_%s_%s'%(prod,tag),'h1_sigmaT_array_byProd_%s_%s'%(prod,tag),200,110.,210.)
        histos['h1_ctr_array_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_ctr_array_byProd_%s_%s'%(prod,tag),'h1_ctr_array_byProd_%s_%s'%(prod,tag),200,150.,250.)
        histos['h1_xt_array_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_xt_array_byProd_%s_%s'%(prod,tag),'h1_xt_array_byProd_%s_%s'%(prod,tag),100,0.,0.5)
        histos['h1_temp_array_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_temp_array_byProd_%s_%s'%(prod,tag),'h1_temp_array_byProd_%s_%s'%(prod,tag),100,2.,7.)
	histos['h1_err_sigmaT_array_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_err_sigmaT_array_byProd_%s_%s'%(prod,tag),'h1_err_sigmaT_array_byProd_%s_%s'%(prod,tag),200,0.,10.)


        histos['h1_ly_arrayRms_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_ly_arrayRms_byProd_%s_%s'%(prod,tag),'h1_ly_arrayRms_byProd_%s_%s'%(prod,tag),100,0.,0.2)
        histos['h1_lyNorm_arrayRms_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_lyNorm_arrayRms_byProd_%s_%s'%(prod,tag),'h1_lyNorm_arrayRms_byProd_%s_%s'%(prod,tag),100,0.,0.2)
        histos['h1_sigmaT_arrayRms_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_sigmaT_arrayRms_byProd_%s_%s'%(prod,tag),'h1_sigmaT_arrayRms_byProd_%s_%s'%(prod,tag),100,0.,0.2)
        histos['h1_ctr_arrayRms_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_ctr_arrayRms_byProd_%s_%s'%(prod,tag),'h1_ctr_arrayRms_byProd_%s_%s'%(prod,tag),100,0.,0.2)
        histos['h1_xt_arrayRms_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_xt_arrayRms_byProd_%s_%s'%(prod,tag),'h1_xt_arrayRms_byProd_%s_%s'%(prod,tag),100,0.,0.2)
        histos['h1_temp_arrayRms_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_temp_arrayRms_byProd_%s_%s'%(prod,tag),'h1_temp_arrayRms_byProd_%s_%s'%(prod,tag),100,0.,1.)
 	histos['h1_err_sigmaT_arrayRms_byProd_%s_%s'%(prod,tag)]=R.TH1F('h1_err_sigmaT_arrayRms_byProd_%s_%s'%(prod,tag),'h1_err_sigmaT_arrayRms_byProd_%s_%s'%(prod,tag),100,0.,0.2)


        for ia in iarr:
            histos['h1_ly_byProd_%s_%s_%s'%(prod,ia,tag)]=R.TH1F('h1_ly_byProd_%s_%s_%s'%(prod,ia,tag),'h1_ly_byProd_%s_%s_%s'%(prod,ia,tag),200,50,100.)
            histos['h1_lyNorm_byProd_%s_%s_%s'%(prod,ia,tag)]=R.TH1F('h1_lyNorm_byProd_%s_%s_%s'%(prod,ia,tag),'h1_ly_byProd_%s_%s_%s'%(prod,ia,tag),200,0.5,1.5)
            histos['h1_sigmaT_byProd_%s_%s_%s'%(prod,ia,tag)]=R.TH1F('h1_sigmaT_byProd_%s_%s_%s'%(prod,ia,tag),'h1_sigmaT_byProd_%s_%s_%s'%(prod,ia,tag),200,110.,210.)
            histos['h1_ctr_byProd_%s_%s_%s'%(prod,ia,tag)]=R.TH1F('h1_ctr_byProd_%s_%s_%s'%(prod,ia,tag),'h1_ctr_byProd_%s_%s_%s'%(prod,ia,tag),200,150.,250.)
            histos['h1_xt_byProd_%s_%s_%s'%(prod,ia,tag)]=R.TH1F('h1_xt_byProd_%s_%s_%s'%(prod,ia,tag),'h1_xt_byProd_%s_%s_%s'%(prod,ia,tag),100,0.,0.5)
            histos['h1_temp_byProd_%s_%s_%s'%(prod,ia,tag)]=R.TH1F('h1_temp_byProd_%s_%s_%s'%(prod,ia,tag),'h1_temp_byProd_%s_%s_%s'%(prod,ia,tag),100,2.,7.)
	    histos['h1_err_sigmaT_byProd_%s_%s_%s'%(prod,ia,tag)]=R.TH1F('h1_err_sigmaT_byProd_%s_%s_%s'%(prod,ia,tag),'h1_err_sigmaT_byProd_%s_%s_%s'%(prod,ia,tag),200,0.,10.)

	for g in geo:
            histos['h1_ly_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_ly_byProd_%s_%s_%s'%(prod,g,tag),'h1_ly_byProd_%s_%s_%s'%(prod,g,tag),200,50,100.)
            histos['h1_lyNorm_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_lyNorm_byProd_%s_%s_%s'%(prod,g,tag),'h1_ly_byProd_%s_%s_%s'%(prod,g,tag),200,0.5,1.5)
            histos['h1_sigmaT_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_sigmaT_byProd_%s_%s_%s'%(prod,g,tag),'h1_sigmaT_byProd_%s_%s_%s'%(prod,g,tag),200,110.,210.)
            histos['h1_ctr_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_ctr_byProd_%s_%s_%s'%(prod,g,tag),'h1_ctr_byProd_%s_%s_%s'%(prod,g,tag),200,150.,250.)
            histos['h1_xt_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_xt_byProd_%s_%s_%s'%(prod,g,tag),'h1_xt_byProd_%s_%s_%s'%(prod,g,tag),100,0.,0.5)
            histos['h1_temp_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_temp_byProd_%s_%s_%s'%(prod,g,tag),'h1_temp_byProd_%s_%s_%s'%(prod,g,tag),100,2.,7.)
	    histos['h1_err_sigmaT_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_err_sigmaT_byProd_%s_%s_%s'%(prod,g,tag),'h1_err_sigmaT_byProd_%s_%s_%s'%(prod,g,tag),200,0.,10.)


            histos['h1_ly_array_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_ly_array_byProd_%s_%s_%s'%(prod,g,tag),'h1_ly_array_byProd_%s_%s_%s'%(prod,g,tag),200,50,100.)
            histos['h1_lyNorm_array_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_lyNorm_array_byProd_%s_%s_%s'%(prod,g,tag),'h1_ly_array_byProd_%s_%s_%s'%(prod,g,tag),200,0.5,1.5)
            histos['h1_sigmaT_array_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_sigmaT_array_byProd_%s_%s_%s'%(prod,g,tag),'h1_sigmaT_array_byProd_%s_%s_%s'%(prod,g,tag),200,110.,210.)
            histos['h1_ctr_array_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_ctr_array_byProd_%s_%s_%s'%(prod,g,tag),'h1_ctr_array_byProd_%s_%s_%s'%(prod,g,tag),200,150.,250.)
            histos['h1_xt_array_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_xt_array_byProd_%s_%s_%s'%(prod,g,tag),'h1_xt_array_byProd_%s_%s_%s'%(prod,g,tag),100,0.,0.5)
            histos['h1_temp_array_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_temp_array_byProd_%s_%s_%s'%(prod,g,tag),'h1_temp_array_byProd_%s_%s_%s'%(prod,g,tag),100,2.,7.)
	    histos['h1_err_sigmaT_array_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_err_sigmaT_array_byProd_%s_%s_%s'%(prod,g,tag),'h1_err_sigmaT_array_byProd_%s_%s_%s'%(prod,g,tag),200,0.,10.)


	    histos['h1_ly_arrayRms_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_ly_arrayRms_byProd_%s_%s_%s'%(prod,g,tag),'h1_ly_arrayRms_byProd_%s_%s_%s'%(prod,g,tag),400,0.,0.8)
            histos['h1_lyNorm_arrayRms_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_lyNorm_arrayRms_byProd_%s_%s_%s'%(prod,g,tag),'h1_lyNorm_arrayRms_byProd_%s_%s_%s'%(prod,g,tag),400,0.,0.8)
            histos['h1_sigmaT_arrayRms_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_sigmaT_arrayRms_byProd_%s_%s_%s'%(prod,g,tag),'h1_sigmaT_arrayRms_byProd_%s_%s_%s'%(prod,g,tag),400,0.,0.8)
            histos['h1_ctr_arrayRms_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_ctr_arrayRms_byProd_%s_%s_%s'%(prod,g,tag),'h1_ctr_arrayRms_byProd_%s_%s_%s'%(prod,g,tag),400,0.,0.8)
            histos['h1_xt_arrayRms_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_xt_arrayRms_byProd_%s_%s_%s'%(prod,g,tag),'h1_xt_arrayRms_byProd_%s_%s_%s'%(prod,g,tag),400,0.,0.8)
            histos['h1_temp_arrayRms_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_temp_arrayRms_byProd_%s_%s_%s'%(prod,g,tag),'h1_temp_arrayRms_byProd_%s_%s'%(prod,tag),100,0.,1.)
	    histos['h1_err_sigmaT_arrayRms_byProd_%s_%s_%s'%(prod,g,tag)]=R.TH1F('h1_err_sigmaT_arrayRms_byProd_%s_%s_%s'%(prod,g,tag),'h1_err_sigmaT_arrayRms_byProd_%s_%s_%s'%(prod,g,tag),400,0.,0.8)


    #### The analysis part...
    for tag in ['PREIRR']:
        # plots by producer 
        for index, row in meas[ (meas['producer']==prod)  
                                & (meas['tag8'].str.contains(tag))
                                & (meas['id']>=int(args.firstArray))  #post OptStep2 (Jul 2022)
                                & (meas['id']<=int(args.lastArray))
                                # & (meas['id']>809)  #post OptStep2 (Jul 2022)
                                # & (meas['id']<840)
                                & (meas['bar']!=0) #skip first and last bar of each array
                                & (meas['bar']!=15) ].iterrows():

            for hh in ['ly','lyNorm','sigmaT','err_sigmaT','ctr','xt','temp']:
		histos['h1_%s_byProd_%s_%s'%(hh,prod,tag)].Fill(row[hh])
                histos['h1_%s_byProd_%s_%s_%s'%(hh,prod,row['tag3'],tag)].Fill(row[hh])
                histos['h1_%s_byProd_%s_%s_%s'%(hh,prod,row['geometry'],tag)].Fill(row[hh])

        # plots by array
        for arr in prod_arrays:
	  for eg,g in enumerate(geo):
            my_data=meas[ (meas['id'] == arr) 
                          & (meas['bar']!=0) #skip first and last bar of each array
                          & (meas['bar']!=15)
                          & (meas['id']>=int(args.firstArray))  #post OptStep2 (Jul 2022)
                          & (meas['id']<=int(args.lastArray))
                          # & (meas['id']>809)  #post OptStep2 (Jul 2022)
                          # & (meas['id']<840)
			  & (meas['geometry']==g)
                          & (meas['tag8'].str.contains(tag)) ]
            runs=set(my_data['tag0'])

            for r in runs:
           	run_data=my_data[ my_data['tag0'] == r]
		ll=set(run_data['tag3'])
		for l in ll:	
	    #	print(run_data['id'])
                    for hh in ['ly','lyNorm','sigmaT','err_sigmaT','ctr','xt','temp']:	
                        if (hh=='sigmaT'):
                            histos['h1_%s_arrayRms_byProd_%s_%s_%s'%(hh,prod,g,tag)].Fill(R.TMath.Sqrt(run_data[hh].std()*run_data[hh].std()-run_data['err_'+hh].mean()*run_data['err_'+hh].mean())/run_data[hh].mean())
                            histos['h1_%s_array_byProd_%s_%s'%(hh,prod,tag)].Fill(run_data[hh].mean())
                            histos['h1_%s_array_byProd_%s_%s_%s'%(hh,prod,g,tag)].Fill(run_data[hh].mean())

                        else:
                            histos['h1_%s_array_byProd_%s_%s'%(hh,prod,tag)].Fill(run_data[hh].mean())
                            histos['h1_%s_array_byProd_%s_%s_%s'%(hh,prod,g,tag)].Fill(run_data[hh].mean())

                            if (hh=='xt' or hh=='temp'):
                                    histos['h1_%s_arrayRms_byProd_%s_%s'%(hh,prod,tag)].Fill(run_data[hh].std())
                                    histos['h1_%s_arrayRms_byProd_%s_%s_%s'%(hh,prod,g,tag)].Fill(run_data[hh].std())
                            elif(hh=='err_sigmaT'):
                                histos['h1_%s_arrayRms_byProd_%s_%s'%(hh,prod,tag)].Fill(run_data[hh].mean())
                                histos['h1_%s_arrayRms_byProd_%s_%s_%s'%(hh,prod,g,tag)].Fill(run_data[hh].mean())
                            else:
                                histos['h1_%s_arrayRms_byProd_%s_%s'%(hh,prod,tag)].Fill(run_data[hh].std()/run_data[hh].mean())
                                histos['h1_%s_arrayRms_byProd_%s_%s_%s'%(hh,prod,g,tag)].Fill(run_data[hh].std()/run_data[hh].mean())	

for en,tag in enumerate(['PREIRR']):
   # print(en,tag)
    for hh in ['temp','ly','lyNorm','sigmaT','err_sigmaT','ctr','xt']:
	if (tag=='PREIRR'):
	        histos['%s_byProd_ratio'%hh]=R.TGraphErrors()
       		histos['%s_byProd_ratio'%hh].SetName('%s_byProd_ratio'%hh)
        	histos['%s_byProd_ratio'%hh].SetMarkerStyle(24)
        	histos['%s_byProd_ratio'%hh].SetMarkerSize(0.8)

        	histos['%s_arrayRms_byProd_ratio'%hh]=R.TGraphErrors()
        	histos['%s_arrayRms_byProd_ratio'%hh].SetName('%s_arrayRms_byProd_ratio'%hh)
        	histos['%s_arrayRms_byProd_ratio'%hh].SetMarkerStyle(24)
        	histos['%s_arrayRms_byProd_ratio'%hh].SetMarkerSize(0.8)

        	histos['%s_rms_byProd_ratio'%hh]=R.TGraphErrors()
        	histos['%s_rms_byProd_ratio'%hh].SetName('%s_rms_byProd_ratio'%hh)
        	histos['%s_rms_byProd_ratio'%hh].SetMarkerStyle(24)
	        histos['%s_rms_byProd_ratio'%hh].SetMarkerSize(0.8)

        histos['%s_byProd_%s'%(hh,tag)]=R.TGraphErrors()
        histos['%s_byProd_%s'%(hh,tag)].SetName('%s_byProd_%s'%(hh,tag))
        histos['%s_byProd_%s'%(hh,tag)].SetMarkerColor((en+1)%4)
	histos['%s_byProd_%s'%(hh,tag)].SetMarkerStyle(en+24)
        histos['%s_byProd_%s'%(hh,tag)].SetLineColor((en+1)%4)
	histos['%s_byProd_%s'%(hh,tag)].SetMarkerSize(1.2)

        histos['%s_arrayRms_byProd_%s'%(hh,tag)]=R.TGraphErrors()
        histos['%s_arrayRms_byProd_%s'%(hh,tag)].SetName('%s_arrayRms_byProd_%s'%(hh,tag))
        histos['%s_arrayRms_byProd_%s'%(hh,tag)].SetMarkerStyle(en+24)
	histos['%s_arrayRms_byProd_%s'%(hh,tag)].SetMarkerColor((en+1)%4)
        histos['%s_arrayRms_byProd_%s'%(hh,tag)].SetMarkerSize(0.8)
	histos['%s_arrayRms_byProd_%s'%(hh,tag)].SetLineColor((en+1)%4)

        histos['%s_rms_byProd_%s'%(hh,tag)]=R.TGraphErrors()
        histos['%s_rms_byProd_%s'%(hh,tag)].SetName('%s_rms_byProd_%s'%(hh,tag))
        histos['%s_rms_byProd_%s'%(hh,tag)].SetMarkerStyle(en+24)
        histos['%s_rms_byProd_%s'%(hh,tag)].SetMarkerSize(0.8)
        histos['%s_rms_byProd_%s'%(hh,tag)].SetMarkerColor((en+1)%4)
        histos['%s_rms_byProd_%s'%(hh,tag)].SetLineColor((en+1)%4)

	for eg,g in enumerate(geo):
            histos['%s_byProd_%s_%s'%(hh,g,tag)]=R.TGraphErrors()
            histos['%s_byProd_%s_%s'%(hh,g,tag)].SetName('%s_byProd_%s_%s'%(hh,g,tag))
            histos['%s_byProd_%s_%s'%(hh,g,tag)].SetMarkerColor((eg+1)%4)
            histos['%s_byProd_%s_%s'%(hh,g,tag)].SetMarkerStyle(eg+24)
            histos['%s_byProd_%s_%s'%(hh,g,tag)].SetLineColor((eg+1)%4)
            histos['%s_byProd_%s_%s'%(hh,g,tag)].SetMarkerSize(1.2)
            
            histos['%s_arrayRms_byProd_%s_%s'%(hh,g,tag)]=R.TGraphErrors()
            histos['%s_arrayRms_byProd_%s_%s'%(hh,g,tag)].SetName('%s_arrayRms_byProd_%s_%s'%(hh,g,tag))
            histos['%s_arrayRms_byProd_%s_%s'%(hh,g,tag)].SetMarkerStyle(eg+24)
            histos['%s_arrayRms_byProd_%s_%s'%(hh,g,tag)].SetMarkerColor((eg+1)%4)
            histos['%s_arrayRms_byProd_%s_%s'%(hh,g,tag)].SetMarkerSize(0.8)
            histos['%s_arrayRms_byProd_%s_%s'%(hh,g,tag)].SetLineColor((eg+1)%4)
            
            histos['%s_rms_byProd_%s_%s'%(hh,g,tag)]=R.TGraphErrors()
            histos['%s_rms_byProd_%s_%s'%(hh,g,tag)].SetName('%s_rms_byProd_%s_%s'%(hh,g,tag))
            histos['%s_rms_byProd_%s_%s'%(hh,g,tag)].SetMarkerStyle(eg+24)
            histos['%s_rms_byProd_%s_%s'%(hh,g,tag)].SetMarkerSize(0.8)
            histos['%s_rms_byProd_%s_%s'%(hh,g,tag)].SetMarkerColor((eg+1)%4)
            histos['%s_rms_byProd_%s_%s'%(hh,g,tag)].SetLineColor((eg+1)%4)
            

    for ip,prod in enumerate(producers):
        for hh in ['temp','ly','lyNorm','sigmaT','err_sigmaT','ctr','xt']:
            histos['%s_byProd_%s'%(hh,tag)].SetPoint(ip,ip+(0.05+en*0.08),histos['h1_%s_byProd_%s_%s'%(hh,prod,tag)].GetMean())
            histos['%s_byProd_%s'%(hh,tag)].SetPointError(ip,0,histos['h1_%s_byProd_%s_%s'%(hh,prod,tag)].GetRMS())
            histos['%s_arrayRms_byProd_%s'%(hh,tag)].SetPoint(ip,ip+(0.05+en*0.08),histos['h1_%s_arrayRms_byProd_%s_%s'%(hh,prod,tag)].GetMean()*100)
            histos['%s_arrayRms_byProd_%s'%(hh,tag)].SetPointError(ip,0,histos['h1_%s_arrayRms_byProd_%s_%s'%(hh,prod,tag)].GetMeanError()*100)

	    for eg,g in enumerate(geo):
		histos['%s_byProd_%s_%s'%(hh,g,tag)].SetPoint(ip,ip+(0.10+eg*0.08),histos['h1_%s_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetMean())
            	histos['%s_byProd_%s_%s'%(hh,g,tag)].SetPointError(ip,0,histos['h1_%s_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetRMS())
		histos['%s_arrayRms_byProd_%s_%s'%(hh,g,tag)].SetPoint(ip,ip+(0.10+eg*0.08),histos['h1_%s_arrayRms_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetMean()*100)
            	histos['%s_arrayRms_byProd_%s_%s'%(hh,g,tag)].SetPointError(ip,0,histos['h1_%s_arrayRms_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetMeanError()*100)            
		if (hh == 'xt' or hh=='temp'):
    	            histos['%s_rms_byProd_%s_%s'%(hh,g,tag)].SetPoint(ip,ip+(0.10+eg*0.08),histos['h1_%s_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetRMS()*100)
        	    histos['%s_rms_byProd_%s_%s'%(hh,g,tag)].SetPointError(ip,0,histos['h1_%s_arrayRms_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetRMSError()*100)
                else:
                    if (histos['h1_%s_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetMean()*100!=0):
                        if (hh=='sigmaT'):
                            histos['%s_rms_byProd_%s_%s'%(hh,g,tag)].SetPoint(ip,ip+(0.05+eg*0.08),R.TMath.Sqrt(histos['h1_%s_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetRMS()*histos['h1_%s_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetRMS()-histos['h1_err_%s_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetMean()*histos['h1_err_%s_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetMean())/histos['h1_%s_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetMean()*100)
                            histos['%s_rms_byProd_%s_%s'%(hh,g,tag)].SetPointError(ip,0,(histos['h1_%s_arrayRms_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetRMSError()*100))

                        else:
                            histos['%s_rms_byProd_%s_%s'%(hh,g,tag)].SetPoint(ip,ip+(0.05+eg*0.08),histos['h1_%s_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetRMS()/histos['h1_%s_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetMean()*100)
                            histos['%s_rms_byProd_%s_%s'%(hh,g,tag)].SetPointError(ip,0,histos['h1_%s_arrayRms_byProd_%s_%s_%s'%(hh,prod,g,tag)].GetRMSError()*100)

 
	    if (tag == 'PREIRR'):
	    	#histos['%s_byProd_ratio'%hh].SetPoint(ip,ip,histos['h1_%s_byProd_%s_geo2_POSTIRR'%(hh,prod)].GetMean()/histos['h1_%s_byProd_%s_geo2_PREIRR'%(hh,prod)].GetMean()) #pat
            	histos['%s_byProd_ratio'%hh].SetPointError(ip,0,0)
            	histos['%s_arrayRms_byProd_ratio'%hh].SetPoint(ip,ip,histos['h1_%s_arrayRms_byProd_%s_ratio'%(hh,prod)].GetMean()*100)
            	histos['%s_arrayRms_byProd_ratio'%hh].SetPointError(ip,0,histos['h1_%s_arrayRms_byProd_%s_ratio'%(hh,prod)].GetMeanError()*100)           
	    	

	    if (hh == 'xt' or hh=='temp'):
                histos['%s_rms_byProd_%s'%(hh,tag)].SetPoint(ip,ip+(0.05+en*0.08),histos['h1_%s_byProd_%s_%s'%(hh,prod,tag)].GetRMS()*100)
                histos['%s_rms_byProd_%s'%(hh,tag)].SetPointError(ip,0,histos['h1_%s_arrayRms_byProd_%s_%s'%(hh,prod,tag)].GetRMSError()*100)
	    else:
		if histos['h1_%s_byProd_%s_%s'%(hh,prod,tag)].GetMean() !=0:
			histos['%s_rms_byProd_%s'%(hh,tag)].SetPoint(ip,ip+(0.05+en*0.08),histos['h1_%s_byProd_%s_%s'%(hh,prod,tag)].GetRMS()/histos['h1_%s_byProd_%s_%s'%(hh,prod,tag)].GetMean()*100)
                	histos['%s_rms_byProd_%s'%(hh,tag)].SetPointError(ip,0,histos['h1_%s_arrayRms_byProd_%s_%s'%(hh,prod,tag)].GetRMSError()*100)


            histos['%s_%s_VsIarr_%s'%(hh,prod,tag)]=R.TGraphErrors()
            histos['%s_%s_VsIarr_%s'%(hh,prod,tag)].SetName('%s_%s_VsIarr_%s'%(hh,prod,tag))
            histos['%s_%s_VsIarr_%s'%(hh,prod,tag)].SetMarkerStyle(24)
            histos['%s_%s_VsIarr_%s'%(hh,prod,tag)].SetMarkerSize(1.2)
            for ia,array in enumerate(iarr):
                histos['%s_%s_VsIarr_%s'%(hh,prod,tag)].SetPoint(ia,ia,histos['h1_%s_byProd_%s_%s_%s'%(hh,prod,array,tag)].GetMean())
                histos['%s_%s_VsIarr_%s'%(hh,prod,tag)].SetPointError(ia,0,histos['h1_%s_byProd_%s_%s_%s'%(hh,prod,array,tag)].GetRMS())

        for hh in ['temp','ly','lyNorm','sigmaT','err_sigmaT','ctr','xt']:
            histos['%s_byProd_%s'%(hh,tag)].GetHistogram().SetBins(len(producers),-0.5,len(producers)-0.5)
	    histos['%s_byProd_ratio'%hh].GetHistogram().SetBins(len(producers),-0.5,len(producers)-0.5)
            histos['%s_arrayRms_byProd_%s'%(hh,tag)].GetHistogram().SetBins(len(producers),-0.5,len(producers)-0.5)
            histos['%s_rms_byProd_%s'%(hh,tag)].GetHistogram().SetBins(len(producers),-0.5,len(producers)-0.5)
	    for g in geo:
		histos['%s_byProd_%s_%s'%(hh,g,tag)].GetHistogram().SetBins(len(producers),-0.5,len(producers)-0.5)
            	histos['%s_arrayRms_byProd_%s_%s'%(hh,g,tag)].GetHistogram().SetBins(len(producers),-0.5,len(producers)-0.5)
            	histos['%s_rms_byProd_%s_%s'%(hh,g,tag)].GetHistogram().SetBins(len(producers),-0.5,len(producers)-0.5)
            for ip,prod in enumerate(producers):
                histos['%s_byProd_%s'%(hh,tag)].GetHistogram().GetXaxis().SetBinLabel(ip+1,prod)
		histos['%s_byProd_ratio'%hh].GetHistogram().GetXaxis().SetBinLabel(ip+1,prod)
                histos['%s_arrayRms_byProd_%s'%(hh,tag)].GetHistogram().GetXaxis().SetBinLabel(ip+1,prod)
                histos['%s_rms_byProd_%s'%(hh,tag)].GetHistogram().GetXaxis().SetBinLabel(ip+1,prod)
       		for g in geo:
			histos['%s_byProd_%s_%s'%(hh,g,tag)].GetHistogram().GetXaxis().SetBinLabel(ip+1,prod)
        	        histos['%s_arrayRms_byProd_%s_%s'%(hh,g,tag)].GetHistogram().GetXaxis().SetBinLabel(ip+1,prod)
                	histos['%s_rms_byProd_%s_%s'%(hh,g,tag)].GetHistogram().GetXaxis().SetBinLabel(ip+1,prod)
 

	

#fOut=R.TFile('prodAnalysis_pat_postMS3_all.root','RECREATE')
#fOut=R.TFile('prodAnalysis_pat_postMS3_noProd6_Sept-Oct2021.root','RECREATE')
#fOut=R.TFile('prodAnalysis_c40_OptStep2_Jul2022.root','RECREATE')
fOut=R.TFile('prodAnalysis_dry_coupling_Oct2022.root','RECREATE')
for h,hh in histos.iteritems():
    hh.Write()
fOut.Close()
