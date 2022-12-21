from os.path import join, dirname
import datetime

import pandas as pd
from scipy.signal import savgol_filter

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, DataRange1d, Select
from bokeh.palettes import Blues4
from bokeh.palettes import Sunset4
from bokeh.palettes import Spectral3
from bokeh.palettes import Vibrant3
from bokeh.palettes import HighContrast3
from bokeh.plotting import figure

STATISTICS = ['AverageTemperature', 'AverageTemperatureUncertainty']

def get_dataset(src, name, distribution):
    #df = src[src.State == name].copy()
    df = src.copy()
    df['dt']=df['dt'].astype('string')


    df['dt'] = pd.to_datetime(df.dt)
    df['month'] = df['dt'].dt.month
    df['AverageTemperature']=(df['AverageTemperature'] * 1.8) + 32
    df=df.loc[(df['State']==name),['dt',\
    'State','AverageTemperature','AverageTemperatureUncertainty','Country']]
    #& ((df['month']==5) | (df['month']==6) | (df['month']==7))
    #del df['Country']
    print('Records in df selection for',name,':',len(df))
    limit_months=600

    start_date = df.iat[0, 0].strftime('%Y-%m-%d')
    end_date = df.iat[limit_months-1, 0].strftime('%Y-%m-%d')



    df['AverageStart'] = df.head(limit_months)['AverageTemperature'].mean()
    df['AverageStartoffset'] = df['AverageStart']-.1
    # timedelta here instead of pd.DateOffset to avoid pandas bug < 0.18 (Pandas issue #11925)
    df['left'] = df.dt - datetime.timedelta(days=0.5)
    df['right'] = df.dt + datetime.timedelta(days=0.5)
    # Multiplying by 1.8 to reflect magnitude of 1 degree celsius compared with Fahrenheit
    # Dividing by 2 to reflect fact that top and bottom range of error cause an even split in the uncertainty; 
    # Therefore each (top and bottom) are equal to uncertainty/2
    df['uncertainty_top'] = df['AverageTemperature']+(df['AverageTemperatureUncertainty']*1.8)/2
    df['uncertainty_bottom'] = df['AverageTemperature']-(df['AverageTemperatureUncertainty']*1.8)/2
    df['avg_est_top']=df['AverageTemperature']+0.1
    df['avg_est_bottom']=df['AverageTemperature']-0.1
    df = df.set_index(['dt'])
    df.sort_index(inplace=True)
    if distribution == 'Smoothed':
        window, order = 51, 3
        for key in STATISTICS:
            df[key] = savgol_filter(df[key], window, order)

    return ColumnDataSource(data=df)

def make_plot(source, title):
    plot = figure(x_axis_type="datetime", width=800, tools="", toolbar_location=None)
    plot.title.text = title

    
    plot.quad(top='AverageTemperature', bottom='uncertainty_bottom', left='left', right='right',
              color=Sunset4[0], source=source, legend_label="Monthly temperature observations, one day's average reading each month")
    plot.quad(top='uncertainty_top', bottom='AverageTemperature', left='left', right='right',
              color=HighContrast3[0], source=source, legend_label="Monthly temperature observations, one day's average reading each month")
    plot.quad(top='AverageStart', bottom='AverageStartoffset', left='left', right='right',
              color=Vibrant3[0], source=source, legend_label="Average for first 50 years of record-keeping")

    # Order: HighContrast3[0], Sunset4[0], Vibrant3[0]
    # fixed attributes
    plot.xaxis.axis_label = None
    plot.yaxis.axis_label = "Temperature (F)"
    plot.axis.axis_label_text_font_style = "bold"
    plot.x_range = DataRange1d(range_padding=0.0)
    plot.grid.grid_line_alpha = 1.0

    return plot

def update_plot(attrname, old, new):
    global end_date
    state = state_select.value
    print('Updating on:',state)
    plot.title.text = "Weather data for " + states[state]

    src = get_dataset(df, state, distribution_select.value)

    source.data.update(src.data)



distribution = 'Smoothed'
df = pd.read_csv(join(dirname(__file__), 'data/GlobalLandTemperatures.csv'))

states=dict(zip(df.State, df.State + ', ' + df.Country))

# Getting first key in dictionary to seed the first state selected on startup
state = list(states.keys())[0]
print(state)
source = get_dataset(df, state, distribution)
#print('TYPE OF SOURCE IS:',type(source))

state_select = Select(value=state, title='State/City', options=sorted(states.keys()))

distribution_select = Select(value=distribution, title='Distribution', options=['Discrete', 'Smoothed'])


plot = make_plot(source, "Weather data for " + states[state])

state_select.on_change('value', update_plot)
distribution_select.on_change('value', update_plot)

controls = column(state_select, distribution_select)

curdoc().add_root(row(plot, controls))
curdoc().title = "Climate Change History"
