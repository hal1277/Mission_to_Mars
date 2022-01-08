#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    
       # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }
    
     # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')


        slide_elem.find('div', class_='content_title')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except:
        return None, None
    
    return news_title, news_p


# ### Featured Images

def featured_image(browser):
    
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try: 
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None


    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    
    return img_url

def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    return df.to_html()


def hemispheres(browser):
    url = 'https://marshemispheres.com'
    browser.visit(url)
    hemisphere_image_urls = []
    URL_links = browser.find_by_tag('h3')

    for x in range(4):    
        hemispheres = {}
        browser.find_by_tag('h3')[x].click()
        html = browser.html
        hemisphere_soup = soup(html, 'html.parser')
        hemisphere_img_url_rel = hemisphere_soup.find('img', class_='wide-image').get('src')
        hemisphere_img_url = f'https://marshemispheres.com/{hemisphere_img_url_rel}'
        hemisphere_image_title = browser.find_by_tag("h2.title").text
    
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
    return hemisphere_image_urls

   

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
    







