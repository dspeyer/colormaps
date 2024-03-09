# I'm saving this code, but it doesn't work very well

import sklearn.decomposition
import numpy as np

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

class OneColor:
    def __init__(self, cn):
        self.colorname = cn
        data = np.array(list(conn.execute('select r,g,b from answers where colorname="%s"' % cn)), dtype=np.uint8)
        self.mean = np.average(data, axis=0)
        minc = np.percentile(data, 5, axis=0)
        maxc = np.percentile(data, 95, axis=0)
        self.mn = np.clip(minc - (self.mean - minc), 0, 255)
        self.mx = np.clip(maxc + (maxc - self.mean), 0, 255)
        if np.average(self.mean) < 128:
            self.linecolor = 255
        else:
            self.linecolor = 0
        self.fn = 'OneColTrio%s' % (self.colorname.replace(' ','_'))
            
    def pxFromCol(self, *col):
        col = np.array(col, dtype=float)
        col -= self.mn
        col *= 254.0 / (self.mx - self.mn)
        col = np.round(col)
        if np.any(col>255) or np.any(col<0):
            raise UnusedPxException()
        col = col.astype(np.uint32)
        out = []
        if col[0]>118 and col[0]<138:
            out.append(tuple(col[1:]))
        if col[1]>118 and col[1]<138:
            out.append((col[0], col[2]+256))
        if col[2]>118 and col[2]<138:
            out.append(tuple(col[:2]+256))
        if len(out):
            return out
        else:
            raise UnusedPxException()            

    def colFromPx(self, x, y):
        if x<255 and y<255:
            col = np.array([128.0,x,y])
        elif x<255 and y>=256:
            col = np.array([x, 128.0, y-256])
        elif x>=256 and y>=256:
            col = np.array([x-256, y-256, 128.0])
        else:
            raise UnusedPxException()
        col *= (self.mx - self.mn) / 254.0
        col += self.mn
        col = np.round(col)
        if np.any(col<0) or np.any(col>255):
            raise UnusedPxException()
        return tuple(col.astype(np.uint8))

    def where(self):
        return f'r>={self.mn[0]} and r<={self.mx[0]} and g>={self.mn[1]} and g<={self.mx[1]} and b>={self.mn[2]} and b<={self.mx[2]}'

    def carveVotes(self, votes, blurRad):
        votes[:,255+blurRad,:] = 0
        votes[255+blurRad,:,:] = 0
    
    w = 512
    h = 512
    ct = 256
    multiplier = 4
