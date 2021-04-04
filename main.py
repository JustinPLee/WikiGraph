"""Description of this file

Justin Lee
"""

import re
import json
import time
import math
import random

import requests
from bs4 import BeautifulSoup


BLACKLIST = [
    'Special:',
    'Watchlist_Articles',
    'Category:',
    'Talk:',
    'Help:',
    'Wikipedia:',
    'File:',
    '.svg',
    '.jpg',
    '.png',
    'Portal:',
    'Main_Page',
]
DUPLICATE_LINKS = False # allows/removes duplicate links in 1 page
REMOVE_SELF_MENTION = True # if true, removes links that exist within itself
WIKI_GRAPH = {}
NUM_RECURSIVE_SEARCH_CALLS = 0
START = time.time()


def fetch_all_url(starter_name, max_urls=-1, ratio=1):
    """Fetches all wikipedia urls in a soup object
    """
    assert max_urls != -1 or ratio != 1, f'cannot set both max urls and ratio: max_urls={max_urls}, ratio={ratio}'
    assert ratio >= 0 and ratio <= 1, f'ratio must be between 0 and 1: ratio={ratio}'

    vgm_url = 'https://en.wikipedia.org/wiki/' + starter_name
    html_text = requests.get(vgm_url).text
    m_soup = BeautifulSoup(html_text, 'html.parser')
    links = []
    links_dict = {}
    count = 0

    for link in m_soup.find_all('a'):
        valid = True
        m_link = link.get('href')
        if m_link and m_link.startswith('/wiki/'): #checks if m_link is not None
            m_link_name = m_link.replace('/wiki/', '')
            for b in BLACKLIST:
                if b in m_link_name:
                    valid = False
                    break
            if valid:
                if not DUPLICATE_LINKS and m_link_name in links_dict:
                    pass
                else:
                    if REMOVE_SELF_MENTION and starter_name == m_link_name:
                        pass
                    else:
                        if count == max_urls:
                            return links
                        links.append(m_link_name)
                        links_dict[m_link_name] = b'1'
                        count += 1
    k = int(len(links) * ratio)
    indicies = random.sample(range(len(links)), k)
    links = [links[i] for i in indicies]
    return links

def recursive_search(link, depth, max_calls):
    """
    finds links in a wikipedia article, recursively searches each link's children up to depth number of times
    function stops if 

    link (str): wikipedia subject. ex: 'Discord'
    depth(int): 
    max_calls(int): sets max number of links to search, default value searches all links
    """
    #
    if depth == 0:
        return True

    global NUM_RECURSIVE_SEARCH_CALLS
    NUM_RECURSIVE_SEARCH_CALLS += 1
    if NUM_RECURSIVE_SEARCH_CALLS % 10 == 0:
        print('Processed {:.0f} links in {:.2f} sec from start'.format(NUM_RECURSIVE_SEARCH_CALLS, time.time()-START))

    if NUM_RECURSIVE_SEARCH_CALLS == max_calls:
        return False

    link_name = link.split('/')[-1]
    links = fetch_all_url(link, ratio=0.5)
    if link_name not in WIKI_GRAPH:
        WIKI_GRAPH[link_name] = { 'edges': links, 'size': 1}
        WIKI_GRAPH[link_name].setdefault('depth', [])
        WIKI_GRAPH[link_name]['depth'].append(depth)
    else: 
        WIKI_GRAPH[link_name]['size'] += 1
        WIKI_GRAPH[link_name]['depth'].append(depth)

    for a_link in links:
        if not recursive_search(a_link, depth - 1, max_calls):
            return False

    return True

def main(starter_name, depth=1, max_calls=-1):    
    # can make this user input link later

    # links = fetch_all_url(soup)
    return recursive_search(starter_name, depth, max_calls)


if __name__ == '__main__':
    starter_name = 'Discord'
    depth = 3

    if not main(starter_name=starter_name, depth=depth):
        print('didnt process all links. stopped at _ links')
    # print(json.dumps(WIKI_GRAPH, indent=4, sort_keys=True))
    with open('data.json', 'w') as f:
        json.dump(WIKI_GRAPH, f)