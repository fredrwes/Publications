import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import AutoMinorLocator
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px

# Setting plotting aesthethics
sns.set(style="ticks")
sns.set_context("paper")
mpl.rcParams['pdf.fonttype'] = 42
params = {'legend.fontsize': 6,
      'legend.handlelength': 2,
      'axes.linewidth' : 0.5,
      'xtick.minor.width'    : 0.5,
      'xtick.major.width'    : 0.5,
      'ytick.major.width'    : 0.5,
      'axes.labelsize'       : 8,
      'xtick.labelsize'      : 6,
      'ytick.labelsize'      : 6,
      'ytick.minor.width'    : 0.5}
plt.rcParams.update(params)

stratlimits_Blanknuten = [35, # lower to middle - upper Muen Mb height (m)
                          42.4, # upper Muen Mb - lower Blanknuten Mb height (m)
                          51.9, # lower - middle Blanknuten Mb height (m)
                          66.45, # middle - upper Blanknuten mb height (m)
                          75.4] # upper Blanknuten mb - Tschermakfjellet Fm height (m)

stratlimits_Skrukkefjellet = [32.5, # lower to middle - upper Muen Mb height (m)
                              34.5, # upper Muen Mb - lower Blanknuten Mb height (m)
                              50.8, # lower - middle Blanknuten Mb height (m)
                              66.25, # middle - upper Blanknuten mb height (m)
                              71] # upper Blanknuten mb - Tschermakfjellet Fm height (m)

# Color palette (Wong, 2011 - https://www.nature.com/articles/nmeth.1618)
wong_Botneheia = ['#F0E442','#E69F00','#56B4E9','#009E73','#0072B2','#CC79A7'] 
df_MPG = pd.read_excel('Appendix_A.xlsx')
df_MPG = df_MPG.set_index('Locality') # split data into locality:
df_MPG_Blanknuten = df_MPG.loc["Blanknuten"] # Blanknuten
df_MPG_Skrukkefjellet = df_MPG.loc["Skrukkefjellet"] # Skrukkefjellet
df_MPG.reset_index(inplace=True) # reset index
df_MPG_Blanknuten.reset_index(inplace=True) # reset index
df_MPG_Skrukkefjellet.reset_index(inplace=True) # reset index

def fig_9():
    locality = ['Blanknuten','Skrukkefjellet']
    y = 'Height (m)'
    hue = "Stratigraphic unit"
    style = 'Facies'
    size = 'Locality'
    markers = ['o','D','s','P']
    columns = ['TOC (wt. %)','TIC (wt. %)','TS (wt. %)']
        
    for s in locality:
        if s == 'Blanknuten':   
            data = df_MPG_Blanknuten
            sl = stratlimits_Blanknuten
        if s == 'Skrukkefjellet':
            data = df_MPG_Skrukkefjellet
            sl = stratlimits_Skrukkefjellet
    
        f, axes = plt.subplots(1, len(columns), sharey = True, squeeze = True, figsize=(6, 6))
        plt.subplots_adjust(wspace=0.05, hspace=0)
        j = 0
        
        for x in columns:
            sns.scatterplot(y=y,
                            x=x,
                            data=data,
                            ax=axes[j],
                            hue = hue,
                            style = style,
                            size = size,
                            s = 10,
                            edgecolor='k',
                            markers = markers,
                            alpha = 0.9,
                            linewidth=0.5,
                            palette = wong_Botneheia
                            )
            
            axes[j].axhspan(0,stratlimits_Blanknuten[0],alpha=0.1,color = wong_Botneheia[0])
            axes[j].axhspan(sl[0],sl[1],alpha=0.1,color=wong_Botneheia[1])
            axes[j].axhspan(sl[1],sl[2],alpha=0.1,color=wong_Botneheia[2])
            axes[j].axhspan(sl[2],sl[3],alpha=0.1,color=wong_Botneheia[3])
            axes[j].axhspan(sl[3],sl[4],alpha=0.1,color=wong_Botneheia[4])
            axes[j].axhspan(sl[4],80,alpha=0.1,color=wong_Botneheia[5])
            axes[j].axhline(0,alpha=1,color='k', linewidth = '0.5')
            axes[j].axhline(sl[4],alpha=1,color='k', linewidth = '0.5')
            axes[j].plot(x,y, data=data, color='k', linewidth = 0.5, alpha = 0.2)
            axes[j].set(ylim = (0, 80))
            axes[j].set(ylim = (0, None))
            axes[j].grid(color='k', linestyle='-', axis = 'x', which = 'both', linewidth=0.25, alpha = 0.1)
            legend = axes[j].legend()
            legend.remove()
            sns.despine()
            
            if x == 'TOC (wt. %)':
                axes[j].set(xlim = (0, 13))
            
            if x == 'TS (wt. %)':
                axes[j].set(xlim = (0, 4))
                
            if x == 'TIC (wt. %)':
                axes[j].set(xlim = (0, 8))
                
            j = j + 1
    
        plt.suptitle(s + ' locality')
        saveloc = 'Fig_9_' + s + '_UNEDITED.pdf'
        plt.savefig(saveloc, bbox_inches='tight')
    plt.show()
    
