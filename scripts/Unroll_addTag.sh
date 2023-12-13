#!/bin/bash

tag="2023Dec7_binMYx2_addMX650"
addtag="10ev"
for ayear in 2016 2017; do
    idir="VarPlots/rootHists/fullSubmission_2022Nov/${ayear}DataPlots_${tag}"
    odir="${idir}_${addtag}"
    ls -ltrh ${idir}
    mkdir ${odir}
    mv "${idir}/outPlotter.root" "${odir}/"
    echo "${odir}"
    ls -ltrh ${odir}
done

