import requests
from bs4 import BeautifulSoup

# This is a code snippet from a tutorial on realpython.com
# With a additional user interface

print('This programme searched monster.com for jobs')
# Ask user for input
print('What title/keywords are you searching for (search box in monster)?')
title = input()
print('Where do you want to work?')
where = input()
print('What keyword has to be in the job title (job title form the searched list)?')
keyword = input()

#For searching we need strings with dashes between words
title_words = title.split()
search_title = ''
for i in range(0, len(title_words)-1):
    search_title += title_words[i] + '-'
search_title += title_words[len(title_words)-1]

where = where.split()
search_where = ''
for i in range(0, len(where)-1):
    search_where += where[i] + '-'
search_where += where[len(where)-1]

URL = 'https://www.monster.com/jobs/search/?q=' + search_title + '&where=' + search_where
#URL = 'https://www.monster.com/jobs/search/?q=Software-Developer&where=Australia'

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='ResultsContainer')
job_elems = results.find_all('section', class_='card-content')

for job_elem in job_elems:
    # Each job_elem is a new BeautifulSoup object
    # You can use the same methods on it as you did before
    title_elem = job_elem.find('h2', class_='title')
    company_elem = job_elem.find('div', class_='company')
    location_elem= job_elem.find('div', class_='location')

    if title_elem != None:
        print(title_elem.text.strip())
    if company_elem != None:
        print(company_elem.text.strip())
    if location_elem != None:
        print(location_elem.text.strip())
        print()

test_jobs = results.find_all('h2', string=lambda text: keyword.lower() in text.lower())

print('List of ' + title + ' jobs:')
for test_job in test_jobs:
    link = test_job.find('a')['href']
    print(test_job.text.strip())
    print('You can apply here:')
    print(link)
    print()