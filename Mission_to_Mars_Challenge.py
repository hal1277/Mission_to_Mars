#!/usr/bin/env python
# coding: utf-8




# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd





executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)





# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)





html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')





slide_elem.find('div', class_='content_title')





# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title





# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images




# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)





# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()





# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')





# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel





# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url





df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df





df.to_html()








# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles





#Use brower to visit the URL
url = 'https://marshemispheres.com'
browser.visit(url)

#Create a list to hold the images and titles
hemisphere_image_urls = []

#Get a list of all the hemisphere photos/titles
URL_links = browser.find_by_tag('h3')

for x in range(4):    
    hemispheres = {}
    browser.find_by_tag('h3')[x].click()
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')

    
    
    try:
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        url_element_rel = hemisphere_soup.find('img', class_='wide-image').get('src')
        url_element = f'https://marshemispheres.com/{url_element_rel}'
    except AttributeError:
        title_element = None
        url_element = None
        pass
    hemispheres = {
        "img_url":url_element,
        "title":title_element
    }

    
    
    hemisphere_image_urls.append(hemispheres)
    browser.back()
    


hemisphere_image_urls       
    





browser.quit()







