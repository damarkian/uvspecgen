import sys
import re
import numpy as np
import matplotlib.pyplot as plt

def get_peaks(f_poles, f_osc):
    poles, osc = [], []
    fpolepos = open(f_poles, "r")
    for line in fpolepos:
        poles.append(float(line))
    foscpos = open(f_osc, "r")
    for line in foscpos:
        osc.append(float(line))
    return poles, osc

def broaden_spectrum(osc,poles,b_type,sigma,npoints):
    ''' Broaden poles to have a particular line shape '''

    npnts = npoints

    # define the range of frequencies
#    pole_min, pole_max = min(poles)-2, max(poles)+4
    pole_min, pole_max = 0.01, max(poles)+4
    freq_step = (pole_max - pole_min) / npnts
    freq = [pole_min + i*freq_step for i in range(npnts)]

    # Build absorption spectrum by brodening each pole
    absorbance = np.zeros([npnts])
    for i in range(len(osc)):
#       print 'Energy = %.4f, Osc = %.4f' % (poles[i], osc[i])
        for j in range(npnts):
            if b_type == 'lorentz':
                x       = (poles[i] - freq[j]) / (sigma/2)
                absorbance[j] += osc[i] / (1 + x**2)
            else:
                print ('Broadening Scheme %s NYI' % b_type)
                sys.exit()
            
    return absorbance, freq

def plot_ev_spectrum(Abs,freq,osc,poles,title):

    fig = plt.figure(figsize=(14,10))
    ax  = fig.gca()
    ax.plot(freq,Abs)
    ax.vlines(poles,[0],osc)
    plt.title(title)
    plt.xlabel('Wavelength (eV)')
    plt.ylabel('Absorbance (arbitrary units)')

def plot_nm_spectrum(absorbance, wavelength, osc, poles, title):
    
    fig = plt.figure(figsize=(14,10))
    ax = fig.gca()
    ax.plot(wavelength, absorbance)
    ax.vlines(poles,[0],osc)
    ax.invert_xaxis()
    plt.xlim(100,900)
    plt.title(title)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Absorbance (arbitrary units)')
    


#
#
# PARAMETERS
#
broadening = 'lorentz'
sigma = 0.2
npoints = 3000
title = "SAMPLE"
peaks_file = "SAMPLE-excitations.txt"
osc_file = "SAMPLE-osc.txt"
hc = 1239.841984


poles, osc = get_peaks(peaks_file, osc_file)
absorbance, freq = broaden_spectrum(osc, poles, broadening, sigma, npoints)
wavelength = [hc / x for x in freq]
lambda_poles = [hc / x for x in poles]
maxabs = max(absorbance)
maxevpol = max(poles)
maxnmpol = max(lambda_poles)
maxosc = max(osc)
norm_absorbance = [x / maxabs for x in absorbance]
norm_osc = [x / maxosc for x in osc]


plot_ev_spectrum(absorbance, freq, osc, poles, title)
plt.show()
plot_nm_spectrum(absorbance, wavelength, osc, lambda_poles, title)
plt.show()

plot_ev_spectrum(norm_absorbance, freq, norm_osc, poles, title)
plt.show()
plot_nm_spectrum(norm_absorbance, wavelength, norm_osc, lambda_poles, title)
plt.show()


