# Modules
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Get list of links to all episodes
list_of_episodes = []
episodeDetails = []

def getLinksForEpisodes():
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
            list_of_episodes.append(website_string + link['href'])
            
        #print("In page: " + str(i) + ", we found: " + str(len(episodelinks)) + " episodes.")
        
    if str(len(list_of_episodes)) != str(total_available_episodes):
        print("Overall, we found " + str(len(list_of_episodes)) + " episodes")
        print("There are " + str(total_available_episodes) + " episodes available")
    else:
        print("Downloading list of episodes was good.")

def extractDetailsForAnEpisode(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # End of URL
    episode_code = link.split('/')[len(link.split('/'))-1]
    
    # Title
    title = soup.find("span", {"class": "sc-c-marquee__title-1"}).text
    
    # Release Date
    date = soup.find("div", {"class": "gel-pica gs-u-display-inline@s sc-c-episode__metadata__data"}).text[13:]
    
    # Body Text
    # We need to click the read-more button
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(link)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.sc-c-synopsis__button.sc-o-button.gel-brevier-bold.gs-u-mt"))).click()
    body = driver.find_element(By.CLASS_NAME, "gel-body-copy").text
    
    return [episode_code, title, date, body]

getLinksForEpisodes()
for individual_link in list_of_episodes[0:5]:
    individual_episode = extractDetailsForAnEpisode(individual_link)
    episodeDetails.append(
        {
            'Episode Code': individual_episode[0],
            'Title': individual_episode[1],
            'Release Date': individual_episode[2],
            'Body Text': individual_episode[3]
        }
    )

episodeDetails = pd.DataFrame(episodeDetails)
episodeDetails.to_pickle('episode_details.pkl')