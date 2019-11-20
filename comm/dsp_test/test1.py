# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 20:46:00 2019

@author: sliu3
"""

import numpy as np
import matplotlib.pyplot as plt

def get_filter(name, T, rolloff=None):
    def rc(t, beta):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return np.sinc(t)*np.cos(np.pi*beta*t)/(1-(2*beta*t)**2)
    def rrc(t, beta):
        return (np.sin(np.pi*t*(1-beta))+4*beta*t*np.cos(np.pi*t*(1+beta)))/(np.pi*t*(1-(4*beta*t)**2))
        
    # rolloff is ignored for triang and rect
    if name == 'rect':
        return lambda t: (abs(t/T)<0.5).astype(int)    
    if name == 'triang': 
        return lambda t: (1-abs(t/T)) * (abs(t/T)<1).astype(float)
    elif name == 'rc':
        return lambda t: rc(t/T, rolloff)
    elif name == 'rrc':
        return lambda t: rrc(t/T, rolloff)

 
    
#
T = 1
Fs = 32
t = np.arange(-3*T,3*T,1/Fs)
g = get_filter('rc', T, rolloff=0.9)
plt.figure(figsize=(8,3))
plt.plot(t, get_filter('rc', T, rolloff=0.5)(t), label=r'Raised cosine $\alpha=0.5$')
plt.plot(t, get_filter('rrc', T, rolloff=0.5)(t), label=r'Root raised cosine $\alpha=0.5$')
plt.plot(t, get_filter('rect', T)(t), label=r'Rectangular')
plt.plot(t, get_filter('triang', T)(t), label=r'Triangular', lw=2)

b = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
#d = 2*b-1

d = b



def get_signal(g, d):
    """Generate the transmit signal as sum(d[k]*g(t-kT))"""
    t = np.arange(-2*T, (len(d)+2)*T, 1/Fs)
    g0 = g(np.array([1e-8]))
    xt = sum(d[k]*g(t-k*T) for k in range(len(d)))
    return t, xt/g0   


fig = plt.figure(figsize=(8,3))
t, xt = get_signal(g, d)
plt.plot(t,xt, 'k-', label='$x(t)$')
plt.stem(T*np.arange(len(d)), d, use_line_collection=True)
#for k in range(len(d)):
#        plt.plot(t, d[k]*g(t-k*T), 'b--', label='$d[k]g(t-kT)$')



tt = np.arange(-2*T, (len(d)+2)*T, 1/Fs)
g00 = g(tt)


xxt = np.convolve(d,g00)
xxxt = sum(d[k]*g(t-k*T) for k in range(len(d)))
xxxxt = [d[k]*g(t-k*T) for k in range(len(d))]

'''
plt.plot(xt)
plt.plot(xxt)
plt.plot(xxxt)


for i in xxxxt:
    plt.plot(i)



'''


