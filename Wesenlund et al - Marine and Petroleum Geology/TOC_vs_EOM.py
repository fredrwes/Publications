
# Importing required libraries and data
###############################################################################

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
from dataimport import Wesenlund_et_al_MPG_data, mplplotparams
(wong_botneheia,
 stratlimits_blanknuten,
 stratlimits_skrukkefjellet,
 df_MPG,
 df_MPG_Blanknuten,
 df_MPG_Skrukkefjellet) = Wesenlund_et_al_MPG_data()

mplplotparams()
sns.set_palette(wong_botneheia)

# Assign variables
###############################################################################

x = 'TOC (wt. %)'
y = 'EOM (mg/g rock)'
style = 'Facies'
size = 'Locality'
hue = 'Stratigraphic unit'

# Drawing dashed lines in EOM vs TOC template, plotting and saving figure
###############################################################################

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
                )

ax.set_xlim(0.1, 100)
ax.set_ylim(0.1, 100)
ax.set(xscale="log", yscale="log")
ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
plt.savefig('TOC_vs_EOM_RAW.pdf')
plt.show()