#!/bin/bash

# mX=650
# mY=350
mX=700
mY=400
sig_tag="mx${mX}_my${mY}_2"
sig_name="sig_NMSSM_bbbb_MX_${mX}_MY_${mY}"

studies/pseudoDatasets_2024Jan/bin/createPsuedoDataset_localExcess_2024Jan ${sig_tag} ${sig_name}

