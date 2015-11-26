'''
Created on 9.4.2014

@author: Matic Perovsek
'''

import numpy
import sys
from collections import defaultdict 

def wALS(no_of_users,no_of_items,R, K=20, niters=50,w_factor=0.005, w_scheme="uniform",regularization_factor=0.002):
    """ wALS algorithm, returns factorization matrices P and Q of matrix R 
    
    Keyword arguments:
    R -- ratings matrix
    K -- number of features (default 20)
    niters -- number of iterations (default 100)
    
    """

    sys.stdout.flush()
    #initialize P and Q with small random numbers
    P = numpy.random.uniform(0.04,0.06,(no_of_users,K)) # NxK
    Q = numpy.random.uniform(0.04,0.06,(no_of_items,K)) # MxK
    
    wf_normalizer=1.
    if w_scheme=="item_oriented":
        item_count=defaultdict(int)
        for user in R:
            for item in R[user]:
                item_count[item]+=1
        wf_normalizer=max([no_of_users-item_count[item] for item in range(no_of_items)])
    elif w_scheme=="user_oriented":
        wf_normalizer=max([len(R[i]) for i in range(no_of_users)])
    

    iters=0
    cond=True
    while iters<niters and cond:
        iters+=1
        
        def update_P_row(i):
            """ Updates i-th row in matrix P """
            
            #set weights for negative examples
            user_row=numpy.zeros(no_of_items)
            W_hat_i=w_factor*numpy.eye(no_of_items)
            
            for item in range(no_of_items):
                if w_scheme=="user_oriented":
                    W_hat_i[item][item]+=(1-w_factor)*len(R[i])*1./wf_normalizer if i in R and len(R[i])>0 else 0.000000001
                elif w_scheme=="item_oriented":
                    W_hat_i[item][item]*=(no_of_users-item_count[item])*1./wf_normalizer
                    
            #set weights to 1 for positive examples    
            for item in R[i]:
                user_row[item]=1
                W_hat_i[item][item]=1

            #calculate new row
            W_i_sum=sum([W_hat_i[abc][abc] for abc in range(no_of_items)])
            W_hat_dot_Q=numpy.dot(W_hat_i,Q)
            
            inner_k_x_k=numpy.linalg.inv(numpy.dot(Q.T,W_hat_dot_Q)+regularization_factor*W_i_sum*numpy.eye(K))
            P[i,:]=numpy.dot(numpy.dot(user_row,W_hat_dot_Q),inner_k_x_k)
            
        def update_Q_row(j):
            """ Updates j-th row in matrix Q """
            
            #set weights for negative examples
            item_row=numpy.zeros(no_of_users)
            W_hat_j=w_factor*numpy.eye(no_of_users)
            #positive=0
            
            for user in range(no_of_users):
                if w_scheme=="user_oriented":
                    W_hat_j[user][user]+=(1-w_factor)*len(R[user])*1./wf_normalizer if user in R and len(R[user])>0 else 0.000000001
                elif w_scheme=="item_oriented":
                    W_hat_j[user][user]*=(no_of_users-item_count[j])*1./wf_normalizer
            
            #set weights to 1 for positive examples              
            for user in R:
                if j in R[user]:
                    item_row[user]=1
                    W_hat_j[user][user]=1

            #calculating new row
            W_j_sum=sum([W_hat_j[abc][abc] for abc in range(no_of_users)])
            W_hat_dot_P=numpy.dot(W_hat_j,P)
            
            inner_k_x_k=numpy.linalg.inv(numpy.dot(P.T,W_hat_dot_P)+regularization_factor*W_j_sum*numpy.eye(K))
            Q[j,:]=numpy.dot(numpy.dot(item_row,W_hat_dot_P),inner_k_x_k)    
            
        
        #update rows in P and Q for every user and item          
        map(update_P_row, xrange(no_of_users))
        map(update_Q_row, xrange(no_of_items))

        sys.stdout.flush()
    return P, Q



