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

def obtain_nepal_dstrct_data():
    url_covnepal = 'https://coronanepal.live/'
    page = requests.get(url_covnepal)
    soup = BeautifulSoup(page.content, 'html.parser')
    res = soup.find_all('table',id="example")
    vals = []
    for r in res:
        theads = r.find_all('th')
        tbody = r.find_all('td')
        ths = []
        tbs = []
        for th in theads:
            ths.append(th.text)
        for tb in tbody:
            tbs.append(tb.text)
        tbs = np.asarray(tbs)
        tbs = list(tbs.reshape(int(len(tbs)/6),6))
    nepal_reg = pd.DataFrame(columns=ths, data=tbs)
    nepal_reg = nepal_reg.iloc[:,1:]
    nepal_reg.columns = ['Districts','Total Cases','New Cases','Deaths', 'Recovered']
    nepal_reg['Districts'] = nepal_reg['Districts'].apply(lambda x: x.capitalize())
    districts_dict= {'Nawalparasi1':'Nawalpur','Nawalparasi2':'Parasi',
              'Rukum1':'Eastern Rukum', 'Rukum2':'Western Rukum',
                    'Sindhupalchowk':'Sindhupalchok','Terathum':'Terhathum',
                    'Kavre':'Kavrepalanchok','Dhanusha': 'Dhanusa',
                    'Kapilbastu':'Kapilvastu','Dang':'Dang Deukhuri',
                    'Tanahu':'Tanahun','Illam':'Ilam'}
    nepal_reg['Districts'] = nepal_reg['Districts'].replace(districts_dict)
    nepal_reg['Deaths'] = nepal_reg['Deaths'].apply(lambda x: nep2eng_num(x))
    nepal_reg['Recovered'] = nepal_reg['Recovered'].apply(lambda x: nep2eng_num(x))
    nepal_reg = nepal_reg.loc[:,['Districts','Total Cases','Deaths', 'Recovered']]
    dataa = pd.read_csv('provincedstrct_nepal.csv')
    prov_reg = pd.DataFrame()
    prov_reg['Districts'] = dataa.iloc[0:,0].apply(lambda x: x.split(';')[3].strip())
    prov_reg['Districts'] =prov_reg['Districts'].apply(lambda x: x[:-9])
    prov_reg['Provinces'] = dataa.iloc[0:,0].apply(lambda x: x.split(';')[4])
    dstrct_prov_data = prov_reg.merge(nepal_reg, how='outer', on=['Districts'])
    dstrct_prov_data['Total Cases'] = pd.to_numeric(dstrct_prov_data['Total Cases']).fillna(0).astype('int')
    dstrct_prov_data['Deaths'] = pd.to_numeric(dstrct_prov_data['Deaths']).fillna(0).astype('int')
    dstrct_prov_data['Recovered'] = pd.to_numeric(dstrct_prov_data['Recovered']).fillna(0).astype('int')
    dstrct_prov_data['Active Cases'] = dstrct_prov_data['Total Cases'] - dstrct_prov_data['Deaths']-dstrct_prov_data['Recovered']
    district_data = dstrct_prov_data.loc[:,['Districts','Total Cases','Active Cases', 'Recovered','Deaths']]
    district_data = district_data.sort_values(by='Total Cases',ascending=False).reset_index(drop=True)
    district_data.index =  district_data.index+1
    province_data = dstrct_prov_data.groupby('Provinces').sum().reset_index()
    province_data =province_data.loc[:,['Provinces','Total Cases','Active Cases', 'Recovered','Deaths']]
    province_data = province_data.sort_values(by='Total Cases', ascending=False).reset_index(drop=True)
    province_data.index = province_data.index+1
    return district_data, province_data

nep_dist_data, nep_prov_data = obtain_nepal_dstrct_data()
display(nep_dist_data)
nep_dist_data.to_csv('district_covid_nepal.csv')
display(nep_prov_data)
nep_prov_data.to_csv('prov_covid_nepal.csv')
```