def fig_10():
    f, ax = plt.subplots(1, squeeze = True, figsize=(6, 4))
    sns.scatterplot(x='TOC (wt. %)',
                    y='TS (wt. %)',
                    data=df_MPG,
                    hue = "Stratigraphic unit",
                    style = 'Facies',
                    size = 'Locality',
                    sizes = (50,20),
                    edgecolor='k',
                    alpha = 0.9,
                    linewidth=0.5,
                    markers = ['o','D','s','P'],
                    legend = 'brief',
                    palette = wong_Botneheia
                    )
    
    x = np.linspace(0, df_MPG['TOC (wt. %)'].max(), 2)
    
    # TOC/TS = 6.5, from Alsenz et al. (2015, Figure 3)
    plt.plot(x, x/6.5, color = 'k', linestyle = "-", linewidth=0.5)
    plt.text(10,2,'TOC/TS = 6.5')
    
    # Normal marine trend line, from Berner and Raiswell (1984, Figure 2)
    plt.plot(x, x/2.8, color = 'b', linestyle = "-", linewidth=0.5)
    plt.text(8.5,4,'Normal marine',color='b')
    
    # Upper marine boundary, from Berner and Raiswell (1984, Figure 2)
    x = np.linspace(0,4.7,100)
    plt.plot(x, -0.0766*x**2 + 0.775*x, color = 'b', linestyle = ":", linewidth=1)
    
    # Lower marine boundary, from Berner and Raiswell (1984, Figure 2)
    x = np.linspace(0,5.3,100)
    plt.plot(x, 0.0413*x**2 + 0.0615*x, color = 'b', linestyle = ":", linewidth=1)
    
    plt.xlim([0, None])
    plt.ylim([0, None])
    saveloc = 'Fig_10_UNEDITED.pdf'
    plt.savefig(saveloc, bbox_inches='tight')
    plt.show()

