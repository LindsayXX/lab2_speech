import numpy as np
import matplotlib.pyplot as plt
from prondict import prondict
from lab2_tools import *
from lab2_proto import *

def main():
    data = np.load('lab2_data.npz')['data']
    phoneHMMs = np.load('lab2_models_onespkr.npz')['phoneHMMs'].item()
    phoneHMMs_all = np.load('lab2_models_all.npz')['phoneHMMs'].item()
    """4"""
    '''
    hmm1 = phoneHMMs['ah']
    hmm2 = phoneHMMs['ao']
    twohmm= concatTwoHMMs(hmm1, hmm2)
    '''
    """5 HMM Likelihood and Recognition"""
    """
    5.1
    """
    example = np.load('lab2_example.npz')['example'].item()
    isolated = {}
    for digit in prondict.keys():
        isolated[digit] = ['sil'] + prondict[digit] + ['sil']
    wordHMMs = {}
    wordHMMs_all = {}
    # example
    for digit in prondict.keys():
        wordHMMs[digit] = concatHMMs(phoneHMMs, isolated[digit])
    lpr = log_multivariate_normal_density_diag(example['lmfcc'], wordHMMs['o']['means'], wordHMMs['o']['covars'])
    diff = example['obsloglik'] - lpr  # 0
    # for 11 digits
    for digit in prondict.keys():
        wordHMMs_all[digit] = concatHMMs(phoneHMMs_all, isolated[digit])
    # same digit 'o'
    lpr_o = log_multivariate_normal_density_diag(data[22]['lmfcc'], wordHMMs_all['o']['means'],
                                                 wordHMMs_all['o']['covars'])
    '''
    plt.figure()
    plt.subplot(2,1,1)
    plt.pcolormesh(lpr.T)
    plt.title('example "o" ')
    plt.colorbar()
    plt.subplot(2, 1, 2)
    plt.pcolormesh(lpr_o.T)
    plt.title('test "o" from data22')
    plt.colorbar()
    plt.show()
    '''
    """
    5.2
    """
    lalpha = forward(lpr, np.log(wordHMMs['o']['startprob']), np.log(wordHMMs['o']['transmat']))
    diff1 = example['logalpha'] - lalpha  # 0
    # log-likelihood
    loglike = logsumexp(lalpha[-1])
    diff0 = example['loglik'] - loglike  # 0

    # score all the 44 utterances in the data array with each of the 11 HMM
    # models in wordHMMs.
    scores_1 = np.zeros((44, 11))
    scores_2 = np.zeros((44, 11))
    labels_ori = []
    labels_pre = []
    labels_pre2 = []
    keys = list(prondict.keys())
    acc_1 = 0
    acc_2 = 0
    '''
    for i in range(44):
        for j, key in enumerate(keys):
            lpr = log_multivariate_normal_density_diag(data[i]['lmfcc'], wordHMMs_all[key]['means'],
                                                         wordHMMs_all[key]['covars'])
            alpha = forward(lpr, np.log(wordHMMs_all[key]['startprob']), np.log(wordHMMs_all[key]['transmat']))
            scores_2[i, j] = logsumexp(alpha[-1])
            lpr_1 = log_multivariate_normal_density_diag(data[i]['lmfcc'], wordHMMs[key]['means'],
                                                       wordHMMs[key]['covars'])
            alpha_1 = forward(lpr_1, np.log(wordHMMs[key]['startprob']), np.log(wordHMMs[key]['transmat']))
            scores_1[i, j] = logsumexp(alpha_1[-1])
        ori = data[i]['digit']
        pre_1 = keys[int(np.argmax(scores_1[i, :]))]
        pre_2 = keys[int(np.argmax(scores_2[i, :]))]
        #labels_ori.append(ori)
        labels_pre.append(pre_1)
        labels_pre2.append(pre_2)
        if ori == pre_1:
            acc_1 += 1
        if ori == pre_2:
            acc_2 += 1
    print("Accuracy(trained on all speakers): {0}; Accuracy(trained on one speaker):{1} ".format(acc_2, acc_1))
    print(labels_pre, labels_pre2)
    '''

    """
    5.3 Viterbi
    """
    viterbi_loglik, viterbi_path = viterbi(lpr, np.log(wordHMMs['o']['startprob']), np.log(wordHMMs['o']['transmat']))
    # plt.pcolormesh(lalpha.T)
    # plt.plot(viterbi_path,'r')
    # plt.show()
    diff3 = example['vloglik'] - viterbi_loglik.T  # 0

    # Score all 44 utterances in the data with each of the 11 HMM models in wordHMMs
    '''
    for i in range(44):
        for j, key in enumerate(keys):
            lpr = log_multivariate_normal_density_diag(data[i]['lmfcc'], wordHMMs_all[key]['means'],
                                                       wordHMMs_all[key]['covars'])
            viterbi_2, viterbi_path_2 = viterbi(lpr, np.log(wordHMMs_all[key]['startprob']), np.log(wordHMMs_all[key]['transmat']))
            scores_2[i, j] = viterbi_2
            lpr_1 = log_multivariate_normal_density_diag(data[i]['lmfcc'], wordHMMs[key]['means'],
                                                         wordHMMs[key]['covars'])
            viterbi_1, viterbi_path_1 = viterbi(lpr_1, np.log(wordHMMs[key]['startprob']), np.log(wordHMMs[key]['transmat']))
            scores_1[i, j] = viterbi_1
        ori = data[i]['digit']
        pre_1 = keys[int(np.argmax(scores_1[i, :]))]
        pre_2 = keys[int(np.argmax(scores_2[i, :]))]
        #labels_ori.append(ori)
        labels_pre.append(pre_1)
        labels_pre2.append(pre_2)
        if ori == pre_1:
            acc_1 += 1
        if ori == pre_2:
            acc_2 += 1
    print("Accuracy(trained on all speakers): {0}; Accuracy(trained on one speaker):{1} ".format(acc_2, acc_1))
    print(labels_pre, labels_pre2)
    '''

    """
    5.4
    """
    lbeta = backward(lpr, np.log(wordHMMs['o']['startprob']), np.log(wordHMMs['o']['transmat']))
    diff2 = example['logbeta'] - lbeta
    # log-likelihood
    loglike = logsumexp(lbeta[0])
    diff4 = example['loglik'] - loglike  # 0

    """6 HMM Retraining(emission probability distributions)"""
    """6.1"""
    lgamma = statePosteriors(lalpha, lbeta)
    # print(np.sum(np.exp(lgamma), axis=1)) #=1
    N = lgamma.shape[0]
    K = 9
    lgamma_gmm = np.zeros((N, K))
    total = log_multivariate_normal_density_diag(example['lmfcc'], wordHMMs['o']['means'],
                                                 wordHMMs['o']['covars'])
    for k in range(K):
        lgamma_gmm[:, k] = 1 / K * total[:, k] / np.sum(total[:, k])
    plt.subplot(2, 1, 1)
    plt.pcolormesh(lgamma_gmm.T)
    plt.colorbar()
    plt.subplot(2, 1, 2)
    plt.pcolormesh(lgamma.T)
    plt.colorbar()
    plt.show()
    #print(np.sum(np.exp(lgamma), axis=0))
    #print(np.sum(np.sum(np.exp(lgamma))))  # =length of obs sequence/time steps

    """6.2"""
    # wordHMMs['4'] =
    # initialization
    log_pi = np.log(wordHMMs_all['4']['startprob'])
    log_tr = np.log(wordHMMs_all['4']['transmat'])
    means = wordHMMs_all['4']['means']
    covars = wordHMMs_all['4']['covars']
    # repitation:
    for i in range(20):
        lpr = log_multivariate_normal_density_diag(data[10]['lmfcc'],
                                                   means, covars)
        # Expectation
        lalpha = forward(lpr,log_pi,log_tr)
        lbeta = backward(lpr,log_pi,log_tr)
        log_gamma = statePosteriors(lalpha,lbeta)
        # Maximization
        means, covars = updateMeanAndVar(data[10]['lmfcc'], log_gamma)
        # Estimate likelihood
        log_like = logsumexp(lalpha[-1])
        #print(covars)
        print(log_like)
    #rint('means', means)
    #print('covars', covars)
    #lpr_new = log_multivariate_normal_density_diag(example['lmfcc'], means,
    #                                          covars)
    #lalpha = forward(lpr_new, np.log(wordHMMs['o']['startprob']), np.log(wordHMMs['o']['transmat']))
    #loglike_new = logsumexp(lalpha[-1])
    #print(loglike_new-loglike)
    #print(wordHMMs['o']['covars'])
    #print(covars)
if __name__ == "__main__":
    main()