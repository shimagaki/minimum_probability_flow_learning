''' Version 1.000

 Code provided by Daniel Jiwoong Im
 http://www.cs.uoguelph.edu/~imj

 Permission is granted for anyone to copy, use, modify, or distribute this
 program and accompanying programs and documents for any purpose, provided
 this copyright notice is retained and prominently displayed, along with
 a note saying that the original programs are available from our
 web page.
 The programs and documents are distributed without any warranty, express or
 implied.  As the programs were written for research purposes only, they have
 not been tested to the degree that would be advisable in any important
 application.  All use of these programs is entirely at the user's own risk.'''

'''Demo of Factored Minimum Probability Flow learning algorithm 
connectivities on Restricted Boltzmann Machines. 
For more information, see :http://arxiv.org/abs/1412.6617
'''

import numpy as np
import timeit, pickle, sys
import theano
import theano.tensor as T
import os
import signal, sys
import matplotlib as mp
import matplotlib.pyplot as plt

from rbm_mpf import *
from mpf_optimizer import *
from utils import *


'''Train Restricted Boltzmann Machines'''
def train_rbm(train_data, valid_data, hyper_params, mpf_type='1bit', steps=25):

    batch_sz, epsilon, lam, num_hid, N, Nv, D, num_epoches= hyper_params
    hyper_params = [batch_sz, epsilon, lam]

    numpy_rng = numpy.random.RandomState()
    rbm = RBM_MPF(n_visible=D, n_hidden=num_hid, batch_sz=batch_sz, numpy_rng=numpy_rng, mpf_type=mpf_type)
    trainer = MPF_optimizer(hyper_params)

    num_batches = N / batch_sz
    train_set = theano.shared(train_data)
    valid_set = theano.shared(valid_data)
    train_update, get_valid_cost = trainer.mpf_MBGD(rbm, train_set, valid_set, reg_type='l2')

    ## Initialize the connectivities
    XX = T.matrix('X'); K=T.iscalar('s');
    v_samples, v_means, h_sample, updates = rbm.get_samples(XX,step=K)
    gen_samples = theano.function([XX, K], v_samples, updates=updates)
    sample_connect = np.around(np.random.binomial(1,1-0.8, 100*D).reshape(100,D).astype('float32'))

    start_mpf = timeit.default_timer()
    for epoch in xrange(num_epoches+1):
        tot_cost = [] 
        thrd_epoch = get_thrd(epoch, num_epoches)

        for ith_batch in xrange(num_batches):
            init_sample_connect = train_data[ith_batch*batch_sz:(ith_batch+1)*batch_sz]

            #Descent over the trajectory 
            for kkk in xrange(20):
                ith_batch_cost = train_update(ith_batch, sample_connect)
            new_sample_connect = gen_samples(init_sample_connect,steps)

            tot_cost.append(ith_batch_cost)
            sample_connect = new_sample_connect


        if epoch % 10 == 0:
            valid_cost = []
            for j in xrange(Nv / 1000):
                valid_cost_j = get_valid_cost(j, sample_connect)
                valid_cost.append(valid_cost_j)

            print 'Epoch %d, Train Cost %g, Valid Cost %g'\
                % (epoch, np.mean(np.asarray(tot_cost)), np.mean(np.asarray(valid_cost)))
       
    stop_mpf = timeit.default_timer() 
    print '...Time it took to train rbm %f' % (stop_mpf-start_mpf)

    print 'Batch size %d, lr %g, lam %g, num_hid %d, num_dim %d' % \
                    (batch_sz, epsilon, lam, num_hid, D)

    return rbm


#Hyper-parameters
steps=15
rbm_type='RBM'
num_hid = 200
epsilon = 0.0001
batch_sz = 25
num_epoches = 10
lam = 0.0001

if __name__ == '__main__':

    data_path = '/mnt/data/datasets/mnist_binary.pkl'
    print 'opening data'
    f = open(data_path)
    train_set, valid_set, test_set = pickle.load(f)
    f.close()

    N, D = train_set[0].shape
    Nv = valid_set[0].shape[0]

    hyper_params = [batch_sz, epsilon, lam, num_hid, N, Nv, D, num_epoches]
    
    start_mpf = timeit.default_timer()
    rbm = train_rbm(train_set[0], valid_set[0], hyper_params, mpf_type='factored_mpf', steps=steps)
    stop_mpf = timeit.default_timer() 


    X = train_set[0][0:16,:]
    display_dataset(X, (28,28), (4,4), i=1)

    XX = T.matrix('X'); K=T.iscalar('s')
    v_samples, v_means, h_sample, updates = rbm.get_samples(XX,step=K)
    gen_samples = theano.function([XX, K], v_samples, updates=updates)

    samples = gen_samples(X,1)
    display_dataset(samples, (28,28), (4,4), i=2)

    samples = gen_samples(X,10)
    display_dataset(samples, (28,28), (4,4), i=3)

    samples = gen_samples(X,30)
    display_dataset(samples, (28,28), (4,4), i=4)

    samples = gen_samples(X,100)
    display_dataset(samples, (28,28), (4,4), i=4)

    plt.show()


