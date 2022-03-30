from lxml import html
from bs4 import BeautifulSoup
import requests

def parse (name):

    item_name = []
    sum = 0
    avg = 0
    denom = 1
    minPrice = 99999

    if (name != ""):

        ebayUrl = 'https://www.ebay.com/sch/i.html?_nkw={0}&_sacat=0&rt=nc&LH_BIN=1'.format(name)
        r= requests.get(ebayUrl)
        data=r.text
        soup=BeautifulSoup(data, features="lxml")

        listings = soup.find_all('li', attrs={'class': 's-item'})

        for listing in listings:
            prod_name=" "
            prod_price = " "
            for name in listing.find_all('h3', attrs={'class':"s-item__title"}):
                if(str(name.find(text=True, recursive=False))!="None"):
                    prod_name=str(name.find(text=True, recursive=False))
                    item_name.append(prod_name)

            if(prod_name!=" "):
                price = listing.find('span', attrs={'class':"s-item__price"})
                prod_price = str(price.find(text=True, recursive=False))

                #print(prod_price)
                if (prod_price != "None"):
                    prod_price = prod_price.replace('$', '')
                    prod_price = prod_price.replace(',', '')
                    floatPrice = float(prod_price)

                    if (avg == 0):
                        avg = floatPrice
                    else:
                        avg = (avg * (denom-1) + floatPrice)/denom
                        denom += 1
                        if (minPrice > floatPrice and floatPrice > 0.8 * avg and denom > 5):                            
                            minPrice = floatPrice
                            if(minPrice > avg):
                                minPrice = avg
                            # print("min price: " + str(minPrice))


    return avg
