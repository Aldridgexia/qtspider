import requests
import json
import numpy as np
from bs4 import BeautifulSoup as BS

def getcookies():
	headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0",
	"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"accept-encoding":"gzip, deflate, br",
	"accept-language":"zh-CN,zh;q=0.8,en;q=0.6",
	"origin":"https://www.quantnet.com",
	"referer":"https://www.quantnet.com/",
	"upgrade-insecure-requests":"1",
	"content-type":"application/x-www-form-urlencoded",
	}
	# login page url
	url = 'https://www.quantnet.com/login/login'
	# login data
	data = {
		'login':'',
		'password':'',
		'redirect':'https://www.quantnet.com/'
	}
	# enter username and password
	data['login'] = raw_input("Username:\n")
	data['password'] = raw_input("Password:\n")

	s = requests.session()
	res = s.post(url,headers = headers, data = data, verify = True)
	soup = BS(res.content,'lxml')
	flag = soup.find('strong','accountUsername')
	if flag:
		print 'Login successfully!'
	else:
		print 'Fail to login!'

	m_cookies = res.cookies
	return m_cookies
