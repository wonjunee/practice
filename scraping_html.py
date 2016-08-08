""" 
This is a simple example script for extracting data
from a scpecified html (indeed website).
The script is from 
	docs.python-guide.org/en/latest/scenarios/scrape/
"""

from lxml import html

# importing requests library to retrieve the web page
import requests

# search the words
search = "python+entry"
page = requests.get("http://www.indeed.com/jobs?q={}&l=".format(search))

# tree contains the whole HTML file with a nice tree structure
tree = html.fromstring(page.content)

# import BeautifulSoup to parse the data
from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(page.content)

# print title of the html
print soup.html.head.title

# print title only
print soup.html.head.title.string

# clean the html text
def clean_title(line):
	st = ""
	start = 0
	for i in range(len(line)):
		if line[i] == ">":
			start = i+1
		elif line[i] == "<":
			st += line[start:i]
	return st

jobtitle = soup.findAll("h2", {"class" : "jobtitle"})

print "\nList of jobs"
for i in jobtitle:
	print "\t{}".format(clean_title(str(i.a)))
