# web-scraper-with-python-flask

Ideas taught: 
* Web scraping using beautifulsoup
* data analysis and visualization
* Forecasting algorithms
* Flask web app

Required skills: pandas basic, concept of html, css

Data Source: 
* https://www.worldometers.info/coronavirus/,
* https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv,
* https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv
* https://www.worldometers.info/coronavirus/country/nepal/
* https://coronanepal.live/

### Explore Webscraping. Try this command to begin
```
from bs4 import BeautifulSoup
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
table_data = soup.find_all('tr', style="")
tds = []
for td in table_data:
  tds.append(td.text)
  tds = [td.split('\n') for td in tds]
  ths = tds[0]
  l = len(ths)
  thss = ths[1:l - 1]
  tdsss = tds[1:]
  tdsss = [tds[1:len(tds) - 1] for tds in tdsss]
  df = pd.DataFrame(tdsss)
```


