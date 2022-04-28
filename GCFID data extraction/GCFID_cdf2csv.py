import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib as mpl
import numpy as np
import netCDF4 as nc
import glob as glob

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
plt.close('all')

def makecsv():
    files = glob.glob("*.cdf")
    for f in files:
        df = pd.DataFrame()
        ds = nc.Dataset(f)
        y = ds['ordinate_values'][:]
        f = (f.rsplit('.', 1)[0]).upper()
        df['Response (V)'] = y
        ds.close()
        df['Retention time (min)'] = np.linspace(0, 90, 53543)
        df.to_csv(f + '.csv', index=False, sep = '\t')

def plotdata():
    
    # Which chromatograms to plot
    chromatograms = glob.glob("*.csv")
       
    # Plot settings
    fig, ax = plt.subplots(len(chromatograms), sharex = True, figsize=(6, 6), constrained_layout=True)
    
    # Plotting
    j = 0
    for c in chromatograms:
        xmin, xmax = 0, 90
        data = pd.read_csv(c, sep = '\t')
        sns.lineplot(data = data, y = 'Response (V)', x = 'Retention time (min)', ax = ax[j], linewidth = 0.5)
        ax[j].set_title(c)
        ax[j].set_xlim(xmin,xmax)
        j = j + 1
    
    ax[0].set_ylim(0, 0.5)
    ax[1].set_ylim(0, 0.3)
    
    # Saving plot
    saveloc = 'NSO_1_chromatograms.pdf'
    plt.savefig(saveloc, bbox_inches='tight')

makecsv()
plotdata()