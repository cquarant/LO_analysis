#! /usr/bin/env python

import os
import sys
import optparse
import datetime
import subprocess
from glob import glob
from collections import defaultdict
from collections import OrderedDict
from array import array

from ROOT import *
import numpy as np

gROOT.SetBatch(True)

usage = "usage: python analysis/launch_analyze_run_array.py --firstRun 1 -i /home/cmsdaq/Workspace/TOFPET/Timing-TOFPET/output/TestArray -o /home/cmsdaq/Workspace/TOFPET/Timing-TOFPET/output/TestArray/RESULTS --arrayCode 0"

parser = optparse.OptionParser(usage)

parser.add_option("-r", "--firstRun", dest="firstRun",
                  help="first run number of the position scan")

parser.add_option("-i", "--input", dest="inputDir",default="/data/TOFPET/LYSOARRAYS",
                  help="input directory")

parser.add_option("-o", "--output", dest="outputDir",default="/data/TOFPET/LYSOARRAYS/RESULTS",
                  help="output directory")

parser.add_option("-b", "--arrayCode", dest="arrayCode", default=-99,
                  help="code of the crystal array")

(opt, args) = parser.parse_args()

if not opt.firstRun:   
    parser.error('first run number not provided')

if not opt.inputDir:   
    parser.error('input directory not provided')

if not opt.outputDir:   
    parser.error('output directory not provided')

#------------------------------------------------

nFilesInScan = 10

#maybe this can be passed from command line 
th = [ 15+5*i for i in range(10) ]


summaryFile = str(opt.outputDir)+"/"+"summary_"+"FirstRun" + str(opt.firstRun.zfill(6)) + "_LastRun" + str((int(opt.firstRun)+(nFilesInScan-1)*3)).zfill(6) + "_ARRAY" + str(opt.arrayCode.zfill(6))+".root"

#### Analysis Summary #####
histos={}

for v in [ 'LY','sigmaT','DT','CTR','XT']:
    histos['%s_vs_pos'%v]=TGraphErrors()
    histos['%s_vs_pos'%v].SetName('%s_vs_bar'%v)

tfileResults={}
treeResults={}

thscan_step=200/60. #LSB for disc_th1_lsb=60 according to TOFPET2 datasheet

sigmaTvsTH=TF1("sigmaTvsTH","TMath::Sqrt([0]*[0]/TMath::Power(x,[1])+[2]*[2]*TMath::Power(x,[3]))",0,1000)
sigmaTvsTH.SetParameter(0,5.67032e+04)
sigmaTvsTH.SetParameter(2,6.21645e+01)
sigmaTvsTH.SetParLimits(1,0.,5.)
sigmaTvsTH.SetParLimits(3,0.,5.)
sigmaTvsTH.SetParameter(1,3.1)
sigmaTvsTH.SetParameter(3,0.3)

istep=0
for step in range(len(th)):
    if (gSystem.AccessPathName(opt.inputDir+"/tree_Run%s_ARRAY%s.root"%(str(int(opt.firstRun)+step*3).zfill(6),opt.arrayCode.zfill(6)))):
        continue
    tfileResults[th[step]] = TFile.Open(opt.inputDir+"/tree_Run%s_ARRAY%s.root"%(str(int(opt.firstRun)+step*3).zfill(6),opt.arrayCode.zfill(6)))
    treeResults[th[step]] = tfileResults[th[step]].Get("results")

    treeResults[th[step]].GetEntry(0)

    peak_mean=np.array(treeResults[th[step]].peak1_mean_barCoinc)
    sigmaT=np.array(treeResults[th[step]].deltaT12_sigma_barCoinc)
    CTR=np.array(treeResults[th[step]].CTR_sigma_barCoinc)
    DT=np.array(treeResults[th[step]].CTR_mean_barCoinc)
    DT_0=np.array(treeResults[th[0]].CTR_mean_barCoinc)
    XT=np.array(treeResults[th[step]].Xtalk_median_barCoinc)
    
    histos['LY_vs_pos'].SetPoint(istep,th[step]*thscan_step,peak_mean[peak_mean>60].mean())
    histos['LY_vs_pos'].SetPointError(istep,0.5,peak_mean[peak_mean>60].std()/4.)
    histos['sigmaT_vs_pos'].SetPoint(istep,th[step]*thscan_step,sigmaT[sigmaT>0].mean()/2.)
    histos['sigmaT_vs_pos'].SetPointError(istep,0.5,sigmaT[sigmaT>0].std()/8.)
    histos['CTR_vs_pos'].SetPoint(istep,th[step]*thscan_step,CTR[CTR>0].mean())
    histos['CTR_vs_pos'].SetPointError(istep,0.5,CTR[CTR>0].std()/4.)
    histos['DT_vs_pos'].SetPoint(istep,th[step]*thscan_step,DT[DT>0].mean()-DT_0[DT_0>0].mean())
    histos['DT_vs_pos'].SetPointError(istep,0.5,DT[DT>0].std()/4.)
    histos['XT_vs_pos'].SetPoint(istep,th[step]*thscan_step,XT[XT>0].mean())
    histos['XT_vs_pos'].SetPointError(istep,0.5,XT[XT>0].std()/4.)
    istep+=1
    
