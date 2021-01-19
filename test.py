import numpy as np

class Test :
    def __init__(self,x,y) :
        self.x = x
        self.y = y
        self.xx = x**2
        self.yy = y**2

l_test = [Test(x,y) for x in range(3) for y in range(3)]
binn = set()
for test in l_test :
    if test.x != 1 :
        binn.add(test)
        if test.y  == 1 :
            binn.remove(test)
print('l_test : '+str(len(l_test))+' binn : '+str(len(binn))+'\n boucle sur l_test :' )
for test in l_test :
    print('(x,y) = ('+str(test.x)+','+str(test.y)+')')
    print('is in binn : ' + str(test in binn))

print('boucle sur binn')
for test in binn :
    print('(x,y) = ('+str(test.x)+','+str(test.y)+')')
    test.x = 10
    test.y = 10

print('boucle sur l_test')
for test in l_test :
    print('(x,y) = ('+str(test.x)+','+str(test.y)+')')
    print('is in binn : ' + str(test in binn))

rng = np.random.default_rng()
print([rng.random(2) for ii in range(3)])
