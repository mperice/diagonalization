
import numpy
import numpy as np

def matrix_factorization(R, P, Q, K, steps=50000, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in xrange(steps):
        print step
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))

        if e < 0.001:
            break
    return P, Q.T


R = [
     [5,3,0,1],
     [4,0,0,1],
     [1,1,0,5],
     [1,0,0,4],
     [0,1,5,4],
    ]


R2 = [
     [0,1,4,1],
     [0,0,3,2],
     [0,0,2,5],
     [0,0,1,4],
     [1,0,5,4],
    ]


R = numpy.array(R2)
R = np.loadtxt('init.dat', dtype = int)
q, r = np.linalg.qr(R)
print q, r

N = len(R)
M = len(R[0])
K = 100

print N,M,K

P = numpy.random.rand(N,K)
Q = numpy.random.rand(M,K)

#nP, nQ = matrix_factorization(R, P, Q, K)
from nmf import NMF
nmf_mdl = NMF(R, num_bases=2)
nmf_mdl.factorize( niter=10)
#nP, nQ = matrix_factorization(R, P, Q, K)
nP=nmf_mdl.W
nQ=nmf_mdl.H

print nP
print nQ
nR = numpy.dot(nP, nQ)
print nR


red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)

# from PIL import Image, ImageDraw
# im = Image.new("RGB", [len(col_perm_rev),len(row_perm_rev)], white)#Image.open("after_col_perm.pgm")
# draw = ImageDraw.Draw(im)
#
#
# #DRAW POINTS
# file=open(filename+".dat", 'r')
# line = file.readline()
#
# i=0
# while line:
#     orig_i=row_perm_rev[i]
#
#     draw.line(((0,i),(len(col_perm_rev),i)), fill=(255,200,200) if trains_class[orig_i]==classes[0] else (200,200,255))
#
#     for j,value in enumerate(line.split(" ")):
#         if value=="1":
#             new_j=col_perm_inv[j] if col_perm_inv else j
#             draw.point((new_j,i), fill=(red if trains_class[orig_i]==classes[0] else blue))
#     line = file.readline()
#     i+=1
# file.close()
#
# #DRAW GREEN LINES: B-TERMS
# for j,old_j in col_perm_rev.items():#enumerate(sorted_words):
#     word=sorted_words[old_j]
#     new_j=col_perm_inv[j] if col_perm_inv else j
#
#
#     if word in b_terms:
#         draw.line(((new_j,0),(new_j,len(row_perm_rev))), fill=(100,255,100))
#
# im.save(name+".png")


import matplotlib.pyplot as plt

def baryCentric(mat, steps):
	#mat.shape = (nRows, nColumns)
	ones0 = np.ones(mat.shape[1]); ones1 = np.ones(mat.shape[0]); range0 = np.arange(mat.shape[1]); range1 = np.arange(mat.shape[0]); rowper = range(mat.shape[0]); colper = range(mat.shape[1])
	stateDict = {False: [ones0, range0, rowper], True: [ones1, range1, colper]}
	state = False #tells if matrix is transposed
	for i in range(steps):
		num = np.dot(mat, stateDict[state][1])
		den = np.dot(mat, stateDict[state][0]) + 0.1
		baryCenters = num / den
		permutation = sorted(range(baryCenters.shape[0]), key = lambda i: [baryCenters[i], den[i]])
		#multiply stateDict[state][2] with permutation (from left)
		stateDict[state][2] = [stateDict[state][2][x] for x in permutation]
		if permutation == range(baryCenters.shape[0]):
			print "barycenters alined at i = %i" % i
			break
		mat = mat[permutation, :].transpose()
		state = not state
	if state:
		mat = mat.transpose()
	return [mat, stateDict[False][2], stateDict[True][2]]

print baryCentric(R, 2)[0]
matrix = baryCentric(R, 2)[0]
plt.pcolor(matrix, cmap = 'Greys')
plt.axis([0, matrix.shape[1], 0, matrix.shape[0]])
plt.gca().invert_yaxis()
plt.show()