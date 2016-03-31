import requests
from bs4 import BeautifulSoup as BS 
from lxml import etree
import numpy as np 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


headers = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
	'Connection':'keep-alive',
	'Host':'cn-proxy.com',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
}

url = 'http://cn-proxy.com/archives/218'
s = requests.session()
res = s.get(url, headers = headers, verify = False)
soup = BS(res.content, 'lxml')
# tables = soup.find_all('table',{'class':'sortable'})
tds = soup.find_all('td')
proxy_list = []	
i = 0
temp1 = ''
temp2 = ''
for td in tds:
	if i % 6 == 0 and i != 0:
		temp1 = td.text
		# print td
	elif i % 6 == 1 and i != 1:
		temp2 = td.text
		# print td
	while temp1 and temp2:
		proxy = 'http://' + temp1 + ':' + temp2 + '/'
		# print proxy
		proxy_list.append(proxy)
		temp1 = ''
		temp2 = ''
	i += 1
del proxy_list[50]
# print proxy_list
# print len(proxy_list)
useful_proxies = []
useful_proxy_sum = 0
useless_proxy_sum = 0
for proxy in proxy_list:
	test_url = 'https://www.google.com/'
	proxies = {"https":"",}
	proxies['https'] = proxy
	try:
		res = requests.get(test_url, proxies = proxies, verify = False)
		if res.status_code == 200:
			useful_proxy_sum += 1
			useful_proxies.append(proxy)
			print "Yeah! Useful proxy! Total useful proxies' num: " + str(useful_proxy_sum)
		else:
			continue
	except requests.exceptions.ConnectionError:
		useless_proxy_sum += 1
		print "Oops! Useless proxy! Total useless proxies' num: " + str(useless_proxy_sum)
	except TypeError:
		print "Something wrong, but don't worry."
		continue
proxies_np = np.array(useful_proxies)
np.save('proxies',proxies_np)



