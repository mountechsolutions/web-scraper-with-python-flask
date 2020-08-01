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
URL = 'https://www.worldometers.info/coronavirus/'

def df_process(cov_df):
    try:
        num_columns = ['Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 
                       'Total Recovered', 'Active Cases','Critical Cases', 
                       'Tot Cases per 1M pop','Tot Deaths per 1M pop', 'Total Tests', 
                       'Tests per 1M pop', 'Population']
        for col in num_columns:
            cov_df = cov_df.replace('N/A', '')
            cov_df[col] = cov_df[col].apply(lambda x: x.strip().replace(',', ''))
            cov_df[col] = pd.to_numeric(cov_df[col])
            cov_df[col] = cov_df[col].fillna(0).astype(int)
    except:
        pass
    return cov_df
    
def obtain_corona_data(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    # results = soup.find_all('tr')
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
    df_curr = df.iloc[:int((len(df) - 2) / 3), :]
    df_curr.drop(df_curr.columns[[7,16,17,18,19]], axis=1, inplace=True)
    df_curr = df_curr.iloc[:,1:].reset_index(drop=True)
    columns = ['Country', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 'Active Cases',
               'Critical Cases', 'Tot Cases per 1M pop',
               'Tot Deaths per 1M pop', 'Total Tests', 'Tests per 1M pop', 'Population','Continent']
    df_curr.columns = columns
    df_curr = df_curr[~df_curr['Country'].isin(['Country,Other','Total:'])].reset_index(drop=True)
    #df_curr = df_process(df_curr)
    return df_curr
```


