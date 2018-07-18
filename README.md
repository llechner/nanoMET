# nanoMET
Repository to use nanoAOD tuples to tune MET Significance, and produce validation plots

Recipe:

```
cmsrel CMSSW_9_4_6
cd CMSSW_9_4_6/src
cmsenv
git cms-init
echo JetMETCorrections/Modules/ >> .git/info/sparse-checkout
git checkout
scram b -j 8

git clone https://github.com/schoef/RootTools.git
git clone https://github.com/danbarto/nanoMET.git
cd $CMSSW_BASE/src
cmsenv
```