def fig_13():
    y = 'Height (m)'
    fracs =  ['SAT (mg/g rock)','ARO (mg/g rock)','POL (mg/g rock)']
    bitumencolors = ["#f6d55c", # SAT fraction
                     "#ed553b", # ARO fraction
                     "#4A412A"] # POL fraction
    
    sns.set_palette(palette=bitumencolors)
    df_MPG_Blanknuten_mod = df_MPG_Blanknuten.loc[:,[y,'SAT (mg/g rock)',
                                                       'ARO (mg/g rock)',
                                                       'POL (mg/g rock)']].dropna()
    
    df_Blanknuten_height = df_MPG_Blanknuten_mod.loc[:,y]
    df_Blanknuten_EOM = df_MPG_Blanknuten_mod.loc[:,fracs]
    df_MPG_Skrukkefjellet_mod = df_MPG_Skrukkefjellet.loc[:,[y,'SAT (mg/g rock)',
                                                               'ARO (mg/g rock)',
                                                               'POL (mg/g rock)']].dropna()
    
    df_MPG_Skrukkefjellet_N = df_MPG_Skrukkefjellet_mod.iloc[16:] # Splitting N part
    df_Skrukkefjellet_height_N = df_MPG_Skrukkefjellet_N.loc[:,y]
    df_Skrukkefjellet_EOM_N = df_MPG_Skrukkefjellet_N.loc[:,fracs]
    
    df_MPG_Skrukkefjellet_NW = df_MPG_Skrukkefjellet_mod.iloc[:16] # Splitting NE part
    df_Skrukkefjellet_height_NW = df_MPG_Skrukkefjellet_NW.loc[:,y]
    df_Skrukkefjellet_EOM_NW = df_MPG_Skrukkefjellet_NW.loc[:,fracs]
    
    # Plotting stacked area logs
    ###############################################################################
    fig, (ax1, ax2) = plt.subplots(1, 2,
                                   squeeze = True,
                                   figsize=(4, 6),
                                   sharey = True)
    
    plt.subplots_adjust(wspace=0.1, hspace=0)
    
    data1 = np.cumsum(df_Blanknuten_EOM.values, axis=1)
    for i, col in enumerate(df_Blanknuten_EOM.columns):
        ax1.fill_betweenx(df_Blanknuten_height,
                          data1[:,i],
                          label=col,
                          zorder=-i,
                          edgecolor = 'k',
                          alpha = 1)
    ax1.hlines(data = df_MPG_Blanknuten, xmin = 0, xmax = 'EOM (mg/g rock)', y = 'Height (m)', linewidth = 0.5, color = 'grey')
    
    data2 = np.cumsum(df_Skrukkefjellet_EOM_NW.values, axis=1)
    for i, col in enumerate(df_Skrukkefjellet_EOM_NW.columns):
        ax2.fill_betweenx(df_Skrukkefjellet_height_NW,
                          data2[:,i],
                          label=col,
                          zorder=-i,
                          edgecolor = 'k',
                          alpha = 1)
    
    data2 = np.cumsum(df_Skrukkefjellet_EOM_N.values, axis=1)
    for i, col in enumerate(df_Skrukkefjellet_EOM_N.columns):
        ax2.fill_betweenx(df_Skrukkefjellet_height_N,
                          data2[:,i],
                          label=col,
                          zorder=-i,
                          edgecolor = 'k',
                          alpha = 1)
    ax2.hlines(data = df_MPG_Skrukkefjellet, xmin = 0, xmax = 'EOM (mg/g rock)', y = 'Height (m)', linewidth = 0.5, color = 'grey')
    
    ## Defining stratigraphic units, boundaries, axis properties
    ###############################################################################
    
    # Blanknuten
    ax1.axhspan(0,stratlimits_Blanknuten[0],alpha=0.1,color = wong_Botneheia[0])
    ax1.axhspan(stratlimits_Blanknuten[0],stratlimits_Blanknuten[1],alpha=0.1,color=wong_Botneheia[1])
    ax1.axhspan(stratlimits_Blanknuten[1],stratlimits_Blanknuten[2],alpha=0.1,color=wong_Botneheia[2])
    ax1.axhspan(stratlimits_Blanknuten[2],stratlimits_Blanknuten[3],alpha=0.1,color=wong_Botneheia[3])
    ax1.axhspan(stratlimits_Blanknuten[3],stratlimits_Blanknuten[4],alpha=0.1,color=wong_Botneheia[4])
    ax1.axhspan(stratlimits_Blanknuten[4],80,alpha=0.1,color=wong_Botneheia[5])
    ax1.axhline(0,alpha=1,color='k', linewidth = '0.5')
    ax1.axhline(stratlimits_Blanknuten[4],alpha=1,color='k', linewidth = '0.5')
    ax1.set(xlim = (0, None))
    ax1.grid(color='k', linestyle='-', axis = 'x', which = 'both', linewidth=0.25, alpha = 0.1)
    
    ax1.set_title('Blanknuten section')
    ax1.margins(y=0)
    ax1.set_xlim(0, 22)
    ax1.set_ylim(0, 80)
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.set_xlabel('EOM (mg/g rock)')
    ax1.set_ylabel('Log height (m)')
    
    # Skrukkefjellet
    ax2.axhspan(0,stratlimits_Skrukkefjellet[0],alpha=0.1,color = wong_Botneheia[0])
    ax2.axhspan(stratlimits_Skrukkefjellet[0],stratlimits_Skrukkefjellet[1],alpha=0.1,color=wong_Botneheia[1])
    ax2.axhspan(stratlimits_Skrukkefjellet[1],stratlimits_Skrukkefjellet[2],alpha=0.1,color=wong_Botneheia[2])
    ax2.axhspan(stratlimits_Skrukkefjellet[2],stratlimits_Skrukkefjellet[3],alpha=0.1,color=wong_Botneheia[3])
    ax2.axhspan(stratlimits_Skrukkefjellet[3],stratlimits_Skrukkefjellet[4],alpha=0.1,color=wong_Botneheia[4])
    ax2.axhspan(stratlimits_Skrukkefjellet[4],80,alpha=0.1,color=wong_Botneheia[5])
    ax2.axhline(0,alpha=1,color='k', linewidth = '0.5')
    ax2.axhline(stratlimits_Skrukkefjellet[4],alpha=1,color='k', linewidth = '0.5')
    ax2.set(xlim = (0, None))
    ax2.grid(color='k', linestyle='-', axis = 'x', which = 'both', linewidth=0.25, alpha = 0.1)
    
    ax2.set_title('Skrukkefjellet composite section')
    ax2.margins(y=0)
    ax2.set_xlim(0, 22)
    ax2.set_ylim(-2, 80)
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.set_xlabel('EOM (mg/g rock)')
    ax1.set_ylabel('Log height (m)')
    
    ## Save figure and show
    plt.savefig('Fig_13_UNEDITED.pdf', bbox_inches='tight')
    plt.show()
    
