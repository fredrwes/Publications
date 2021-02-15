import plotly.express as px
from dataimport import Wesenlund_et_al_MPG_data

(wong_botneheia,
 stratlimits_blanknuten,
 stratlimits_skrukkefjellet,
 df_MPG,
 df_MPG_Blanknuten,
 df_MPG_Skrukkefjellet) = Wesenlund_et_al_MPG_data()

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
fig.write_image("SAT_ARO_POL_ternary_RAW.pdf")