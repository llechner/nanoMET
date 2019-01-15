'''
Tuning of Run2016
'''

# Standard imports
import ROOT
import os
import sys
import math
import copy
import itertools
import json
import random

from RootTools.core.standard    import *

from nanoMET.core.JetResolution import JetResolution

from Samples.Tools.metFilters   import getFilterCut

from run import run

postProcessing_directory = "2017_v6/dimuon/"
from nanoMET.samples.nanoTuples_Fall17_postProcessed import *

# define the selection
preselection    = "Sum$(Jet_pt>30&&Jet_jetId&&abs(Jet_eta)<2.4)>=0 && Sum$(Muon_pt>25&&Muon_isGoodMuon)==2 && Sum$(Electron_pt>10&&abs(Electron_eta)<2.5&&Electron_cutBased>0&&abs(Electron_pfRelIso03_all)<0.4)==0 && abs(dl_mass-91.2)<10"
trigger         = "( %s )"%" || ".join(['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ', 'HLT_IsoMu27', 'HLT_IsoTkMu27'])
eventfilter     = getFilterCut( 2017, isData=False)
sel             = " && ".join([preselection,trigger,eventfilter])

JR = JetResolution('Summer16_25nsV1_MC')

## only run over max 1M event per sample, uncertainty is anyway low. Need to confirm that the parameters really converged then.
#DoubleMuon_Run2016.reduceFiles(to=3)
r = run([DY_LO_17, Top_17, VVTo2L2Nu_17, WJets_17], sel, JR, outfile="results/tune_Fall17_incl_v3", maxN=1e6)

LL = r.getLL( [1.0, 1.0, 1.0, 1.0, 1.0, 0., .5] )

r.minimize()