def fig_14():
    fig = px.scatter_ternary(df_MPG,
    a="SAT (%)",
    b="ARO (%)",
    c="POL (%)",
    color="Stratigraphic unit",
    symbol="Facies",
    size="Locality_size",
    size_max=8,
    template="simple_white",
    color_discrete_map = {
        "Lower-Middle Muen Mb": '#F0E442',
        'Upper Muen Mb': "#E69F00",
        "Lower Blanknuten Mb": "#56B4E9",
        "Middle Blanknuten Mb": "#009E73",
        "Upper Blanknuten Mb": "#0072B2",
        "Tschermakfjellet Fm": "#CC79A7",
        }
    )
    
    fig.update_traces(marker=dict(opacity=0.9,
                                  line=dict(width=0.5,
                                            color='black')),
                      selector=dict(mode='markers'))
    
    def makeAxis(title, tickangle):
        return {
          'title': title,
          'titlefont': { 'size': 20 },
          'tickangle': tickangle,
          'tickfont': { 'size': 10 },
          'tickcolor': 'rgba(0,0,0,0)',
          'ticklen': 5,
          'showline': True,
        #  'showgrid': True
        }
    
    fig.update_layout({
        'ternary': {
            'sum': 100,
            #'aaxis': makeAxis('SAT %', 0),
            #'baxis': makeAxis('<br>ARO %', 45),
            #'caxis': makeAxis('<br>POL %', -45)
        },
        'annotations': [{
          'showarrow': False,
          'text': 'Simple Ternary Plot with Markers',
            'x': 0.5,
            'y': 1.3,
            'font': { 'size': 15 }
        }]
    })
    
    fig.update_ternaries(caxis_min = 45)
    
    fig.show()
    fig.write_image("Fig_14_UNEDITED.pdf")

