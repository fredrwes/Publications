import re
import pandas as pd
import seaborn as sns
import glob as glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Plotting aesthethics
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
        with open(f, "rt") as myfile: # Open .txt file
            for line in myfile:
                if "Packet # 0" in line: # Read the entire file to string
                    ls = re.findall("\d+\.\d+", line) # Find decimal digits in line
                    val = float(ls[0]) # ... the value
                    key = float(ls[1]) # ... the m/z ratio
                    key = round(key) # Round m/z ratio to integer
                    key = 'm/z ' + str(key)
                    d_sub[key].append(val) # Add to dictionary
                                       
            f = f.rsplit('.', 1)[0] # Remove file ending from string                
            makecsv(d_sub, f) # Make .csv file for each sample
            d[f] = d_sub # Add sample to master dictionary (sample set)
                        
    return d #Return sample set

def makecsv(d, f):
    df = pd.DataFrame().from_dict(d, orient = 'index')
    df = df.transpose()
    df.dropna().to_csv(f + '.csv', index=False, sep = '\t')

def plotdata_mz191():
    # Setting retention time window
    xmin, xmax = 45, 120
    # Which chromatograms to plot
    chromatograms = ['NSO-1_190320000325.csv','NSO-1_190321033404.csv']
       
    # Plot settings
    fig, ax = plt.subplots(len(chromatograms), sharex = True, figsize=(6, 6), constrained_layout=True)
    
    # Plotting
    j = 0
    for c in chromatograms:
        xmin, xmax = 45, 120
        data = pd.read_csv(c, sep = '\t')
        data = data.iloc[1412:]
        sns.lineplot(data = data, y = 'm/z 191', x = 'Retention time (min)', ax = ax[j], linewidth = 0.5)
        ax[j].set_title(c)
        ax[j].set_xlim(xmin,xmax)
        ax[j].set_ylim(0, data['m/z 191'].max()*1.05)
        j = j + 1
    
    # Saving plot
    saveloc = 'NSO_1_chromatograms.pdf'
    plt.savefig(saveloc, bbox_inches='tight')

makedict()
plotdata_mz191()

# Chromatograms to plot for paper III:

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
