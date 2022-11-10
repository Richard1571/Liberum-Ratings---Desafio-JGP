import requests 
import urllib
import pandas as pd
import re
import matplotlib.pyplot as plt

check_fidc = {'start' : 0,
              'length': 100}
encode_ = urllib.parse.urlencode(check_fidc)
link = 'http://www.liberumratings.com.br/pt/src/ratings/server_processing.php?' + encode_
page = requests.get(link, verify=False).text
df = pd.read_json(page)['data'].apply(pd.Series)
newdata = pd.DataFrame([the_index[23:] for the_index in df[2]], columns=['Instituição'])
newdata.insert(0,'Data', df[0].to_list())
newdata.insert(2, 'Rating de Longo Prazo', [re.compile(r'<br>').sub('', index.split()[2]) for index in df[6]])
indice = newdata.groupby(['Rating de Longo Prazo']).size().to_dict()
percent = pd.DataFrame([name for name in indice.keys()], columns=['Rating de Longo Prazo'])
percent['Percentual'] = [(tax/check_fidc['length'])*100 for tax in indice.values()]
plt.bar(percent['Rating de Longo Prazo'], percent['Percentual'], color='red')
plt.xticks(percent['Rating de Longo Prazo'])
plt.ylabel('Percentual')
plt.show()
