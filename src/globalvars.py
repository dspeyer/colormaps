import sys
import os

import sqlite3
import numpy as np
import cv2

path = os.path.dirname(sys.argv[0])

conn = sqlite3.connect(path + '/xkcd.sqllite')

names = conn.execute('select * from (select colorname, count(*) as cnt from answers group by colorname) where cnt > 200').fetchall()

names = [x[0] for x in names]
numbyname = {n:i for i,n in enumerate(names)}
nnames = len(names)

blurRad = 16
blurSide = 2 * blurRad + 1
g1 = cv2.getGaussianKernel(blurSide, blurRad)
g2 = g1 @ g1.transpose()

