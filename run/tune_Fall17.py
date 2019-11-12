"""
Tuning of Run2016
"""

# Standard imports
import ROOT
import os
import sys
import math
import copy
import itertools
import json
import random
import pickle

from RootTools.core.standard      import *

from nanoMET.core.JetResolution   import JetResolution
from nanoMET.tools.cutInterpreter import cutInterpreter
from nanoMET.tools.metFilters     import getFilterCut

from run import run

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',                      action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'])
argParser.add_argument('--pTdependent',                   action='store_true', help='run pT dependent METSig tuning', )
argParser.add_argument('--maxSig',                        action='store',      type=float, default=25 )
argParser.add_argument('--jetThreshold',                  action='store',      type=float, default=15 )
argParser.add_argument('--ttbarModifier',                 action='store',      type=float, default=1. )
args = argParser.parse_args()

# Logger
import nanoMET.tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

postProcessing_directory = "2017_v21/dimuon/"
from nanoMET.samples.nanoTuples_Fall17_postProcessed import *

# define setting
selection       = "diMuon-looseLeptonVeto-onZ-BadEEJetVeto"
samples         = [DY_LO_17, Top_17, diboson_17, rare_17]
trigger         = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ", "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8", "HLT_IsoMu27"]
jer             = "Fall17_V3_MC"
METPtVar        = "METFixEE2017_pt"
METPhiVar       = "METFixEE2017_phi"
JetCollection   = "Jet_pt_nom"
vetoEtaRegion   = (2.65,3.14)

# calculate setting
preselection    = cutInterpreter.cutString(selection)
triggerSel      = "(%s)"%"||".join(["Alt$(%s,0)"%trigg for trigg in trigger])
eventfilter     = getFilterCut( 2017, isData=False )
sel             = "&&".join([preselection, triggerSel, eventfilter])
JR              = JetResolution(jer)
version         = postProcessing_directory.split("/")[0]
outfile         = "results/tune_%s_%s_puWeight_sumPt%i_max%i_ttbar%i_%s"%(jer,selection,args.jetThreshold,args.maxSig,args.ttbarModifier,version)

r  = run(samples, sel, JR, outfile=outfile, METPtVar=METPtVar, METPhiVar=METPhiVar, JetCollection=JetCollection, maxN=3e5, vetoEtaRegion=vetoEtaRegion, jetThreshold=args.jetThreshold, puWeight="puWeight", ttbarModifier=args.ttbarModifier, pTdepMetSig=args.pTdependent)
LL = r.getLL(r.defaultStart)
r.minimize(start=r.defaultStart, maxSig=args.maxSig)

