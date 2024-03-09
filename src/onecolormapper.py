# I'm saving this code, but it doesn't work very well

import sklearn.decomposition
import numpy as np

from globalvars import conn
from mappers import UnusedPxException

class OneColorPCA:
    def __init__(self, cn):
        self.colorname = cn
        data = np.array(list(conn.execute('select r,g,b from answers where colorname="%s"' % cn)), dtype=np.uint8)
        self.mean = np.average(data, axis=0)
        dc = data - self.mean
        pca = sklearn.decomposition.PCA()
        pca.fit(dc)
        self.mtx = pca.components_
        tr = (self.mtx @ dc.transpose()).transpose()
        self.sc = [384.0, 192.0] / (np.percentile(tr[:,:2], 99) - np.percentile(tr[:,:2], 1))
        self.limit = max(np.percentile(tr[:,2], 80), -np.percentile(tr[:,2], 20))
        if np.average(self.mean) < 128:
            OneColorPCA.linecolor = 255
        fn = 'OneCol%s' % (self.colorname.replace(' ','_'))
            
    def pxFromCol(self, *color):
        col = np.array(color, dtype=float)
        col -= self.mean
        tr = self.mtx @ col
        if np.abs(tr[2]) > self.limit:
            raise UnusedPxException()
        tr = tr[:2]
        tr *= self.sc
        tr += [256, 128]
        tr = np.round(tr)
        if tr[0]<0 or tr[0]>512 or tr[1]<0 or tr[1]>256:
            raise UnusedPxException()
        tr = tr.astype(np.int32)
        return (tr[1], tr[0])

    def colFromPx(self, x, y):
        if x > 256:
            raise UnusedPxException()
        px = np.array([y,x], dtype=float)
        px -= [256, 128]
        px /= self.sc
        tr = np.zeros(3, dtype=float)
        tr[:2]=px
        col = np.linalg.inv(self.mtx) @ tr
        col += self.mean
        col = np.round(col)
        if np.any(col<0) or np.any(col>255):
            raise UnusedPxException()
        return tuple(col.astype(np.uint8))

    def where(self):
        return '1=1'

    w = 512
    h = 512
    ct = 256
    linecolor = 0
    multiplier = 8
