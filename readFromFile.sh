#!/bin/bash

cnt=0
while IFS= read -r line; do
    echo "Downloading: $line"
    let cnt++
    rucio download --rse T1_US_FNAL_Disk cms:$line
done < "$1"
echo "Number of files downloaded: $cnt"

# execute setupRucio (alias in .profile) first
# Notes: run with ./readFromFile.sh dataset_files.txt
