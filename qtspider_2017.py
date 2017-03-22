# -*- coding: utf-8 -*-
import re
import time
import random
import requests
import pandas as pd 
from pandas import DataFrame, Series
from qtlogin import getcookies
# from qtlogin_local import getcookies
from bs4 import BeautifulSoup as BS

# generate headers
def gethdrs():
	headers = {
	    "User-Agent":'',
		"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"accept-encoding":"gzip, deflate, sdch",
		"accept-language":"zh-CN,zh;q=0.8,en;q=0.6",
		"referer":"https://www.quantnet.com/tracker/",
		"upgrade-insecure-requests":"1",
	}
	usr_agents = [
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0",
		"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
	]
	headers["User-Agent"] = usr_agents[random.randint(0,4)]
	return headers

# start actions
url = 'https://www.quantnet.com/tracker/'
cookies = getcookies()
s = requests.session()
page_soup = BS(s.get(url,cookies=cookies,verify=True).content, 'lxml')
max_page_num = int(page_soup.find('span','pageNavHeader').text.split()[-1])
# generate all urls
urls = ['https://www.quantnet.com/tracker/?page=' + str(i) for i in range(1,max_page_num+1)]

# function to parse single tracker's info, return a dict containing all useful info we need
def tracker_info(li):
    info_dict = {}
    info_dict['program_name'] = li.find('h3','title').text.strip().split(u'\n')[0]
    info_dict['program_type'] = li.find('h3','title').text.strip().split(u'\n')[1]
    info_dict['ugpa'] = li.find('div','listBlock ugpa').text.strip()
    info_dict['gre_q'] = li.find('div','listBlock GRE_Q').text.strip()
    info_dict['gre_v'] = li.find('div','listBlock GRE_V').text.strip()
    info_dict['gre_awa'] = li.find('div','listBlock GRE_AWA').text.strip()
    info_dict['submitted'] = li.find('div','listBlock submitted').text.strip()
    if len(info_dict['submitted']) > 15:
        submits = info_dict['submitted'].split(u'\n')
        info_dict['submitted'] = submits[0]
        info_dict['interview'] = submits[2][5:]
    result_block = li.find('div','listBlock result')
    info_dict['status'] = result_block.find('div','status').text.strip()
    if info_dict['status'] == 'Pending':
        days = result_block.find('div','secondRow').text.strip()
        info_dict['days_elapsed'] = int(re.findall(r'\d+',days)[0])
    else:
        days = result_block.find('div','secondRow').text.strip()
        info_dict['days_to_result'] = int(re.findall(r'\d+',days)[0])
        info_dict['status'] = info_dict['status'].split(u'\n')[0]
        if len(info_dict['status'].split(u'\n')) > 1:
            info_dict['result_date'] = info_dict['status'].split(u'\n')[1][1:-1]
    try:
        info_dict['note'] = li.find('div','applicationNote').text.strip().replace(u'\n',' | ')
    except AttributeError:
        info_dict['note'] = ''
    info_dict['will_join'] = li.find('div','listBlock active').text.strip()
    return info_dict

# store tracker info into a list
trackers = []

# loop through all urls
start = time.time()
for idx, url in enumerate(urls):
    print('Parsing page %i...' % (idx+1))
    soup = BS(s.get(url, headers=gethdrs(), cookies=cookies, verify=True).content, 'lxml')
    lis = soup.find_all('li','applicationListItem')
    for li in lis:
        trackers.append(tracker_info(li))
    print('Page %i successfully parsed! Trackers downloaded:%i' % (idx+1, len(trackers)))
    if idx % 7 == 0:
        nap = random.randint(1,5)
        time.sleep(nap)
        print('Intentional break for %is' % nap)
end = time.time()
print('Total parsing time: %f' % (end - start))

# store trackers into DataFrame
df_trackers = DataFrame(trackers)
print(df_trackers.head(5))
