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

    container = page_soup.find_all("div",attrs={"class":"product-desc-rating"})
    #len(container)


    mylist = []
    for item in container:
        
        title = item.find("p",attrs={"class":"product-title"}).text#.find("span")

        #print(title)
        original_price = item.find("div",attrs={"class":"lfloat marR10"}).find("span",attrs={"class":"lfloat product-desc-price strike "}).text

        #print(original_price)
        discounted_price= item.find("div",attrs={"class":"lfloat marR10"}).find("span",attrs={"class":"lfloat product-price"}).text
        #print(discounted_price)
        try:
            bachat = item.find("div",attrs={"class":"product-discount"}).find('span').text.split()
            #print(bachat)
        except Exception as e:
            #print(bachat,e)
            #pass
            bachat=0
        #else:
        #    bachat=0
        #Get_rattings = item.find("div",attrs={"class":"rating-stars "}).text
        #print(Get_rattings)"""
        mylist.append({
            'title':title,
            "original_price":original_price,
            "discounted_price":discounted_price,
            'bachat':bachat,

            })
    return mylist

def get_section(last_section):
    
    last_section =2*10
        
    return last_section


def save_csv(datadict,path):
    data=pd.DataFrame(datadict)
    data.to_csv(path)
    return data

def save_sql(datadict, db):
    data=pd.DataFrame(datadict)
    data.to_sql('snapdeal',db.engine,index=False)
    return data



if __name__ == "__main__":
    query = 'saree'
    section=0
    url=f"https://www.snapdeal.com/acors/json/product/get/search/0/{section}/20?q=&sort=rlvncy&brandPageUrl=&keyword={query}&searchState=k3=true|k5=0|k6=0|k7=/yeUxAAIQAAAAAAAAAAAAAAAAAAAAABA|k8=0&pincode=&vc=&webpageName=searchResult&campaignId=&brandName=&isMC=false&clickSrc=go_header&showAds=true&cartId=&page=srp"
        
    start_page = 0
    product_list = []
    while True:
        #print('url',url)
        soup = get_soup(url)
        itemlist = extract_data(soup)
        if itemlist:
            product_list.extend(itemlist)
        #print('total items',len(product_list))
        section = get_section(soup)
        if section>1:
            url = next_section =f"https://www.snapdeal.com/acors/json/product/get/search/0/{section}/20?q=&sort=rlvncy&brandPageUrl=&keyword={query}&searchState=k3=true|k5=0|k6=0|k7=/yeUxAAIQAAAAAAAAAAAAAAAAAAAAABA|k8=0&pincode=&vc=&webpageName=searchResult&campaignId=&brandName=&isMC=false&clickSrc=go_header&showAds=true&cartId=&page=srp"
        
            start_page +=1
        else:
            print('finished')
            break
        if len(product_list) >=100:
            break
    save_csv(product_list,'productdeatail.csv')