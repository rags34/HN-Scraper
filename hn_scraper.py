import requests
from bs4 import BeautifulSoup
import pprint

# URLs for the first and second pages of Hacker News
url = "https://news.ycombinator.com/news"
url2 = "https://news.ycombinator.com/news?p=2"

# Fetching data from Hacker News pages
res = requests.get(url)
res2 = requests.get(url2)

# Parsing HTML content using BeautifulSoup
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

# Selecting post titles and subtext elements from both pages
links = soup.select('.titleline')
subtext = soup.select('.subtext')
links2 = soup2.select('.titleline')
subtext2 = soup2.select('.subtext')

# Merging the post titles and subtext from both pages
mega_links = links + links2
mega_subtext = subtext + subtext2

# Function to sort posts by votes
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

# Function to create a list of Hacker News posts meeting criteria
def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        # Extracting post title
        title = links[idx].getText()
        # Extracting post link
        href = links[idx].get('href', None)
        # Extracting votes for the post
        vote = subtext[idx].select('.score')
        if len(vote):
            # Converting votes to integer
            points = int(vote[0].getText().replace(' points', ''))
            # Filtering posts with more than 49 points
            if points > 49:
                # Appending post details to the list
                hn.append({'title': title, 'link': href, 'votes': points})
    # Sorting and returning posts by votes
    return sort_stories_by_votes(hn)

# Displaying top posts from Hacker News based on votes
pprint.pprint(create_custom_hn(mega_links, mega_subtext))
