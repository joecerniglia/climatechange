## Climate Change on Earth During the Last 150 - 270 Years

Climate change works slowly but over centuries can be quite visible. This website I created demonstrates that no place on Earth can
remain unaffected, although certain cities in Brazil and island regions such as Hawaii appear to have been particularly vulnerable.

The website that this code actualizes may be found here:
https://climatehistorygraph.herokuapp.com/main

The dataset the website uses is from Kaggle: https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data?select=GlobalLandTemperaturesByState.csv by way of Berkeley Earth, https://berkeleyearth.org/data/.

The discrete distribution view shows how uncertainty in weather measurements has decreased over the years. Longer vertical lines in the earlier years signal an uncertainty factor, arising from the use of mercury thermometers, which can be less reliable if measurements are not taken very quickly. In the 1940s, weather stations moved to airports, which also introduces some uncertainty for purposes of comparison.

The dataset has one daily average observation for the first of each month, so certain extreme weather events may be missing. The intent of the graph
is to show long-term trends, not short-term events.

The orange line is the average monthly reading for the first 50 years of record-keeping for the given city or state. 

When looking at the thick blue band in the middle of each graph, bear in mind that this is a cluster of values tending toward the average </br>
monthly climate over a given year. High uncertainty and/or extreme weather events on the first of each month can on rare occasions make </br>
the 50-year average appear distorted, when in fact it is merely reflecting values outside the blue band.

The smoothing algorithm used for smoothed distributions is a Savitsky-Golay filter, pioneered by chemist Abraham Savitsky (1919-1989) and mathematician
Marcel J.E. Golay (1902-1989).

Special thanks must be accorded to: 

Bryan Van de Ven, co-inventor of the Python Bokeh library that makes these graphs possible, and whose "Weather Examples" source code, https://github.com/bokeh/bokeh/tree/main/examples/server/app/weather, provided a starting point for this graph; and

Jo Lorden, whose Medium article, provided useful instruction on the special requirements for deploying this website to Heroku. https://medium.com/@jodorning/how-to-deploy-a-bokeh-app-on-heroku-486d7db28299. 
