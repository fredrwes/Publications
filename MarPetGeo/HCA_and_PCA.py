
# Importing required libraries and data
###############################################################################

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from dataimport import Wesenlund_et_al_MPG_data, mplplotparams

# Importing data
(wong_botneheia,
 stratlimits_blanknuten,
 stratlimits_skrukkefjellet,
 df_MPG,
 df_MPG_Blanknuten,
 df_MPG_Skrukkefjellet) = Wesenlund_et_al_MPG_data()

# Setting plot aesthethics
mplplotparams()
sns.set_palette(wong_botneheia)

###############################################################################
# HCA analysis
###############################################################################

# Splitting and sorting relevant variables from dataframes
df_MPG_split = df_MPG.loc[:,'Sample ID':'SAT/ARO']
(df_p, df_h, df_f, df_s) = (df_MPG_split['Sample ID'],
                            df_MPG_split['Height (m)'],
                            df_MPG_split['Facies'],
                            df_MPG_split['Stratigraphic unit'])

df_numdata = df_MPG_split.loc[:, 'TOC (wt. %)':'SAT/ARO'] # Extracting XRF data
df_beforeHCA = pd.concat([df_s, df_h, df_p, df_f, df_numdata], axis = 1).dropna()
stratunits = df_beforeHCA.pop("Stratigraphic unit")

# Formatting ticklabels for y axis to show locality, Facies and log height
yticklabels = (df_beforeHCA['Sample ID'].astype(str).str[0] + ', ' +
               df_beforeHCA['Facies'] + ', ' + 
               df_beforeHCA['Height (m)'].round(2).astype(str) + ' m')

# Creating numerical matrix for HCA analysis
df_beforeHCA = df_beforeHCA.drop(['Sample ID',
                                  'Facies',
                                  'Height (m)',
                                  'TC (wt. %)'], axis = 1)

# Assigning colordata for plotting leftmost column as stratigraphic unit
colordict = dict(zip(stratunits.unique(), wong_botneheia))
row_colors = stratunits.map(colordict)

# Plotting HCA heatmap and dendrogram
cg = sns.clustermap(df_beforeHCA,
               method='average',
               metric='euclidean',
               standard_scale=1,
               row_colors=row_colors,
               cmap = 'rocket',
               yticklabels=yticklabels,
               col_cluster=False,
               )

# Plot settings
plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=45, horizontalalignment='right')
plt.savefig('HCA_RAW.pdf')

###############################################################################

# The PCA analysis code is based on Serafeim Loukas's original post (CC BY-SA 4.0)
# on StackExchange (https://stackoverflow.com/a/50845697/5025009). S. Loukas's
# code was modified to fit the aim of this scientific contribution.
# The code below is licensed under CC BY-SA 4.0.
# Link to licence: https://creativecommons.org/licenses/by-sa/4.0/

###############################################################################

# splitting and sorting relevant variables from dataframes
df_MPG_cat = df_MPG[['Stratigraphic unit','Locality','Facies']]
df_MPG_num = df_MPG.loc[:,'TOC (wt. %)':'SAT/ARO']
df_MPG_beforePCA = pd.concat([df_MPG_cat,df_MPG_num], axis = 1).dropna()
hue = df_MPG_beforePCA['Stratigraphic unit']
style = df_MPG_beforePCA['Facies']
size = df_MPG_beforePCA['Locality']
markers = ['o','D','s','P']
df_beforePCA_data = df_MPG_beforePCA.loc[:,'TOC (wt. %)':'SAT/ARO']
df_beforePCA_data = df_beforePCA_data.drop('TC (wt. %)', axis = 1)

labels = list(df_beforePCA_data.columns)

# Scaling data
df_beforePCA_data_scaled = MinMaxScaler().fit_transform(df_beforePCA_data)

# Assigning PCA function
pca = PCA()

# Performing PCA
df_afterPCA = pca.fit_transform(df_beforePCA_data_scaled)

# Defining PCA plot function. The function is modified based on 
def PCAplot(pcax, pcay, score, coeff):
    pcax = pcax - 1
    pcay = pcay - 1
    xs = score[:,pcax]
    ys = score[:,pcay]
    n = coeff.shape[0]
    scalex = 1.0/(xs.max() - xs.min())
    scaley = 1.0/(ys.max() - ys.min())
    fig, ax = plt.subplots(1, 1, figsize=(6, 4), constrained_layout=True)
    sns.scatterplot(x = xs * scalex,
                    y = ys * scaley,
                    hue = hue,
                    style = style,
                    size = size,
                    sizes= (50, 20),
                    legend = 'brief',
                    markers = markers,
                    palette = wong_botneheia,
                    edgecolor='k',
                    alpha=0.9,
                    linewidth=0.5,
                    )
    
    # Create biplot arrows and labels for arrows
    for i in range(n):
        plt.arrow(0, 0, coeff[i,pcax], coeff[i,pcay], color = 'r', alpha = 0.5)
        plt.text(coeff[i,pcax], coeff[i,pcay], labels[i], color = 'k', ha = 'center', va = 'center', fontsize = 8)
    
    # Plot Explained variance for the plotted PCs
    plt.xlabel("PC" + str(pcax+1) + " (" + str(round(pca.explained_variance_ratio_[pcax] * 100, 1)) + " % of variance)")
    plt.ylabel("PC" + str(pcay+1) + " (" + str(round(pca.explained_variance_ratio_[pcay] * 100, 1)) + " % of variance)")

PCAplot(1, 2, df_afterPCA[:, 0:2], np.transpose(pca.components_[0:3, :]))
plt.savefig('PCA_RAW.pdf')