def fig_15():
    locality = ['Blanknuten','Skrukkefjellet']
    y = 'Height (m)'
    hue = "Stratigraphic unit"
    style = 'Facies'
    size = 'Locality'
    markers = ['o','D','s','P']
    columns = ['SAT/ARO','EOM/TOC']
       
    for s in locality:
        if s == 'Blanknuten':   
            data = df_MPG_Blanknuten.loc[:,['SAT/ARO','EOM/TOC','Height (m)','Stratigraphic unit','Facies','Locality']].dropna()
            sl = stratlimits_Blanknuten
        if s == 'Skrukkefjellet':
            data = df_MPG_Skrukkefjellet.loc[:,['SAT/ARO','EOM/TOC','Height (m)','Stratigraphic unit','Facies','Locality']].dropna()
            sl = stratlimits_Skrukkefjellet
    
        f, axes = plt.subplots(1, len(columns), sharey = True, squeeze = True, figsize=(6, 6))
        plt.subplots_adjust(wspace=0.05, hspace=0)
        j = 0
        
        for x in columns:
            sns.scatterplot(y=y,
                            x=x,
                            data=data,
                            ax=axes[j],
                            hue = hue,
                            style = style,
                            size = size,
                            s = 10,
                            edgecolor='k',
                            markers = markers,
                            alpha = 0.9,
                            linewidth=0.5,
                            palette = wong_Botneheia
                            )
            
            axes[j].axhspan(0,stratlimits_Blanknuten[0],alpha=0.1,color = wong_Botneheia[0])
            axes[j].axhspan(sl[0],sl[1],alpha=0.1,color=wong_Botneheia[1])
            axes[j].axhspan(sl[1],sl[2],alpha=0.1,color=wong_Botneheia[2])
            axes[j].axhspan(sl[2],sl[3],alpha=0.1,color=wong_Botneheia[3])
            axes[j].axhspan(sl[3],sl[4],alpha=0.1,color=wong_Botneheia[4])
            axes[j].axhspan(sl[4],80,alpha=0.1,color=wong_Botneheia[5])
            axes[j].axhline(0,alpha=1,color='k', linewidth = '0.5')
            axes[j].axhline(sl[4],alpha=1,color='k', linewidth = '0.5')
            axes[j].plot(x,y, data=data, color='k', linewidth = 0.5, alpha = 0.2)
            axes[j].set(ylim = (0, 80))
            axes[j].set(ylim = (0, None))
            axes[j].grid(color='k', linestyle='-', axis = 'x', which = 'both', linewidth=0.25, alpha = 0.1)
            legend = axes[j].legend()
            legend.remove()
            sns.despine()
            
            if x == 'EOM/TOC':
                axes[j].set(xlim = (0, 0.3))
           
            if x == 'SAT/ARO':
                axes[j].set(xlim = (0.1, 15))
                axes[j].set_xscale('log')
                
            j = j + 1
    
        plt.suptitle(s + ' locality')
        saveloc = 'Fig_15_' + s + '_UNEDITED.pdf'
        plt.savefig(saveloc, bbox_inches='tight')
    plt.show()

def fig_16():
    x = 'TOC (wt. %)'
    y = 'EOM (mg/g rock)'
    style = 'Facies'
    size = 'Locality'
    hue = 'Stratigraphic unit'

    # DUNEDITEDing dashed lines in EOM vs TOC template, plotting and saving figure
    #########################################################################

    fig, ax = plt.subplots(1,1, figsize=(6, 4), squeeze = True,)
    ax.plot([0.1,100],[0.1,100], '--', color = 'k', linewidth = '0.5')
    ax.plot([0.1,5],[0.2,10], '--', color = 'k', linewidth = '0.5')
    ax.plot([5,50],[10,100], '--', color = 'k', linewidth = '0.5')
    ax.plot([0.1,20],[0.5,100], '--', color = 'k', linewidth = '0.5')
    ax.plot([0.25,5],[0.5,0.5], '--', color = 'k', linewidth = '0.5')
    ax.plot([0.3,0.3],[0.1,0.25], '--', color = 'k', linewidth = '0.5')
    ax.plot([0.3,0.3],[0.1,0.25], '--', color = 'k', linewidth = '0.5')
    ax.plot([2.5,100],[0.25,10], '--', color = 'k', linewidth = '0.5')
    ax.plot([2,40],[4,4], '--', color = 'k', linewidth = '0.5')
    ax.plot([0.125,2.5],[0.25,0.25], '--', color = 'k', linewidth = '0.5')
    ax.plot([0.5,10],[1,1], '--', color = 'k', linewidth = '0.5')
    ax.plot([1,20],[2,2], '--', color = 'k', linewidth = '0.5')
    ax.plot([5,100],[10,10], '--', color = 'k', linewidth = '0.5')
    ax.arrow(4,0.5,40,5, head_width=0, head_length=0, fc='k', ec='k')
    ax.text(0.5,0.15,'Gas source (possibly biogenic)')
    ax.text(0.2,7,'Impregnation')
    ax.text(0.115,0.125,'Non\nsource')
    ax.text(6,0.4,'Improved oil source quality', rotation = 33)
    ax.text(5,30,'EOM/TOC=0.5', rotation = 33, fontsize = 8)
    ax.text(12.5,30,'EOM/TOC=0.2', rotation = 33, fontsize = 8)
    ax.text(25,30,'EOM/TOC=0.1', rotation = 33, fontsize = 8)
    
    sns.scatterplot(x=x,
                    y=y,
                    style=style,
                    data=df_MPG,
                    size=size,
                    sizes = (50,20),
                    markers = ['o','D','s','P'],
                    hue=hue,
                    legend='brief',
                    edgecolor='k',
                    alpha = 0.9,
                    linewidth=0.5,
                    palette=wong_Botneheia
                    )
    
    ax.set_xlim(0.1, 100)
    ax.set_ylim(0.1, 100)
    ax.set(xscale="log", yscale="log")
    ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    plt.savefig('Fig_16_UNEDITED.pdf')
    plt.show()

