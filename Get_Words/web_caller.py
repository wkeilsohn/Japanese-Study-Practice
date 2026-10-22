# William Keilsohn
# August 10th 2026

# Import Packages
import requests
from bs4 import BeautifulSoup as bs4
from random import randint 
from time import sleep

# Define Functions
def getPage(path_url):
    resp = requests.get(path_url)
    return resp.text
    
def callPage(link):
    sleep(randint(1,5))
    return getPage(link)