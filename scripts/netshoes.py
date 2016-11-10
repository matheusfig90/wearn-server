# Dependencies
import urllib2

from bs4 import BeautifulSoup
from wearn import app
from wearn.models.wear import Wear

# Set URLs to scrapping
urls = [
    # Men
    'http://www.netshoes.com.br/camisas-polo/masculino?mi=hm_ger_mntop_H-ROU-camisas-polo&psn=Menu_Top&fc=menu',
    'http://www.netshoes.com.br/camisetas/masculino?mi=hm_ger_mntop_H-ROU-camisetas&psn=Menu_Top&fc=menu',


    # Women
    'http://www.netshoes.com.br/camisas-polo/feminino?mi=hm_ger_mntop_M-ROU-camisas-polo&psn=Menu_Top&fc=menu',
    'http://www.netshoes.com.br/camisetas/feminino?mi=hm_ger_mntop_M-ROU-camisetas&psn=Menu_Top&fc=menu'
]

# Each in all urls
for url in urls:
    currentUrl = url

    while True:
        # Load page
        soup = BeautifulSoup(urllib2.urlopen(currentUrl))

        # Get all images
        items = soup.select('.product-list-item')
        if len(items) == 0:
            break

        # Get all images
        for item in items:
            try:
                # Get image
                image_link = item.select('.product-img')[0].select('img')[0].attrs.get('data-src')
                image_link = 'http:' + image_link.split('?')[0].replace('detalhe1.jpg', 'zoom1.jpg')

                Wear.save({
                    'name': item.select('.name')[0].get_text(),
                    'image': image_link,
                    'price': 0.00,
                    'link': ('http://www.netshoes.com.br' + item.select('a')[0].attrs.get('href')),
                })
            except:
                pass

        if len(soup.select('.pagination-link.is-next')) == 0:
            break

        currentUrl = 'http://www.netshoes.com.br' + soup.select('.pagination-link.is-next')[0].attrs.get('href')



