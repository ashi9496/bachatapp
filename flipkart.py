import requests
from bs4 import BeautifulSoup
import pandas as pd

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

def extract_data(page_soup):
    containers = page_soup.findAll("div",attrs={"class":"IIdQZO _1SSAGr"})
    
    #size = len(containers)
    mylist=[]
    for item  in containers:
        try:
            title = item.find('div',attrs={'class':'_2LFGJH'}).find('a',attrs={'class','_2mylT6'}).text#.attrs.get('title')
        except Exception as e:
            #print('name',e)
            title=""
        try:
            link = item.find('div',attrs={'class':'_2LFGJH'}).find('a',attrs={'class','_2mylT6'}).attrs.get('href') #.attrs.get('title')
        except Exception as e:
            #print('name',e)
            link=""
        try:
            current_price = item.find('div',attrs={'class':'_2LFGJH'}).find('div',attrs={'class','_1vC4OE'}).text
        except Exception as e:
            #print('price',e)
            current_price =0
        try:
            original_price = item.find('div',attrs={'class':'_2LFGJH'}).find('div',attrs={'class','_3auQ3N'}).text
        except Exception as e:
            #print('price',e)
            original_price =0
        try:
            bachat = item.find('div',attrs={'class':'_2LFGJH'}).find('div',attrs={'class','VGWI6T'}).text
        except Exception as e:
            #print('bachat',e)
            bachat = 0
        try:
            name = item.find('div',attrs={'class':'_2LFGJH'}).find('div',attrs={'class':'_2B_pmu'}).text
        except Exception as e:
            #print('name',e)
            name= ''
        
        mylist.append({
            'name':name,
            'title':title,
            'current_price':current_price,
            'original_price':original_price,
            'bachat':bachat,
            'link':link,
        })
    return mylist


def get_next(page_soup):
    next_page =page_soup.find_all('a',attrs={'class':'_3fVaIS'}) 
    if next_page:
        if len(next_page)>1:
            next_page=next_page[1]
        else:
            next_page = next_page[0]
        base = "https://www.flipkart.com"
        next_link = next_page.attrs.get('href')
        #print(next_link)
        
        return base+next_link

def save(datadict,path):
    data=pd.DataFrame(datadict)
    data.to_csv(path)
    return data

if __name__ == "__main__":
    query = 'shirts'
    url=f"https://www.flipkart.com/search?q={query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

    start_page = 0
    product_list = []
    while True:
        #print('url',url)
        soup = get_soup(url)
        itemlist = extract_data(soup)
        if itemlist:
            product_list.extend(itemlist)
        print('total items',len(product_list))
        link = get_next(soup)
        if link:
            url = link
            start_page +=1
        else:
            print('finished')
            break
        if start_page >=4:
            break
    print(save(product_list,'shirts.csv'))