def RISMF(no_of_users,no_of_items,R, K=2, niters=150,learning_rate=0.2, regularization_factor=0.02):
    """ RISMF algorithm, returns factorization matrices P and Q of matrix R 
    
    Keyword arguments:
    R -- ratings matrix
    K -- number of features (default 20)
    niters -- number of iterations (default 100)
    learning_rate -- learning weight for every iteration (default 0.2)
    regularization_factor -- the wight of reqularization (default 0.02)
    
    """
    
    print "RISMF K="+str(K)  
    sys.stdout.flush()
    
    #initialize P and Q with small random numbers
    P = numpy.random.uniform(0.04,0.06,(no_of_users,K)) # NxK
    Q = numpy.random.uniform(0.04,0.06,(no_of_items,K)).T #(MxK).T
    
    
    previous_SSE_apos=999999999999 #initial big value
    iters=0 #iteration counter
    cond=True
    while iters<niters and cond:
        iters+=1
        
        #update P and Q for every example
        for u in R:
            for i in R[u]:
                #the error of rating u on i
                e_ui = 1. - numpy.dot(P[u,:],Q[:,i])
                #stohastic gradient descent
                for k in range(K):
                    gradient_p_uk= -e_ui * Q[k][i] + regularization_factor * P[u][k]
                    gradient_q_ki= -e_ui * P[u][k] + regularization_factor * Q[k][i]
                    P[u][k] = P[u][k] + learning_rate * (-gradient_p_uk)
                    Q[k][i] = Q[k][i] + learning_rate * (-gradient_q_ki)
                
        #calculate RMSE error
        SSE_apos = 0
        for u in R:
            for i in R[u]:
                #SSE_apos=sum of all e'_ui
              
                #calculate e'_ui
                SSE_apos = SSE_apos + pow(1.0 - numpy.dot(P[u,:],Q[:,i]), 2)
                for k in range(K):
                    SSE_apos = SSE_apos + (regularization_factor/2) * (pow(P[u][k],2) + pow(Q[k][i],2))
        
        #break if difference smaller than epsilon
        if previous_SSE_apos-SSE_apos < 0.000001:
            cond=False
            break
        previous_SSE_apos=SSE_apos
    return P, Q.T


def RISMF_AMAN(no_of_users,no_of_items,R, K=2, niters=150,learning_rate=0.2, regularization_factor=0.02):
    print "RISMF K="+str(K)#,iters,SSE_apos    
    sys.stdout.flush()
    #initialize P and Q with small random numbers
    P = numpy.random.uniform(0.04,0.06,(no_of_users,K)) # NxK
    Q = numpy.random.uniform(0.04,0.06,(no_of_items,K)).T #(MxK).T
    
    #print P,Q
    
    previous_SSE_apos=999999999999
    iters=0
    cond=True
    while iters<niters and cond:
        iters+=1        
        for u in range(no_of_users):
            for i in range(no_of_items):
                in_training_set=u in R and i in R[u]
                r_ui=1. if in_training_set else 0.
                #the error of rating u on i
                e_ui = r_ui - numpy.dot(P[u,:],Q[:,i])
                #stohastic gradient descent
                for k in range(K):
                    gradient_p_uk= -e_ui * Q[k][i] + regularization_factor * P[u][k]
                    gradient_q_ki= -e_ui * P[u][k] + regularization_factor * Q[k][i]
                    P[u][k] = P[u][k] + learning_rate * (-gradient_p_uk)
                    Q[k][i] = Q[k][i] + learning_rate * (-gradient_q_ki)
            
        #print len(R)
        eR = numpy.dot(P,Q)
        SSE_apos = 0
        for u in range(no_of_users):
            for i in range(no_of_items):
                in_training_set=u in R and i in R[u]
                r_ui=1. if in_training_set else 0.
                #SSE_apos=sum of all e'_ui
                
                #calculate e'_ui
                SSE_apos = SSE_apos + pow(r_ui - numpy.dot(P[u,:],Q[:,i]), 2)
                for k in range(K):
                    SSE_apos = SSE_apos + (regularization_factor/2) * (pow(P[u][k],2) + pow(Q[k][i],2))

        if previous_SSE_apos-SSE_apos < 0.0001:
            cond=False
            break
        previous_SSE_apos=SSE_apos
    return P, Q.T