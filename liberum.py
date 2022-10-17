import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt

navegador = webdriver.Chrome()
navegador.maximize_window()
navegador.get('http://www.liberumratings.com.br/pt/pub-ratings.php')
navegador.implicitly_wait(5)
id_liberum = []
date = []
institution = []
rating_long = []

for page in range (1,11): 
    for index in range(1, 11):
        navegador.implicitly_wait(3)
        data = f'//*[@id="tbl-contact"]/tbody/tr[{index}]/td[1]'
        insituição = f'//*[@id="tbl-contact"]/tbody/tr[{index}]/td[3]'
        longo_prazo = f'//*[@id="tbl-contact"]/tbody/tr[{index + 1}]/td/ul/li[1]/span[2]'
        botao = f'//*[@id="tbl-contact"]/tbody/tr[{index}]/td[1]'

        date.append(navegador.find_element('xpath', data).text)
        navegador.implicitly_wait(3)
        institution.append(navegador.find_element(By.XPATH, insituição).text[19:])
        id_liberum.append(navegador.find_element(By.XPATH,
                                f'//*[@id="tbl-contact"]/tbody/tr[{index}]/td[2]').text)
    try: 
        navegador.find_element(By.XPATH, '//*[@id="tbl-contact_next"]').click()
        sleep(3)
    except StaleElementReferenceException:
        break

for identicator in id_liberum:
    try:
        navegador.find_element(By.XPATH, 
                                    '//*[@id="tbl-contact"]/thead/tr/th[2]/input').send_keys(identicator)
        navegador.implicitly_wait(2)
        navegador.find_element(By.XPATH, 
                                    '//*[@id="tbl-contact"]/thead/tr/th[2]/input').send_keys(Keys.ENTER)
        sleep(3)
        navegador.find_element(By.XPATH, '//*[@id="tbl-contact"]/tbody/tr[1]/td[1]').click()
        sleep(3)
        rating = navegador.find_element(By.XPATH, 
                                    '//*[@id="tbl-contact"]/tbody/tr[2]/td/ul/li[1]/span[2]').text
    except NoSuchElementException or StaleElementReferenceException:
        navegador.implicitly_wait(2)
        navegador.find_element(By.XPATH, '//*[@id="tbl-contact"]/tbody/tr[1]/td[1]').click()
        sleep(3)
        rating = navegador.find_element(By.XPATH, 
                                    '//*[@id="tbl-contact"]/tbody/tr[2]/td/ul/li[1]/span[2]').text
    if len(rating.split()) >= 15:
        rating = navegador.find_element(By.XPATH, '//*[@id="tbl-contact"]/tbody/tr[1]/td[7]').text
        rating_long.append(rating.split()[2])
    else:
        if rating.split()[2] == 'Rating:':
            rating = navegador.find_element(By.XPATH, '//*[@id="tbl-contact"]/tbody/tr[2]/td/ul/li[2]').text
            rating_long.append(rating.split()[3])
        elif rating.split()[2] == 'Rating':
            rating = navegador.find_element(By.XPATH, '//*[@id="tbl-contact"]/tbody/tr[1]/td[7]').text
            rating_long.append(rating.split()[2])
        else:
            rating_long.append(rating.split()[2])
    navegador.find_element(By.XPATH, '//*[@id="tbl-contact"]/thead/tr/th[2]/input').clear()

tuple_list = list(zip(date, institution, rating_long))
df = pd.DataFrame(tuple_list, columns=['Data', 'Instituição', 'Rating de Longo Prazo'])
indice = df.groupby(['Rating de Longo Prazo']).size().to_dict()
percent = pd.DataFrame([name for name in indice.keys()], columns=['Rating de Longo Prazo'])
percent['Percentual'] = [(tax/len(rating_long))*100 for tax in indice.values()]
print(percent)
plt.bar(percent['Rating de Longo Prazo'], percent['Percentual'], color='red')
plt.xticks(percent['Rating de Longo Prazo'])
plt.ylabel('Percentual')
plt.show()