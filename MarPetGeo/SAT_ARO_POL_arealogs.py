
# Importing required libraries and data
###############################################################################

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib as mpl
import numpy as np
import seaborn as sns
from dataimport import Wesenlund_et_al_MPG_data
(wong_botneheia,
 stratlimits_Blanknuten,
 stratlimits_Skrukkefjellet,
 df_MPG,
 df_MPG_Blanknuten,
 df_MPG_Skrukkefjellet) = Wesenlund_et_al_MPG_data()

# Define plot settings and color palette
###############################################################################

sns.set(style="ticks")
sns.set_context("paper")
bitumencolors = ["#f6d55c","#ed553b","#4A412A"]
sns.set_palette(palette=bitumencolors)
mpl.rcParams['pdf.fonttype'] = 42
params = {'legend.fontsize': 8,
          'legend.handlelength': 2,
          'axes.linewidth' : 0.5,
          'xtick.minor.width'    : 0.5,
          'xtick.major.width'    : 0.5,
          'ytick.major.width'    : 0.5,
          'axes.labelsize'       : 10,
          'xtick.labelsize'      : 8,
          'ytick.labelsize'      : 8,
          'ytick.minor.width'    : 0.5}
plt.rcParams.update(params)

# Preparing data for plotting by splitting into separate dataframes
###############################################################################

y = 'Height (m)'
df_MPG_Blanknuten = df_MPG_Blanknuten.loc[:,[y,'SAT (mg/g rock)',
                                             'ARO (mg/g rock)',
                                             'POL (mg/g rock)']].dropna()

df_Blanknuten_height = df_MPG_Blanknuten.loc[:,y]
df_Blanknuten_EOM = df_MPG_Blanknuten.loc[:,['SAT (mg/g rock)',
                                             'ARO (mg/g rock)',
                                             'POL (mg/g rock)']]

df_MPG_Skrukkefjellet = df_MPG_Skrukkefjellet.loc[:,[y,'SAT (mg/g rock)',
                                                     'ARO (mg/g rock)',
                                                     'POL (mg/g rock)']].dropna()

df_MPG_Skrukkefjellet_N = df_MPG_Skrukkefjellet.iloc[16:] # Splitting N part
df_Skrukkefjellet_height_N = df_MPG_Skrukkefjellet_N.loc[:,y]
df_Skrukkefjellet_EOM_N = df_MPG_Skrukkefjellet_N.loc[:,['SAT (mg/g rock)',
                                                         'ARO (mg/g rock)',
                                                         'POL (mg/g rock)']]

df_MPG_Skrukkefjellet_NW = df_MPG_Skrukkefjellet.iloc[:16] # Splitting NE part
df_Skrukkefjellet_height_NW = df_MPG_Skrukkefjellet_NW.loc[:,y]
df_Skrukkefjellet_EOM_NW = df_MPG_Skrukkefjellet_NW.loc[:,['SAT (mg/g rock)',
                                                           'ARO (mg/g rock)',
                                                           'POL (mg/g rock)']]

# Plotting stacked area logs
###############################################################################

c = ["saturates","aromatics","polars (resins and asphaltenes)"]
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

## Defining stratigraphic units, boundaries, axis properties
###############################################################################

# Blanknuten
ax1.axhspan(0,stratlimits_Blanknuten[0],alpha=0.1,color = wong_botneheia[0])
ax1.axhspan(stratlimits_Blanknuten[0],stratlimits_Blanknuten[1],alpha=0.1,color=wong_botneheia[1])
ax1.axhspan(stratlimits_Blanknuten[1],stratlimits_Blanknuten[2],alpha=0.1,color=wong_botneheia[2])
ax1.axhspan(stratlimits_Blanknuten[2],stratlimits_Blanknuten[3],alpha=0.1,color=wong_botneheia[3])
ax1.axhspan(stratlimits_Blanknuten[3],stratlimits_Blanknuten[4],alpha=0.1,color=wong_botneheia[4])
ax1.axhspan(stratlimits_Blanknuten[4],80,alpha=0.1,color=wong_botneheia[5])
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
ax2.axhspan(0,stratlimits_Skrukkefjellet[0],alpha=0.1,color = wong_botneheia[0])
ax2.axhspan(stratlimits_Skrukkefjellet[0],stratlimits_Skrukkefjellet[1],alpha=0.1,color=wong_botneheia[1])
ax2.axhspan(stratlimits_Skrukkefjellet[1],stratlimits_Skrukkefjellet[2],alpha=0.1,color=wong_botneheia[2])
ax2.axhspan(stratlimits_Skrukkefjellet[2],stratlimits_Skrukkefjellet[3],alpha=0.1,color=wong_botneheia[3])
ax2.axhspan(stratlimits_Skrukkefjellet[3],stratlimits_Skrukkefjellet[4],alpha=0.1,color=wong_botneheia[4])
ax2.axhspan(stratlimits_Skrukkefjellet[4],80,alpha=0.1,color=wong_botneheia[5])
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

## Save figure and show
plt.savefig('EOM_sat_aro_pol_RAW.pdf', bbox_inches='tight')
plt.show()