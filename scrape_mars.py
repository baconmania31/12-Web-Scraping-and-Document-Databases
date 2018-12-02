from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

def scrape():
   #news
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find('div', class_="image_and_description_container")
    news_title = results.find('img', class_='img-lazy')['alt']
    news_p = results.find('div', class_="rollover_description_inner").get_text(strip=True)
    
  #image  
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('section', class_="centered_text clearfix main_feature primary_media_feature single")
    details_url = 'https://www.jpl.nasa.gov' + results.a['data-link']
    browser.visit(details_url)
    details_html = browser.html
    detSoup = BeautifulSoup(details_html, 'html.parser')
    featured_image_url = 'https://www.jpl.nasa.gov' + detSoup.find('img', class_="main_image")['src']
    
    #twitter weather
    url = 'https://twitter.com/marswxreport?lang=en)'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mars_weather = soup.find('div', {"class": "tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet ", "data-mentions" : ""}).find('p', class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text(strip = True)
    
    #table
    url = "http://space-facts.com/mars/"
    table = pd.read_html(url)
    marsDF = table[0]
    marsDF.columns = ['Facts','Value']
    marsDF['Facts'] = marsDF['Facts'].replace(to_replace = ' ', value = '_', regex = True).replace(to_replace = ':', value = '', regex = True)
    mars_dict = marsDF.set_index('Facts').to_dict(orient = 'dict')
    
    # hemisphere
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    hemisphere_dict = []
    results = soup.find_all('a', class_="itemLink product-item")
    for result in results:
        trg_url = 'https://astrogeology.usgs.gov' + result['href']
        trg_resp = requests.get(trg_url)
        trgSoup = BeautifulSoup(trg_resp.text, 'html.parser')
        image_url = 'https://astrogeology.usgs.gov' + trgSoup.find('img',class_="wide-image")['src']
        hemisphere_dict.append({"title": result.find('h3').get_text(strip = True).replace(" ","_") , "image_url": image_url})
    
    
    
    
    mars_data = {"news_title": news_title, "news_p": news_p, "hemisphere_dict" : hemisphere_dict, "featured_image_url": featured_image_url, "mars_weather": mars_weather, "mars_dict": mars_dict}
    
    return mars_data

    

    