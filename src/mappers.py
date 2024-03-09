import numpy as np

class UnusedPxException(Exception):
    pass

class FullSat:
    @staticmethod
    def pxFromCol(r,g,b):
        if r == 0:
            return 255-g, b+256
        if g == 0:
            return r+256, b+256
        if b == 0:
            return 255-g, 255-r
        raise UnusedPxException()

    @staticmethod
    def colFromPx(x,y):
        if y >= 256:
            if x <= 255:
                return 0, 255-x, y-256
            else:
                return x-256, 0, y-256
        else:
            if x <= 255:
                return 255-y, 255-x, 0
            else:
                raise UnusedPxException()

    @staticmethod
    def where():
        return 'r=0 or g=0 or b=0'

    w = 511
    h = 511
    fn = 'fullsat'
    ct = 256
    linecolor = 255
    multiplier = 4
    

class Pastel:
    @staticmethod
    def pxFromCol(r,g,b): 
        if r == 255:
            return b, g
        if g == 255:
            return b, 510-r
        if b == 255:
            return 510-g, 510-r
        raise UnusedPxException()

    @staticmethod
    def colFromPx(x,y):
        if y >= 256:
            if x < 256:
                return 510-y, 255, x
            else:
                return 510-y, 510-x, 255
        else:
            if x < 256:
                return 255, y, x
            else:
                raise UnusedPxException()

    @staticmethod
    def where():
        return 'r=255 or g=255 or b=255'

    w = 510
    h = 510
    fn = 'pastel'
    ct = 0
    linecolor = 0
    multiplier = 4

class Slice:
    mtx = np.array([[.5, -0.25, -0.25], [0, np.sqrt(3)/4, -np.sqrt(3)/4], [1, 1, 1]], dtype=float)

    def __init__(self, s, m=4):
        self.s=s
        if s > 384:
            self.linecolor=0
        else:
            self.linecolor=255
        self.fn = 'slice%03d_%d' % (s, self.w*m)
        self.multiplier = m


    def pxFromCol(self, *c):
        c = np.array(c)
        p = np.round(self.mtx @ c).astype(np.int32)
        if p[2]!=self.s:
            raise UnusedPxException()        
        return tuple((p[:2]+128).astype(np.int32))
        
    def colFromPx(self,x,y):
        if x>256:
            raise UnusedPxException()            
        p = np.array([x-128, y-128, self.s], dtype=float)
        col = np.round(np.linalg.inv(self.mtx) @ p)
        if np.any(col>255) or np.any(col<0):
            raise UnusedPxException()
        return tuple(col.astype(np.uint8))

    def where(self):
        return 'r + g + b = %d' % self.s
    
    w = 256
    h = 256
    ct = 256
    eschew_footnotes = True
    
class Primary:
    def __init__(self,which):
        self.which = which
        self.o1 = (which+1)%3
        self.o2 = (which+2)%3
        self.fn = 'primary%d' % self.which
        
    def pxFromCol(self, *data):
        if data[self.o1] != data[self.o2]:
            raise UnusedPxException()
        return data[self.which], data[self.o1]

    def colFromPx(self, x, y):
        if x>255 or y>255:
            raise UnusedPxException()            
        o=[0,0,0]
        o[self.which]=x
        o[self.o1]=y
        o[self.o2]=y
        return tuple(o)

    def where(self):
        ns='rgb'
        return f'{ns[self.o1]}={ns[self.o2]}'

    w = 512
    h = 256
    ct = 256
    linecolor = 0
    multiplier = 8        
    

class ParPlane:
    def __init__(self,which,val):
        self.which = which
        self.o1 = (which+1)%3
        self.o2 = (which+2)%3
        self.val = val
        self.fn = 'ParPlane%d_%d' % (self.which,self.val)
        
    def pxFromCol(self, *data):
        if data[self.which] != self.val:
            raise UnusedPxException()
        return data[self.o1], data[self.o2]

    def colFromPx(self, x, y):
        if x>255 or y>255:
            raise UnusedPxException()            
        o=[0,0,0]
        o[self.which]=self.val
        o[self.o1]=x
        o[self.o2]=y
        return tuple(o)

    def where(self):
        ns='rgb'
        return f'{ns[self.which]}={self.val}'

    w = 512
    h = 256
    ct = 256
    linecolor = 0
    multiplier = 8


class Edge:
    def __init__(self, p, s):
        self.p = p
        self.s = s
        self.o = 3-p-s
        self.fn = 'edge%d%d' % (p,s)

    def colFromPx(self,x,y):
        if x > 256:
            raise UnusedPxException()
        c = np.zeros(3, dtype=np.uint8)
        if x+y<256:
            c[self.p] = 255-x
            c[self.s] = 0
            c[self.o] = 255-x-y
        elif y<256:
            c[self.p] = y
            c[self.s] = x+y-256
            c[self.o] = 0
        elif x+y<512:
            c[self.p] = 255
            c[self.s] = x+y-256
            c[self.o] = y - 256
        else:
            c[self.p] = 767-x-y
            c[self.s] = 255
            c[self.o] = 255 - x
        return tuple(c)

    def pxFromCol(self, *c):
        x,y = self.pxFromColTrue(*c)
        if x<0 or y<0 or x>256 or y>512:
            raise UnusedPxException()
        return x,y
        
    def pxFromColTrue(self, *c):
        c = np.array(c, dtype=np.int32)
        if c[self.s] == 0:
            return 255-c[self.p], c[self.p]-c[self.o]
        elif c[self.s] == 255:
            return 255-c[self.o], c[self.o]-c[self.p]+512
        elif c[self.o] == 0:
            return c[self.s]-c[self.p]+256, c[self.p]
        elif c[self.p] == 255:
            return c[self.s]-c[self.o], c[self.o]+256
        else:
            raise UnusedPxException()            

    def where(self):
        ns='rgb'
        return f'{ns[self.p]}=255 or {ns[self.o]}=0 or {ns[self.s]}=0 or {ns[self.s]}=255'
    
    w = 512
    h = 512
    ct = 256
    linecolor = 0
    multiplier = 4
    
    
class Orange:
    def pxFromCol(self, *data):
        if data[0] // 2 != data[1]:
            raise UnusedPxException()
        return data[0], data[2]*2

    def colFromPx(self, x, y):
        if x>255 or y>510:
            raise UnusedPxException()            
        o=[0,0,0]
        o[0]=x
        o[1]=x/2
        o[2]=y/2
        return tuple(o)

    def where(self):
        return 'floor(r/2)=g and colorname!="orange" and colorname!="brown" and colorname!="blue" and colorname!="purple" and colorname!="pink"'

    fn = 'orange'
    w = 512
    h = 510
    ct = 256
    linecolor = 0
    multiplier = 8
