import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

# Importing Excel-file and making three dataframes:
# - All data from both localities
# - Data from Blanknuten locality only
# - Data from Skrukkefjellet (W and NW) localities only

def Wesenlund_et_al_MPG_data():
     stratlimits_blanknuten = [35, # lower to middle - upper Muen Mb height (m)
                               42.4, # upper Muen Mb - lower Blanknuten Mb height (m)
                               51.9, # lower - middle Blanknuten Mb height (m)
                               66.45, # middle - upper Blanknuten mb height (m)
                               75.4] # upper Blanknuten mb - Tschermakfjellet Fm height (m)
     
     stratlimits_skrukkefjellet = [32.5, # lower to middle - upper Muen Mb height (m)
                                   34.5, # upper Muen Mb - lower Blanknuten Mb height (m)
                                   50.8, # lower - middle Blanknuten Mb height (m)
                                   66.25, # middle - upper Blanknuten mb height (m)
                                   71] # upper Blanknuten mb - Tschermakfjellet Fm height (m)
     
     # Color palette (Wong, 2011 - https://www.nature.com/articles/nmeth.1618)
     wong_botneheia = ['#F0E442','#E69F00','#56B4E9','#009E73','#0072B2','#CC79A7'] 
     df_MPG = pd.read_excel('Appendix_A.xlsx')
     df_MPG = df_MPG.set_index('Locality') # split data into locality:
     df_MPG_Blanknuten = df_MPG.loc["Blanknuten"] # Blanknuten
     df_MPG_Skrukkefjellet = df_MPG.loc["Skrukkefjellet"] # Skrukkefjellet
     df_MPG.reset_index(inplace=True) # reset index
     df_MPG_Blanknuten.reset_index(inplace=True) # reset index
     df_MPG_Skrukkefjellet.reset_index(inplace=True) # reset index
     
     return (wong_botneheia,
             stratlimits_blanknuten,
             stratlimits_skrukkefjellet,
             df_MPG,
             df_MPG_Blanknuten,
             df_MPG_Skrukkefjellet)

# Setting plotting aesthethics
def mplplotparams():
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