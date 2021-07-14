import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib as mpl
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from matplotlib.ticker import AutoMinorLocator
plt.close('all')

sns.set_context("paper")
sns.set_style('ticks')
mpl.rcParams['pdf.fonttype'] = 42
params = {'legend.fontsize': 6,
      'legend.handlelength': 2,
      'axes.linewidth' : 0.5,
      'xtick.minor.width'    : 0.5,    ## major tick width in points
      'xtick.major.width'    : 0.5,
      'ytick.major.width'    : 0.5,
      'axes.labelsize'       : 8,
      'xtick.labelsize'      : 6,
      'ytick.labelsize'      : 6,
      'ytick.minor.width'    : 0.5}    ## minor tick width in points
plt.rcParams.update(params)

palette = ['#4A412A', '#F0E442', '#E69F00', '#56B4E9', '#009E73', '#0072B2', '#CC79A7', '#D55E00']
df = pd.read_excel('Appendix_C.xlsx', skipfooter=1)
df = df.set_index("Sample ID")
df_no_outliers = df.drop(['BLA2-18-49','BLA2-18-65','SKØ2-18-11'])
df_no_outliers.reset_index(inplace=True)

X1 = df_no_outliers[['Sample ID',
         'Composite height (m)',
         'Stratigraphic unit',
         'Facies',
         'Locality',
         'TOC (wt. %)',
         'TIC (wt. %)',
         'TS (wt. %)']]

X2 = df_no_outliers.loc[:,'Si (%)-EF':'U (PPM)-EF']
X3 = df_no_outliers['DOPT']
X4 = df_no_outliers.loc[:,'Si (%)':'U (PPM)']
X_EF = pd.concat([X1,X2,X3], axis = 1) # concatenating labels, LECO and XRF data
X_wt = pd.concat([X1,X4,X3], axis = 1) # concatenating labels, LECO and XRF data

def Fig_5():
    X_EF_corr = X_EF.drop(['Sample ID',
                           'Facies',
                           'Composite height (m)',
                           'Locality',
                           'Al (%)-EF'], axis = 1)
    corr = X_EF_corr.corr()
    corr = corr * 100
    corr = corr.round(0)
    mask = np.zeros(corr.shape, dtype=bool)
    mask[np.triu_indices(len(mask))] = True
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr,
                mask=mask,
                cmap="vlag",
                annot=True,
                linewidths=.5,
                vmin = -100,
                vmax = 100,
                center = 0.0,
                annot_kws={"size": 6})
    plt.savefig('Fig_5_PCC_EFs_RAW.pdf')
    
    X_wt_corr = X_wt.drop(['Sample ID',
                            'Facies',
                            'Composite height (m)',
                            'Locality',
                            'Al2O3 (%)',
                            'Fe2O3 (%) M',
                            'Fe2O3 (%)',
                            'Fe (%) M',
                            'CaO (%)',
                            'MgO (%)',
                            'Na2O (%)',
                            'K2O (%)',
                            'S (%)',
                            'SO3 (%)',
                            'P2O5 (%)',
                            'SeO2 (PPM)',
                            'Se (PPM)',
                            'TiO2 (%)',
                            'MnO (%)'], axis = 1)
    corr = X_wt_corr.corr()
    corr = corr * 100
    corr = corr.round(0)
    mask = np.zeros(corr.shape, dtype=bool)
    mask[np.triu_indices(len(mask))] = True
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr,
                mask=mask,
                cmap="vlag",
                annot=True,
                linewidths=.5,
                vmin = -100,
                vmax = 100,
                center = 0.0,
                annot_kws={"size": 6})
    plt.savefig('Fig_5_PCC_wt_RAW.pdf')

def Fig_6():
    stratunits = X_EF["Stratigraphic unit"]
    lut = dict(zip(stratunits.unique(), palette))
    row_colors = stratunits.map(lut)
    yticklabels = (X_EF['Sample ID'].astype(str).str[0] + ', ' +
               X_EF['Facies'] + ', ' + 
               X_EF['Composite height (m)'].round(1).astype(str) + ' m')

    X = X_EF.drop(['Sample ID','Facies','Stratigraphic unit','Composite height (m)','Locality','Al (%)-EF'], axis = 1)

    sns.clustermap(X,
               method='average',
               metric='euclidean',
               standard_scale=1,
               row_colors=row_colors,
               cmap = 'mako',
               yticklabels=yticklabels,
               #robust = True,
               )

    plt.savefig('Fig_6_HCA_RAW.pdf')

