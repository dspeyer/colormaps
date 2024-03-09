#!/usr/bin/python

import numpy as np
import sys
import os
import cv2

from globalvars import path, conn, names, nnames, numbyname, blurSide, g2
from mappers import UnusedPxException, FullSat, Pastel, Slice, Primary, ParPlane, Edge, Orange
from visualizers import Visualizer

class Data:
    def __init__(self, mapper, ratios=False, localmax=False):
        w, h = mapper.w, mapper.h
        counts = np.zeros((w+blurSide,h+blurSide,nnames), dtype=float)
        query = 'select colorname, r, g, b from answers where '+mapper.where()
        for name, r, g, b in conn.execute(query):
            if name not in names:
                continue
            c = numbyname[name]
            try:
                x,y = mapper.pxFromCol(r,g,b)
                counts[x:x+blurSide, y:y+blurSide, c] += g2
            except UnusedPxException:
                continue

        if localmax:
            ks = 201 # Chosen by messing around until it looked good
            for c in range(counts.shape[2]):
                counts[:,:,c] -= 1.5 * cv2.GaussianBlur(counts[:,:,c], (ks,ks), ks//2, ks//2)

        self.best = np.argmax(counts, axis=2)
        self.best = self.best[blurSide//2:-blurSide//2, blurSide//2:-blurSide//2]

        if ratios:
            countSnip = counts[blurSide//2:-blurSide//2, blurSide//2:-blurSide//2]
            cw,ch,cd = countSnip.shape
            cs = countSnip.sum(axis=2)
            cs = cs.reshape(cw,ch,1)
            self.countRats = countSnip / cs
        

def doTheThing(opts, p1=None, p2=None, maj=False, colorsToTopo=None, localmax=False):
    data = Data(opts, ratios=(p1 or colorsToTopo or maj), localmax=localmax)
    v = Visualizer(opts)
    if colorsToTopo:
        v.topoColors(data, colorsToTopo)
    else:
        minfont = (localmax and 2 or 4)  * (hasattr(opts,'eschew_visualizations') and 4 or 1)
        v.labelColors(data, maj, minfont)
    if p1 is not None:
        v.addGraph(data, p1, p2)
    v.finalize()
    fn = f'{path}/../results/{opts.fn}'
    if colorsToTopo:
        fn += '_topo_'
        fn += '_'+''.join(colorsToTopo).replace(' ','')
    elif localmax:
        fn += '_localmax'
    elif maj:
        fn += '_majority'
    else:
        fn += '_plurality'
    if p1:
        fn += '_withgraph'
    fn += '.png'
    print(f'saving as {fn}')
    v.save(fn)

if __name__ == '__main__':
    for mp in [ FullSat(), Pastel(), Slice(256,8), Slice(384,8), Slice(512,8) ]:
        doTheThing(mp)
        doTheThing(mp, localmax=True)
        doTheThing(mp, maj=True)
    for c in range(3):
        for v in [64,128,192]:
            doTheThing(ParPlane(c,v))
        doTheThing(Primary(c))
    doTheThing(Edge(1,0), (19,240), (180, 331))
    doTheThing(Edge(1,2), (230,200), (48, 430))
    doTheThing(Edge(0,2), (193,103), (226, 361))
    for i in range(16, 3*256-16, 16):
        doTheThing(Slice(i))
    doTheThing(Slice(384), colorsToTopo=['brown','grey'])
    doTheThing(Slice(384), colorsToTopo=['red','mustard','lime','teal','purple'])
    doTheThing(Slice(384), colorsToTopo=['blue','green','orange','pink'])
    doTheThing(FullSat(), colorsToTopo=['orange','brown','teal','purple'])
    doTheThing(FullSat(), colorsToTopo=['cyan','yellow','pink','black'])
    doTheThing(FullSat(), colorsToTopo=['red','green','blue'])
    doTheThing(Orange())
    
