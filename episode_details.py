# Modules
from episode_details_functions import *
import pandas as pd

# Get list of links to all episodes
list_of_episodes = []
episodeDetails = []

getLinksForEpisodes(list_of_episodes)
for individual_link in list_of_episodes:
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