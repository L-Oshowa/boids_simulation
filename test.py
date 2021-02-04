import numpy as np

class Test :
    def __init__(self,x,y) :
        self.x = x
        self.y = y
        self.xx = x**2
        self.yy = y**2
    def show(self) :
        txt = '(x,y) = ({},{})'
        print(txt.format(self.x,self.y))

size = 5
l_test = [Test(x,y) for x in range(size) for y in range(size)]
ll_binn = [[{t for t in l_test if t.x%2==x and t.y%2==y}for y in range(2)]for x in range(2)]

for l_b in ll_binn[0:1] : 
    for b in l_b[0:1] : 
        for t in b :
            t.show()