import re
import json
import pandas as pd
import pickle
import seaborn as sns
import glob as glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import csv

sns.set(style="ticks")
sns.set_context("paper")
mpl.rcParams['pdf.fonttype'] = 42
params = {'legend.fontsize': 8,
          'legend.handlelength': 2,
          'axes.linewidth' : 0.25,
          'xtick.minor.width'    : 0.5,    ## major tick width in points
          'xtick.major.width'    : 0.5,
          'ytick.major.width'    : 0.5,
          'axes.labelsize'       : 6,
          'xtick.labelsize'      : 6,
          'ytick.labelsize'      : 6,
          'axes.titlesize'       : 8,
          'ytick.minor.width'    : 0.5}    ## minor tick width in points
plt.rcParams.update(params)
plt.close(fig=None)

def makedict():
    files = glob.glob("*.txt")
    keys = ['198','192','184','178','170','156','142','205','259','253','231','218','217','191','177','219','206']
    keys = ['m/z ' + s for s in keys]
    t = np.linspace(9, 125, 4875)
    
    d = {}
    for f in files:
        d_sub = {key: [] for key in keys}
        d_sub['Retention time (min)'] = t
        with open(f, "rt") as myfile: # open GCMS_sample.txt for reading text
            for line in myfile:
                if "Packet # 0" in line: # read the entire file to string
                    ls = re.findall("\d+\.\d+", line)
                    val = float(ls[0])             
                    key = float(ls[1])
                    key = round(key)
                    key = 'm/z ' + str(key)
                    d_sub[key].append(val)
                                       
            f = f.rsplit('.', 1)[0] # remove file ending from string                
            d[f] = d_sub # add sample to master dictionary
            makecsv(d_sub, f)
            
    return d

def makepkl(d):
    pklfile = open("data.pkl", "wb")
    pickle.dump(d, pklfile)
    pklfile.close()

def getpkl():
    pickle_in = open("data.pkl","rb")
    example_dict = pickle.load(pickle_in)
    return example_dict

def makecsv(d, f):
    df = pd.DataFrame().from_dict(d, orient = 'index')
    df = df.transpose()
    df.dropna().to_csv(f + '.csv', index=False, sep = '\t')

def plotdata_mz191():
    xmin, xmax = 45, 120
    chromatograms_test = ['NSO-1_190320000325.csv','NSO-1_190321033404.csv']
    titles = chromatograms_test
    
    # Skrukkefjellet
    #chromatograms = ['SKØ2-18-16.csv',
    #                 'SKØ2-18-10.csv',
    #                 'SKØ2-18-05.csv',
    #                 'SKR1-18-22.csv',
    #                 'SKR1-18-05.csv',
    #                 'NSO-1_190323103825.csv']
    
    # Blanknuten
    #chromatograms = ['BLA2-18-16.csv',
    #                 'BLA2-18-25.csv',
    #                 'BLA2-18-39.csv',
    #                 'BLA2-18-44.csv',
    #                 'BLA2-18-55.csv',
    #                 'BLA2-18-64.csv',
    #                 'BLA2-18-70.csv'][::-1]
    
    # Stratigraphic units    
    #titles = ['Tschermakfjellet Fm.'
    #'upper Blanknuten Mb.',
    #'middle Blanknuten Mb.',
    #'lower Blanknuten Mb.',
    #'upper Muen Mb.',
    #'lower-middle Muen Mb.',
    #'Vendomdalen Mb.']

    fig, ax = plt.subplots(len(chromatograms_test), sharex = True, figsize=(6, 4), constrained_layout=True)
    
    j = 0
    for x, y in zip(chromatograms_test, titles):
        xmin, xmax = 45, 120
        data = pd.read_csv(x, sep = '\t')
        data = data.iloc[1412:]
        sns.lineplot(data = data, y = 'm/z 191', x = 'Retention time (min)', ax = ax[j], linewidth = 0.5)
        ax[j].set_title(y)
        ax[j].set_xlim(xmin,xmax)
        ax[j].set_ylim(0, data['m/z 191'].max()*1.05)
        #plt.autoscale(enable=True, axis='y', tight=True)
        j = j + 1

def plotdata_mz177():
    xmin, xmax = 45, 120
    # selecting chromatograms to plot
    chromatograms = ['SKØ2-18-16.csv',
                     'SKØ2-18-10.csv',
                     'SKØ2-18-05.csv',
                     'SKR1-18-22.csv',
                     'SKR1-18-05.csv',
                     'NSO-1_190323103825.csv']
    
    titles = ['Tschermakfjellet Fm.',
    'upper Blanknuten Mb.',
    'middle Blanknuten Mb.',
    'lower Blanknuten Mb.',
    'upper Muen Mb.',
    'lower-middle Muen Mb.',
    'Vendomdalen Mb.']

    fig, ax = plt.subplots(len(chromatograms), sharex = True, figsize=(6, 4), constrained_layout=True)
    
    j = 0
    for x, y in zip(chromatograms, titles):
        data = pd.read_csv(x, sep = '\t')
        sns.lineplot(data = data.iloc[1412:], y = 'm/z 177', x = 'Retention time (min)', ax = ax[j], linewidth = 0.5)
        ax[j].set_title(y)
        ax[j].set_xlim(xmin,xmax*1.05)
        ax[j].set_ylim(0,None)
        plt.autoscale(enable=True, axis='y', tight=True)
        j = j + 1

makedict()
plotdata_mz191()