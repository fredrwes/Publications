
# load data
###############################################################################

import matplotlib.pyplot as plt
import seaborn as sns
from dataimport import Wesenlund_et_al_MPG_data, mplplotparams

(wong_botneheia,
stratlimits_Blanknuten,
stratlimits_Skrukkefjellet,
df_MPG,
df_MPG_Blanknuten,
df_MPG_Skrukkefjellet) = Wesenlund_et_al_MPG_data()
mplplotparams()
sns.set_palette(wong_botneheia)

# Geochemical logs
###############################################################################

columns = ['TOC (wt. %)','TIC (wt. %)','TS (wt. %)','SAT/ARO','EOM/TOC']
if columns == ['SAT/ARO','EOM/TOC']:
    df_MPG_Blanknuten = df_MPG_Blanknuten.loc[:,['SAT/ARO','EOM/TOC','Height (m)','Stratigraphic unit','Facies','Locality']].dropna()
    df_MPG_Skrukkefjellet = df_MPG_Skrukkefjellet.loc[:,['SAT/ARO','EOM/TOC','Height (m)','Stratigraphic unit','Facies','Locality']].dropna()

lokalitet = ['Blanknuten','Skrukkefjellet']
y = 'Height (m)'
hue = "Stratigraphic unit"
style = 'Facies'
size = 'Locality'
markers = ['o','D','s','P']

for s in lokalitet:
    if s == 'Blanknuten':   
        data = df_MPG_Blanknuten
    if s == 'Skrukkefjellet':
        data = df_MPG_Skrukkefjellet

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
                        cmap = wong_botneheia
                        )
        
        if s == 'Blanknuten':
            axes[j].axhspan(0,stratlimits_Blanknuten[0],alpha=0.1,color = wong_botneheia[0])
            axes[j].axhspan(stratlimits_Blanknuten[0],stratlimits_Blanknuten[1],alpha=0.1,color=wong_botneheia[1])
            axes[j].axhspan(stratlimits_Blanknuten[1],stratlimits_Blanknuten[2],alpha=0.1,color=wong_botneheia[2])
            axes[j].axhspan(stratlimits_Blanknuten[2],stratlimits_Blanknuten[3],alpha=0.1,color=wong_botneheia[3])
            axes[j].axhspan(stratlimits_Blanknuten[3],stratlimits_Blanknuten[4],alpha=0.1,color=wong_botneheia[4])
            axes[j].axhspan(stratlimits_Blanknuten[4],80,alpha=0.1,color=wong_botneheia[5])
            axes[j].axhline(0,alpha=1,color='k', linewidth = '0.5')
            axes[j].axhline(stratlimits_Blanknuten[4],alpha=1,color='k', linewidth = '0.5')
            axes[j].plot(x,y, data=data, color='k', linewidth = 0.5, alpha = 0.2)

        if s == 'Skrukkefjellet':
            axes[j].axhspan(0,stratlimits_Skrukkefjellet[0],alpha=0.1,color = wong_botneheia[0])
            axes[j].axhspan(stratlimits_Skrukkefjellet[0],stratlimits_Skrukkefjellet[1],alpha=0.1,color=wong_botneheia[1])
            axes[j].axhspan(stratlimits_Skrukkefjellet[1],stratlimits_Skrukkefjellet[2],alpha=0.1,color=wong_botneheia[2])
            axes[j].axhspan(stratlimits_Skrukkefjellet[2],stratlimits_Skrukkefjellet[3],alpha=0.1,color=wong_botneheia[3])
            axes[j].axhspan(stratlimits_Skrukkefjellet[3],stratlimits_Skrukkefjellet[4],alpha=0.1,color=wong_botneheia[4])
            axes[j].axhspan(stratlimits_Skrukkefjellet[4],80,alpha=0.1,color=wong_botneheia[5])
            axes[j].axhline(0,alpha=1,color='k', linewidth = '0.5')
            axes[j].axhline(stratlimits_Skrukkefjellet[4],alpha=1,color='k', linewidth = '0.5')
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
        
        if x == 'EOM/TOC':
           axes[j].set(xlim = (0, 0.3))
           
        if x == 'SAT/ARO':
           axes[j].set(xlim = (0.1, 15))
           axes[j].set_xscale('log')
        
        j = j + 1

    plt.suptitle(s + ' locality')
    saveloc = s + '_logs_RAW.pdf'
    plt.savefig(saveloc, bbox_inches='tight')

plt.show()