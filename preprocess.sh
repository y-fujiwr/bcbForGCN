#!/bin/bash
mv bcb_dataset/raw/43 bcb_dataset/raw/0
mv bcb_dataset/raw/44 bcb_dataset/raw/1
mv bcb_dataset/raw/45 bcb_dataset/raw/16
mv bcb_dataset/multi/43 bcb_dataset/multi/0
cp -r bcb_dataset/raw bcb_dataset/test
python preprocess.py