from config import *

js = json.loads("""
{
    "id": "2020RATIO011001",
    "realtime_start": "2017-08-15",
    "realtime_end": "2017-08-15",
    "title": "Income Inequality in District of Columbia",
    "observation_start": "2010-01-01",
    "observation_end": "2015-01-01",
    "frequency": "Annual",
    "frequency_short": "A",
    "units": "Ratio",
    "units_short": "Ratio",
    "seasonal_adjustment": "Not Seasonally Adjusted",
    "seasonal_adjustment_short": "NSA",
    "last_updated": "2017-02-10 16:12:36-06",
    "popularity": 14,
    "notes": "This data represents the ratio of the mean income for the highest quintile (top 20 percent) of earners divided by the mean income of the lowest quintile (bottom 20 percent) of earners in a particular county."
}
""")

js['id'] = 'fred_' + js['id']
js['unit'] = js.pop('units')
js['last_update'] = js.pop('last_updated')
js['note'] = js.pop('notes')
js['series_attr'] = {
    'realtime_start': js.pop('realtime_start')
    , 'realtime_end': js.pop('realtime_end')
    , 'frequency_short': js.pop('frequency_short')
    , 'units_short': js.pop('units_short')
    , 'seasonal_adjustment_short': js.pop('seasonal_adjustment_short')
    , 'popularity': js.pop('popularity')
}

print(js)