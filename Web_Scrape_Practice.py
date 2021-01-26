# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:11:01 2021

@author: dboyd020
"""
#inserting to get riud of ssl error
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


#this shows how to get the html of the website page
from requests import get
from bs4 import BeautifulSoup
url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'
response = get(url, verify=False)
print(response.text[:500])


html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)


#in this case gets the 50 containers for each movie on the page i.e. 50 movies
movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')
print(type(movie_containers))
print(len(movie_containers))


first_movie = movie_containers[0]
first_movie
first_movie.div
first_movie.a
first_movie.h3
first_movie.h3.a
first_name = first_movie.h3.a.text
print(first_name)


first_movie.strong
first_imdb = float(first_movie.strong.text)
print(first_imdb)


first_year = first_movie.h3.find('span', class_ = 'lister-item-year text-muted unbold')
print(first_year)
first_year = first_year.text
print(first_year)

#gets number of votes
first_votes = first_movie.find('span', attrs = {'name':'nv'})
first_votes

#finds the metascore 
first_mscore = first_movie.find('span', class_ = 'metascore favorable')
first_mscore = int(first_mscore.text)
print(first_mscore)

#finds number of votes
first_votes['data-value']
first_votes = int(first_votes['data-value'])
print(first_votes)

#finds container with no metascore
eighteen_movie_mscore = movie_containers[18].find('div', class_ = 'ratings-metascore')
type(eighteen_movie_mscore)


#lists to store scraped data
names = []
years = []
imdb_ratings = []
metascores = []
votes = []


# Extract data from individual movie container
for container in movie_containers:
# If the movie has Metascore, then extract:
    if container.find('div', class_ = 'ratings-metascore') is not None:
# The name
        name = container.h3.a.text
        names.append(name)
# The year
        year = container.h3.find('span', class_ = 'lister-item-year').text
        years.append(year)
# The IMDB rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)
# The Metascore
        m_score = container.find('span', class_ = 'metascore').text
        metascores.append(int(m_score))
# The number of votes
        vote = container.find('span', attrs = {'name':'nv'})['data-value']
        votes.append(int(vote))
        
        
        
#using pandas to produce dataframe
import pandas as pd
test_df = pd.DataFrame({'movie': names,
'year': years,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes
})
print(test_df.info())
test_df

#using this to avoid header error
headers = {"Accept-Language": "en-US, en;q=0.5"}

'''
SCRAPING FROM MULTIPLE PAGES
'''
try:
    pages = [str(i) for i in range(1,5)]
    years_url = [str(i) for i in range(2000,2002)]
    
    
    #from time import sleep
    from random import randint
    from time import sleep
    
    from time import time
    timestart_time = time()
    requests = 0
    for _ in range(72):
    # A request would go here
        requests += 1
        sleep(randint(1,3))
        elapsed_time = time() - timestart_time
        print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        
        
    #clears output with most recent one to keep the code looking tidy
    from IPython.core.display import clear_output
    start_time = time()
    requests = 0 
    
    for _ in range(5):
    # A request would go here
        requests += 1
        sleep(randint(1,3))
        current_time = time()
        elapsed_time = current_time - start_time
        print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)
        
    
    '''
    from warnings import warn
    warn("Warning Simulation")
    '''
    
    # Redeclaring the lists to store data in
    names = []
    years = []
    imdb_ratings = []
    metascores = []
    votes = []
    
    # Preparing the monitoring of the loop
    start_time = time()
    requests = 0
    
    # For every year in the interval 2000-2017
    for year_url in years_url:
    
        # For every page in the interval 1-4
        for page in pages:
    
            # Make a get request
            #using this to avoid header error
            headers = {"Accept-Language": "en-US, en;q=0.5"}
            response = get('http://www.imdb.com/search/title?release_date=' + year_url +
            '&sort=num_votes,desc&page=' + page, headers = headers)
    
            # Pause the loop
            sleep(randint(8,15))
    
            # Monitor the requests
            requests += 1
            elapsed_time = time() - start_time
            print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
            clear_output(wait = True)
    
            # Throw a warning for non-200 status codes
            #if response.status_code != 200:
             #   warn('Request: {}; Status code: {}'.format(requests, response.status_code))
    
            # Break the loop if the number of requests is greater than expected
            #if requests > 72:
             #   warn('Number of requests was greater than expected.')
              #  break
    
            # Parse the content of the request with BeautifulSoup
            page_html = BeautifulSoup(response.text, 'html.parser')
    
            # Select all the 50 movie containers from a single page
            mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
    
            # For every movie of these 50
            for container in mv_containers:
                # If the movie has a Metascore, then:
                if container.find('div', class_ = 'ratings-metascore') is not None:
    
                    # Scrape the name
                    name = container.h3.a.text
                    names.append(name)
    
                    # Scrape the year
                    year = container.h3.find('span', class_ = 'lister-item-year').text
                    years.append(year)
    
                    # Scrape the IMDB rating
                    imdb = float(container.strong.text)
                    imdb_ratings.append(imdb)
    
                    # Scrape the Metascore
                    m_score = container.find('span', class_ = 'metascore').text
                    metascores.append(int(m_score))
    
                    # Scrape the number of votes
                    vote = container.find('span', attrs = {'name':'nv'})['data-value']
                    votes.append(int(vote))
                    
                    
                    

except:
    print('error')


#pandas dataframe 
movie_ratings = pd.DataFrame({'movie': names,
'year': years,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes
})
print(movie_ratings.info())
movie_ratings.head(10)
import os
os.chdir(r'####ENTER DIRECTORY#####')
f = open("IMDB.csv", "w")
f.truncate()
f.close()
movie_ratings.to_csv('IMDB.csv')




movie_ratings = movie_ratings[['movie', 'year', 'imdb', 'metascore', 'votes']]
movie_ratings.head()
