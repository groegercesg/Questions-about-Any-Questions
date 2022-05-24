# Modules
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
logging.getLogger('WDM').setLevel(logging.NOTSET)

def getLinksForEpisodes(list):
    # Website for episodes
    website_string = "https://www.bbc.co.uk"
    all_episodes_link = "https://www.bbc.co.uk/sounds/brand/b006qgvj"
    page_sect = "?page="

    # Get max number of pages
    page = requests.get(all_episodes_link)
    soup = BeautifulSoup(page.content, "html.parser")
    next_pages = soup.find_all("a", {"sc-c-pagination-button__number gel-pica-bold sc-o-button sc-c-pagination-button gs-u-display-flex sc-o-button__text"})
    max_pages = next_pages[len(next_pages) - 1].find_all("span")[0].text

    # Total available
    total_available = soup.find("div", {"gel-minion sc-c-available-episodes"})
    total_available_episodes = total_available.text.split()[1][1:]

    for i in range(1, int(max_pages)+1):
        current_page = requests.get(all_episodes_link+page_sect+str(i))
        soup = BeautifulSoup(current_page.content, "html.parser")
        episodelinks = soup.find_all("a", {"class": "sc-c-playable-list-card__link sc-o-link sc-u-flex-grow"})

        for link in episodelinks:
            list.append(website_string + link['href'])
            
        #print("In page: " + str(i) + ", we found: " + str(len(episodelinks)) + " episodes.")
        
    if str(len(list)) != str(total_available_episodes):
        print("Overall, we found " + str(len(list)) + " episodes")
        print("There are " + str(total_available_episodes) + " episodes available")
    else:
        print("Downloading list of episodes was good.")

def extractDetailsForAnEpisode(link):
    print("Currently extracting: " + str(link)) 
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # End of URL
    episode_code = link.split('/')[len(link.split('/'))-1]
    
    # Title
    title = soup.find("span", {"class": "sc-c-marquee__title-1"}).text
    
    # Release Date
    date = soup.find("div", {"class": "gel-pica gs-u-display-inline@s sc-c-episode__metadata__data"}).text[13:]
    
    # Sometimes there isn't a read-more button, use soup to detect if there is a button
    # if there is use selenium to click and then grab the text
    # otherwise just use soup to get it
    if (soup.find("button", {"class": "sc-c-synopsis__button sc-o-button gel-brevier-bold gs-u-mt"})) is None:
        # There is no button, get the text simply
        body = soup.find("p", {"class": "gel-body-copy"}).text
    else:
        # Body Text
        # We need to click the read-more button
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        try:
            driver.set_page_load_timeout(10)
            driver.get(link)
            driver.get(link)
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.sc-c-synopsis__button.sc-o-button.gel-brevier-bold.gs-u-mt"))).click()
            body = driver.find_element(By.CLASS_NAME, "gel-body-copy").text
        except TimeoutException as ex:
            print("An error occurred during: " + str(link))
            print("The following Exception was thrown: " + str(ex))
            driver.close()
            exit()
        driver.close()
        
    return [episode_code, title, date, body]