import requests
from bs4 import BeautifulSoup

def get_soup(url):
    try:
        page=requests.get(url)
        if page.status_code == 200:
            print('Connected to the server Successfully')
            return BeautifulSoup(page.text,'html.parser')
        else:
            print('Failed',page.status_code)
    except Exception as e:
        print(e)

def extract_data(soup):
    containers = soup.find_all("div",attrs={"class":"item-container"})
    size = len(containers)
    result =[]
    for item in containers:
        try:
            title = item.find('div',attrs={'class':'item-info'}).find('a',attrs={"class":"item-title"}).text
        except Exception as e:
            #print('title',e)
            title=" "
        try:
            price = item.find('div',attrs={'class':'item-action'}).find('li',attrs={"class":"price-current"}).text.strip().split()[1]
        except Exception as e:
            #print('price',e)
            price=0
        try:
            bachat = item.find(('div'),attrs={"class":'item-action'}).find('li',attrs={"class":'price-save'}).text.strip().split()[1]
        except Exception as e:
            #print('save',e)
            bachat=0
        result.append({
            'title':title,
            'price':price,
            'bachat':bachat,
        })
    return result

def get_next(last_pos):
    return last_pos+1

import pandas as pd
def save(datadict,path):
    data=pd.DataFrame(datadict)
    data.to_csv(path)
    return data


if __name__ == "__main__":
    query = "lenovo"
    page=1
    url=f'https://www.newegg.com/global/in-en/p/pl?d={query}&Page={page}'

    start_page = 0
    product_list = []
    while True:
        print('url',url)
        soup = get_soup(url)
        itemlist = extract_data(soup)
        if itemlist:
            product_list.extend(itemlist)
        print('total items',len(product_list))
        page = get_next(page)
        if page>1:
            url = f'https://www.newegg.com/global/in-en/p/pl?d={query}&Page={page}'
            start_page +=1
        else:
            print('finished')
            break
        if start_page >=5:
            break
    save(product_list,'laptops_1_oct_2019.csv')