##########################################

mergedLabel = str(opt.outputDir)+"/"+"tree_"+"FirstRun" + str(opt.firstRun.zfill(6)) + "_LastRun" + str((int(opt.firstRun)+(nFilesInScan-1)*3)).zfill(6) + "_ARRAY" + str(opt.arrayCode.zfill(6))

c1_LY = TCanvas("phe_peak", "phe_peak", 900, 700)     

c1_LY.cd()  
gStyle.SetOptStat(1111);
c1_LY.SetGrid();

t=TLatex()
t.SetTextSize(0.035)

out=TFile(mergedLabel+"_"+"THSCAN_SUMMARY.root","RECREATE")

for hh in ['LY','sigmaT','CTR', 'DT', 'XT']:
    histos['%s_vs_pos'%hh].GetXaxis().SetTitle("TH1 (mV)")
    if (hh=='LY'):
        histos['%s_vs_pos'%hh].GetYaxis().SetTitle("Energy (QDC)")
    elif (hh=='sigmaT'):
        histos['%s_vs_pos'%hh].GetYaxis().SetTitle("#sigma_{t} (ps)")
    elif (hh=='CTR'):
        histos['%s_vs_pos'%hh].GetYaxis().SetTitle("CTR (ps)")
    elif (hh=='DT'):
        histos['%s_vs_pos'%hh].GetYaxis().SetTitle("#DeltaT (ps)")
        histos['%s_vs_pos'%hh].GetXaxis().SetTitle("TH1 (mV)")
    elif (hh=='XT'):
        histos['%s_vs_pos'%hh].GetYaxis().SetTitle("XT")
    histos['%s_vs_pos'%hh].SetLineColor( 2 )
    histos['%s_vs_pos'%hh].SetMarkerColor( 1 )
    histos['%s_vs_pos'%hh].SetMarkerStyle( 21 )
    histos['%s_vs_pos'%hh].Draw("APE")
    if (hh=='LY'):
        histos['%s_vs_pos'%hh].GetYaxis().SetLimits(60,100)
        histos['%s_vs_pos'%hh].GetYaxis().SetRangeUser(60,100)
    elif (hh=='sigmaT'):
        histos['%s_vs_pos'%hh].GetYaxis().SetLimits(100,200)
        histos['%s_vs_pos'%hh].GetYaxis().SetRangeUser(100,200)
        histos['%s_vs_pos'%hh].Fit("sigmaTvsTH","BR+")
    elif (hh=='CTR'):
        histos['%s_vs_pos'%hh].GetYaxis().SetLimits(160,250)
        histos['%s_vs_pos'%hh].GetYaxis().SetRangeUser(160,250)
    elif (hh=='XT'):
        histos['%s_vs_pos'%hh].GetYaxis().SetLimits(0.,0.5)
        histos['%s_vs_pos'%hh].GetYaxis().SetRangeUser(0.,0.5)
    elif (hh=='DT'):
        histos['%s_vs_pos'%hh].Fit("pol2")
        f=histos['%s_vs_pos'%hh].GetFunction('pol2')
        t.DrawLatexNDC(0.6,0.15,"SR=%.3f mV/ns"%(1/f.Derivative(140)*1000))

    histos['%s_vs_pos'%hh].Write()
    c1_LY.SaveAs(mergedLabel+"_"+"THSCAN_SUMMARY_%s.png"%hh)

out.Close()
print(out.GetName()+' closed')
