# Import Dependencies 
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Function for Scrape All
def scrape_all():

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome',**executable_path, headless=True)

    # Set news title and paragraph variables 
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts":mars_facts(),
        "hemispheres": mars_hemi(browser),
        "last_modified":dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data 

# Function for Mars News
def mars_news(browser):

    # Visit the Mars NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Parse the HTML
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Scrape article title
        slide_elem.find('div',class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div',class_='content_title').get_text()

        # # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title,news_paragraph


# ### Featured Images

# Function for Featured Image
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url 
        img_url_rel = img_soup.find('img',class_='fancybox-image').get('src')
    except AttributeError():
        return None

    # Use the base URL to create an absolute URL 
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# Function for Mars Facts
def mars_facts():

    # Add try/except for error handling
    try:
        
        # Scrape entire table with Pandas
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index 
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace = True)

    # convert our DataFrame back into HTML-ready code
    return df.to_html()


 # ### Hemispheres
# Function for Mars Hemispheres
def mars_hemi(browser):

    # Set up Splinter x2
    #executable_path = {'executable_path': ChromeDriverManager().install()}
    #browser = Browser('chrome',**executable_path, headless=False)

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse the HTML
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    # HTML tag that holds all image urls and titles
    hemi_items = hemi_soup.find_all('div', class_ = 'item')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Loop through tags
    for x in hemi_items:
        # Create an empty dictionary 
        hemispheres = {}
        
        # Find image url
        main_url = x.find('a', class_='itemLink')['href']    
        browser.visit(url + main_url)
        main_url = browser.html
        image_soup = soup(main_url,'html.parser')
        hemi_url = url + image_soup('img', class_='wide-image')[0]['src']

        
        # Find title
        hemi_title = x.find('h3').text
        
        # Store in dictionary 
        hemispheres['img_url'] = hemi_url
        hemispheres['title'] = hemi_title
        
        # Add to list
        hemisphere_image_urls.append(hemispheres)

    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape_all())