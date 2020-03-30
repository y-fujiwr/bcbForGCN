import os,shutil
from pathlib import Path
import random

random.seed(0)

for i in range(43):
    filelist = list(Path(f"bcb_dataset/test/{i}").glob("**/*.java"))
    traindata = random.sample(filelist,int(len(filelist)*4/5))
    os.makedirs(f"bcb_dataset/train/{i}",exist_ok=True)
    for d in traindata:
        shutil.move(str(d),f"bcb_dataset/train/{i}/")