def Figs_7_and_8():
    X_EF.sort_values(by=['Composite height (m)'], inplace=True)
    hue = X_EF['Stratigraphic unit']
    style = X_EF['Facies']
    size = X_EF['Locality']
    markers = ['^','o','D','s','P','p']
    X_EF_unscaled = X_EF.loc[:,'TOC (wt. %)':'DOPT'].drop('Al (%)-EF', axis = 1)
    labels = list(X_EF_unscaled.columns) # labels for PCA plot

    X_EF_scaled = MinMaxScaler().fit_transform(X_EF_unscaled)
    pca = PCA()
    X_EF_scores = pca.fit_transform(X_EF_scaled)

    def myplot(pcax, pcay, score, coeff):
        pcax = pcax - 1
        pcay = pcay - 1
        xs = score[:,pcax]
        ys = score[:,pcay]
        n = coeff.shape[0]
        
        scalex = 1.0/(xs.max() - xs.min())
        scaley = 1.0/(ys.max() - ys.min())
        fig, ax = plt.subplots(1, 1, figsize=(6, 4))
        sns.scatterplot(x = xs * scalex,
                        #x = xs,
                        y = ys * scaley,
                        #y = ys,
                        hue = hue,
                        style = style,
                        size = size,
                        sizes= (50, 20),
                        legend = 'brief',
                        #legend = False,
                        markers = markers,
                        palette = palette,
                        edgecolor='k',
                        alpha=0.9,
                        linewidth=0.5,
                        )
        
        for i in range(n): # Create biplot arrows and labels for arrows
            plt.arrow(0, 0, coeff[i,pcax], coeff[i,pcay], color = 'r', alpha = 0.5)
            plt.text(coeff[i,pcax], coeff[i,pcay], labels[i][:2], color = 'k', ha = 'center', va = 'center', fontsize = 6)
        
        plt.axvline(0, linewidth=0.5, color =  'k')
        plt.axhline(0, linewidth=0.5, color =  'k') 
        plt.xlabel("PC" + str(pcax+1) + " (" + str(round(pca.explained_variance_ratio_[pcax] * 100, 2)) + " % of variance)")
        plt.ylabel("PC" + str(pcay+1) + " (" + str(round(pca.explained_variance_ratio_[pcay] * 100, 2)) + " % of variance)")
    
    myplot(1, 2, X_EF_scores[:, 0:2], np.transpose(pca.components_[0:2, :])) # Call the function. Use only the 2 PCs.
    plt.savefig('Fig_7_PCA_biplot_RAW.pdf')
    
    pcs = [0,1,2]
    plt.subplots_adjust(wspace=0.1, hspace=0)
    y = X_EF['Composite height (m)']
    vikboundary = 41.2
    stratlimits_Botneheia = [35, # lower to middle - upper Muen Mb height (m)
                             42.4, # upper Muen Mb - lower Blanknuten Mb height (m)
                             51.9, # lower - middle Blanknuten Mb height (m)
                             66.45, # middle - upper Blanknuten mb height (m)
                             75.4] # upper Blanknuten mb - Tschermakfjellet Fm height (m)
    stratlimits_Sassen = np.array([0] + stratlimits_Botneheia) + vikboundary

    f, ax = plt.subplots(2,
                    len(pcs),
                    squeeze=True,
                    figsize=(6, 8)                   
                    )

    for i in pcs:
        ax[0,i].hlines(range(0,35), 0, np.transpose(*pca.components_[i:i+1, :]), color='tab:grey', linewidth = 1)
        ax[0,i].axvline(0, color = 'k', linewidth = 0.5, ls = '--')
        ax[0,i].plot(np.transpose(*pca.components_[i:i+1, :]), range(0,35), marker = 'o', markersize = 2, linestyle = '', c = 'red')  # Stem ends
        ax[0,i].set_yticks(range(0,35,1))
        ax[0,i].set_yticklabels(X_EF_unscaled.columns.values)   
        ax[0,i].xaxis.set_minor_locator(AutoMinorLocator())
        ax[0,i].grid(color='k', linestyle='-', axis = 'x', which = 'both', linewidth=0.25, alpha = 0.1)       
              
    for i in pcs:
        sns.scatterplot(x = X_EF_scores[:,i],
                        y = y,
                        hue = hue,
                        style = style,
                        ax = ax[1,i],
                        sizes=(30,15),
                        legend = False,
                        palette = palette,
                        markers = markers,
                        edgecolor='k',
                        alpha=0.9,
                        linewidth=0.5,
                        )
     
        h = stratlimits_Sassen
        ax[1,i].plot(X_EF_scores[:,i], y, color='k', linewidth = 0.5, alpha = 0.2)
        ax[1,i].axhspan(0,h[0],alpha=0.1,color = palette[0])
        ax[1,i].axhspan(h[0],h[1],alpha=0.1,color=palette[1])
        ax[1,i].axhspan(h[1],h[2],alpha=0.1,color=palette[2])
        ax[1,i].axhspan(h[2],h[3],alpha=0.1,color=palette[3])
        ax[1,i].axhspan(h[3],h[4],alpha=0.1,color=palette[4])
        ax[1,i].axhspan(h[4],h[5],alpha=0.1,color=palette[5])
        ax[1,i].axhspan(h[5],140,alpha=0.1,color=palette[6])
        ax[1,i].axhline(h[0],alpha=1,color='k', linewidth = '0.5')
        ax[1,i].axhline(h[5],alpha=1,color='k', linewidth = '0.5')
        ax[1,i].xaxis.set_minor_locator(AutoMinorLocator())
        ax[1,i].yaxis.set_minor_locator(AutoMinorLocator())
        ax[1,i].set(ylim = (0, 140))
        ax[1,i].set(xlim = (None, None))
        ax[1,i].xaxis.set_minor_locator(AutoMinorLocator())
        ax[1,i].yaxis.set_minor_locator(AutoMinorLocator())
        ax[1,i].grid(color='k', linestyle='-', axis = 'x', which = 'both', linewidth=0.25, alpha = 0.1)
        ax[1,i].set_xlabel("PC" + str(pcs[i]+1) + " (" + str(round(pca.explained_variance_ratio_[i] * 100, 2)) + " % of variance)")
        sns.despine()
        plt.savefig('Fig_8_PCA_logs_RAW.pdf')

Fig_5()
Fig_6()
Figs_7_and_8()
