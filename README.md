# Any Questions

A repository for some investigation and analysis into the long running, BBC Radio 4 topical discussion program: Any Questions.

## Research Questions

### Where has it been hosted from

To answer this question, from the data we need to extract where each Any Questions episode is coming from.
Using Spacy, the NLP package for Python, I tried to extract locations from the text. I wrote some code to do this, then audited the first 20 episodes to check it's effectiveness. Below is a table of the problems encountered:

| Index       | Description |
| ----------- | ----------- |
| 2 | **MISC** swallows **LOC** inside of it |
| 7 | **LOC** is detected as **PER** |
| 11 | **LOC** is not detected |
| 12 | **LOC** is not detected |
| 17 | No **LOC** detected |
| 18 | **MISC** swallows **LOC** inside of it |
| 19 | **LOC** is not detected |
| 20 | **LOC** is detected as **PER** |

As can be seen from the table above, of the first 20 records I audited my code's functioning on; 12 (or 60%) had perfect location information) and the other 8's information wasn't usable. Further complicating this matter is that there is no method of determining what the location should be, no ground truth, which makes this either a very manual task or a technically infeasible one.

#### NLP Notes

From the documentation for the Stanford Named Entity Recogniser (NER):

- **MISC** corresponds to miscellaneous entities, e.g., events, nationalities, products or works of art
- **LOC** corresponds to location names
- **PER** corresponds to person names
- **ORG** corresponds to organisations

### Who has hosted Any Questions?

### Who is the most frequent guest?


## File List

- ```downloader.py``` - Download an episode, might be used later
- ```episode_details.py``` - Get details to all episodes and save it as a .pkl file
- ```analysis.ipynb``` - File for all the analysis we need to perform, using our data collected
