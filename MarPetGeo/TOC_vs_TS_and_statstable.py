import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from dataimport import Wesenlund_et_al_MPG_data, mplplotparams
wong_botneheia, stratlimits_blank, stratlimits_skrukk, df_MPG, df_MPG_Blanknuten, df_MPG_Skrukkefjellet = Wesenlund_et_al_MPG_data()
mplplotparams()
sns.set_palette(wong_botneheia)

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
                cmap = wong_botneheia
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
saveloc = 'TOC_vs_TS_RAW.pdf'
plt.savefig(saveloc, bbox_inches='tight')
plt.show()

############ Making tables

tbl_stratunit = df_MPG.groupby(['Stratigraphic unit']).agg({
'TOC (wt. %)': ['count','min', np.median, np.std,'max'],
'TIC (wt. %)': [        'min', np.median, np.std, 'max'],
'TS (wt. %)' : [        'min', np.median, np.std,'max'],
}).round(2)

tbl_lithofacies = df_MPG.groupby(['Facies']).agg({
'TOC (wt. %)': ['count','min', np.median, np.std, 'max'],
'TIC (wt. %)': [        'min', np.median, np.std, 'max'],
'TS (wt. %)' : [        'min', np.median, np.std, 'max'],
}).round(2)

tbl = pd.concat([tbl_stratunit, tbl_lithofacies], axis = 0)
tbl = tbl.T
tbl.to_excel('Wesenlund_et_al_stats_MPG.xlsx')
print(tbl.to_string())