def fig_17():
    
    # The PCA analysis code is based on Serafeim Loukas's original post (CC BY-SA 4.0)
    # on StackExchange (https://stackoverflow.com/a/50845697/5025009). S. Loukas's
    # code was modified to fit the aim of this scientific contribution.
    # The code below is licensed under CC BY-SA 4.0.
    # Link to licence: https://creativecommons.org/licenses/by-sa/4.0/    
        
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
    def pcaplot(pcax, pcay, score, coeff):
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
                        palette = wong_Botneheia,
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
    
    pcaplot(1, 2, df_afterPCA[:, 0:2], np.transpose(pca.components_[0:3, :]))
    plt.savefig('Fig_17_UNEDITED.pdf')

def fig_18():
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
    colordict = dict(zip(stratunits.unique(), wong_Botneheia))
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
    plt.savefig('Fig_18_UNEDITED.pdf')

def make_stats():
    categories = ['Stratigraphic unit','Facies','Cluster']
    d = {}
    
    for c in categories:
        d[c] = df_MPG.groupby(c).agg({
        'TOC (wt. %)'     : ['count','min', np.median, np.std, 'max'],
        'TIC (wt. %)'     : [        'min', np.median, np.std, 'max'],
        'TS (wt. %)'      : [        'min', np.median, np.std, 'max'],
        'TOC/TS'          : [        'min', np.median, np.std, 'max'],
        'SAT (mg/g rock)' : ['count','min', np.median, np.std, 'max'],
        'ARO (mg/g rock)' : [        'min', np.median, np.std, 'max'],
        'POL (mg/g rock)' : [        'min', np.median, np.std, 'max'],
        'EOM (mg/g rock)' : [        'min', np.median, np.std, 'max'],
        'EOM/TOC'         : [        'min', np.median, np.std, 'max'],
        'SAT (%)'         : [        'min', np.median, np.std, 'max'],
        'ARO (%)'         : [        'min', np.median, np.std,'max'],
        'POL (%)'         : [        'min', np.median, np.std,'max'],
        'SAT/ARO'         : [        'min', np.median, np.std,'max'],
        }).round(2)
            
    table_concat = pd.concat([d['Stratigraphic unit'], d['Facies'], d['Cluster']], axis = 0).T
    table_concat.to_excel('Wesenlund_et_al_MPG_stats.xlsx')
    print(table_concat)

# Plotting figures and generating .pdfs

def plot_all_figs():
    fig_9()
    fig_10()
    fig_13()
    fig_14()
    fig_15()
    fig_16()
    fig_17()
    fig_18()

#plot_all_figs()
#make_stats()
