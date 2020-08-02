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
    df_curr = df_process(df_curr)
    return df_curr
df_curr =obtain_corona_data(URL)

def nep2eng_num(nep_num):
    d = {'१':'1','२':'2','३':'3','४':'4','५':'5','६':'6','७':'7','८':'8','९':'9','०':'0'}  
    eng_num = ''.join(d[s] for s in nep_num if s in d.keys())
    return eng_num

def obtain_nepal_reg_data():
    url_covnepal = 'https://covidnepal.live/'
    page = requests.get(url_covnepal)
    soup = BeautifulSoup(page.content, 'html.parser')
    res = soup.find_all('th')
    vals = []
    for r in res:
        vals.append(r.text)
    vals = np.asarray(vals)
    vals = list(vals.reshape(int(len(vals)/5),5))
    nep_reg_df = pd.DataFrame(vals[1:],columns=vals[0])
    nep_reg_df.columns = ['States','Total Cases','Active Cases','Recovered Cases','Deaths']
    nep_reg_df.index = nep_reg_df.index+1
    nep_reg_df['States'] = nep_reg_df['States'].apply(lambda x:nr.romanize_text(x).capitalize() )
    nep_reg_df['States'] = nep_reg_df['States'].apply(lambda x: 'State No. '+nep2eng_num(x) if nep2eng_num(x)!='' else x )
    nep_reg_df['Total Cases'] = nep_reg_df['Total Cases'].apply(lambda x:nep2eng_num(x) )
    nep_reg_df['Active Cases'] = nep_reg_df['Active Cases'].apply(lambda x:nep2eng_num(x) )
    nep_reg_df['Recovered Cases'] = nep_reg_df['Recovered Cases'].apply(lambda x:nep2eng_num(x) )
    nep_reg_df['Deaths'] = nep_reg_df['Deaths'].apply(lambda x:nep2eng_num(x) )
    return nep_reg_df

nepal_reg_data =obtain_nepal_reg_data()
```


