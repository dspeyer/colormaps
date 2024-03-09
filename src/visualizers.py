from collections import namedtuple, defaultdict

import cv2
import numpy as np

from globalvars import names, nnames, numbyname, blurSide
from mappers import UnusedPxException

class PotentialFootnote:
    def __init__(self):
        self.size = 0
        self.places = []

def inscribed(c,w,h):
    scratch = np.zeros((w,h),dtype=np.uint8)
    cv2.drawContours(scratch, [c], 0, 255, -1)
    scratch[0,:] = 0
    scratch[-1,:] = 0
    scratch[:,0] = 0
    scratch[:,-1] = 0
    dt = cv2.distanceTransform(scratch, cv2.DIST_L1, 3, cv2.DIST_LABEL_CCOMP)
    mx = np.argmax(dt)
    center = (mx//h, mx%h)
    r = dt.astype(np.int32)[center]
    return center, r


class Visualizer:
    def __init__(self, mapper):
        self.mapper = mapper
        w = mapper.w
        h = mapper.h
        canvas = np.zeros((w,h,3), dtype=np.uint8)
        self.mask = np.zeros((w,h), dtype=np.uint8)
        for x in range(w):
            for y in range(h):
                try:
                    canvas[x,y,:] = mapper.colFromPx(x,y)
                    self.mask[x,y] = 1
                except UnusedPxException:
                    continue
        if hasattr(self.mapper, 'eschew_footnotes'):
            self.labelmask = cv2.erode(1-self.mask, np.ones((51, 5), np.uint8))
        m = mapper.multiplier
        self.canvas = cv2.resize(canvas, dsize=None, fx=m, fy=m, interpolation=cv2.INTER_CUBIC)
        self.textnotes = []
        self.footnotes = defaultdict(PotentialFootnote)
        self.linenotes = {}
        
    def labelColors(self, data, maj, minfont):
        m = self.mapper.multiplier
        w = self.mapper.w
        h = self.mapper.h
        for i in range(nnames):
            if maj:
                iscol = (data.countRats[:,:,i] > .5).astype(np.uint8)
            else:
                iscol = (data.best == i).astype(np.uint8)
            iscol *= self.mask
            if not np.any(iscol):
                continue
            contours, _ = cv2.findContours(iscol, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            lc = self.mapper.linecolor
            cv2.drawContours(self.canvas, np.array(contours)*m, -1, (lc,lc,lc), 1+maj)
            for c in contours:
                (cx,cy), rad = inscribed(c,w,h)
                if not np.all(iscol[cx,cy]):
                    continue
                if rad * m > len(names[i]) * minfont:
                    self.delayedPutText(cx, cy, rad, names[i])
                elif rad * m > 2 * minfont:
                    if not hasattr(self.mapper, 'eschew_footnotes'):
                        self.delayedPutFootnote(cx, cy, rad, names[i])
                    else:
                        self.delayedPutLinenote(cx, cy, names[i], lc)

    def topoColors(self, data, colorsToTopo):
        m = self.mapper.multiplier
        w = self.mapper.w
        h = self.mapper.h
        LabelPos = namedtuple('LabelPos', ('c', 'rad', 'thr'))
        for cn in colorsToTopo:
            col = numbyname[cn]
            best = LabelPos(None, 0, 0)
            for thr in [0.05] + [i/10 for i in range(1,10)] + [.95, .99]:
                iscol = data.countRats[:,:,col] > thr
                iscol = iscol.reshape(w,h).astype(np.uint8)
                if not np.any(iscol):
                    break
                contours, _ = cv2.findContours(iscol, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                lc = self.mapper.linecolor
                cv2.drawContours(self.canvas, np.array(contours)*m, -1, (lc,lc,lc), 1)
                for c in contours:
                    for p in range(0,len(c),50):
                        self.delayedPutText(c[p][0][1], c[p][0][0], 5, '%d%%'%(thr*100), lc)
                    center, rad = inscribed(c, w, h)
                    if rad > best.rad or (rad>10 and thr>best.thr):
                        best = LabelPos(center, rad, thr)
            if best.rad > 0:
                self.delayedPutText(best.c[0], best.c[1], best.rad, cn, lc)

    def addGraph(self, data, p1, p2):
        m = self.mapper.multiplier
        w = self.mapper.w
        h = self.mapper.h
        lc = self.mapper.linecolor
        colToLab = {}
        p1 = np.array(p1, dtype=float)
        p2 = np.array(p2, dtype=float)
        cv2.line(self.canvas, (p1[::-1]*m).astype(np.int32), (p2[::-1]*m).astype(np.int32), (lc,lc,lc), 1)
        for i in range(256):
            p = np.round((p2 * i + p1 * (256-i)) / 256).astype(np.int32)
            c = np.array(self.mapper.colFromPx(*p), dtype=np.uint8)
            #print(c)
            b = data.best[p[0],p[1]]
            #print('best ' + names[b])
            #print('count %s : %f' % (names[b], counts[p[0]+blurSide//2, p[1]+blurSide//2, b]))
            #if i==255:
            
            #print(list(zip(names, data.countRats[p[0],p[1]])))
            self.canvas[-256*m:,(256+i)*m:(257+i)*m,:] = c
            for cn in np.where(data.countRats[p[0],p[1]] > 0.1)[0]:
                v = int(data.countRats[p[0],p[1],cn]*256)
                #print('count %s : %f' % (names[cn], counts[p[0]+blurSide//2, p[1]+blurSide//2, cn]))
                if int(cn) not in colToLab or v > colToLab[int(cn)][1]:
                    #print(names[cn])
                    colToLab[int(cn)] = (i,v)
        #print('---')
        for i,(cn,(mx,my)) in enumerate(colToLab.items()):
            #print(names[cn])
            ic = [lc,lc,lc]
            if hasattr(self.mapper, 'o'):
                ic[self.mapper.o] = (255*i)//len(colToLab)
            for i in range(255):
                p = np.round((p2*i + p1*(256-i)) / 256).astype(np.int32)                
                pn = np.round((p2*(i+1) + p1*(255-i)) / 256).astype(np.int32)
                v = int(data.countRats[p[0],p[1],cn]*256)
                vn = int(data.countRats[pn[0],pn[1],cn]*256)
                cv2.line(img=self.canvas, pt1=((256+i)*m, (512-v)*m), pt2=((256+i+1)*m, (512-vn)*m), color=tuple(ic), thickness=2)
            tw = cv2.getTextSize(names[cn], cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0][0]
            mxp = (256+mx)*m - tw//2
            if mxp + tw > 512*m:
                mxp = 512*m - tw
            if mxp < 256*m:
                mxp = 256*m
            cv2.putText(self.canvas, names[cn], (mxp, (512-my)*m), cv2.FONT_HERSHEY_SIMPLEX, 1, ic, 1, cv2.LINE_AA)

                
    def finalize(self):
        w = self.mapper.w
        h = self.mapper.h
        m = self.mapper.multiplier
        if not hasattr(self.mapper, 'eschew_footnotes'):
            self.canvas[-(256*m):,:(256*m),:] = 0
            keep = list(sorted(self.footnotes.items(), key=lambda x:-x[1].size))
            keep = keep[:24]
            for fn, (txt, nt) in enumerate(keep):
                fnx = (fn * 128 // m) % 256
                fny = 64 * (1 + fn//(m*2))
                self.delayedPutText(fnx+(w-256)+16, fny, 20, '%X=%s'%(fn,txt), 255)
                for x,y,s in nt.places:
                    self.delayedPutText(x, y, s, '%X'%fn)
        for x,y,s,txt,c in self.textnotes:
            if  txt: 
                cv2.putText(self.canvas, txt, (y*m-3*s, x*m+s), cv2.FONT_HERSHEY_SIMPLEX, m*s/(10*len(txt)), (255-c,255-c,255-c), s//10+2, cv2.LINE_AA)
                cv2.putText(self.canvas, txt, (y*m-3*s, x*m+s), cv2.FONT_HERSHEY_SIMPLEX, m*s/(10*len(txt)), (c,c,c), s//10, cv2.LINE_AA)

    def save(self, fn):
        cv2.imwrite(fn, self.canvas[:,:,::-1])


    def show(self):
        import matplotlib.pyplot as plt
        plt.imshow(self.canvas)
        plt.show()

            
    def delayedPutText(self, x, y, s, txt, tc=None):
        m = self.mapper.multiplier
        if tc is None:
            col = self.canvas[x*m,y*m]
            if np.sum(col.astype(np.int32)) >= self.mapper.ct:
                tc = 0
            else:
                tc = 255
        self.textnotes.append((x,y,s,txt,tc))

    def delayedPutFootnote(self, x, y, s, txt):
        self.footnotes[txt].places.append((x,y,s))
        self.footnotes[txt].size += s ** 2

    def delayedPutLinenote(self, x, y, txt, lc):
        h = self.mapper.h
        w = self.mapper.w
        m = self.mapper.multiplier
        if txt not in self.linenotes:
            dot = self.mask * 0 +1
            dot[x,y]=0
            closeness = (h+w) - cv2.distanceTransform(dot, cv2.DIST_L2, 3, cv2.DIST_LABEL_CCOMP)
            closeness *= self.labelmask
            out = np.argmax(closeness)
            outx = out // h
            outy = out % h
            if closeness[outx,outy] == 0:
                print('Failed to find a space for linenote '+txt)
                return
            self.delayedPutText(outx, outy, 10, txt, 255)
            cv2.circle(self.labelmask, (outy,outx), len(txt)*3, 0, -1)
            self.linenotes[txt] = (outx, outy)
        else:
            (outx, outy) = self.linenotes[txt]
        cv2.line(self.canvas, (y*m,x*m), (outy*m,outx*m), (255,255,255), 1)

