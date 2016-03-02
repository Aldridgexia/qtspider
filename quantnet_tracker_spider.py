# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
from bs4 import BeautifulSoup
import numpy as np

#定义一个qtspider 的class
class qtspider: 

	def __init__(self):
		self.page_num = 1
		self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
		self.headers = {'User-Agent':self.user_agent}

	def getPage(self,page_num):
		try:
			url = 'https://www.quantnet.com/tracker/?page=' + str(page_num)
			request = urllib2.Request(url,headers=self.headers)
			response = urllib2.urlopen(request)
			content = response.read().decode('utf-8')
			tracker_soup = BeautifulSoup(content,'lxml')
			return tracker_soup
		except urllib2.URLError, e:
			if hasattr(e,'reason'):
				print u'连接失败，错误原因',e.reason
				return None

	def getPageContent(self,page_num):
		tracker_soup = self.getPage(page_num)

		
		school_name_list = []
		school_name = tracker_soup.find_all('span',{'class':'programTitle'})
		for school in school_name:
			#print school.text
			school_name_list.append(school.text)
		#print school_name_list

		program_type_list = []
		program_types = tracker_soup.find_all('span',{'class':'type'})
		for program_type in program_types:
			#print program_type.text
			program_type_list.append(program_type.text)
		#print program_type_list

		ugpa_list = []
		ugpas = tracker_soup.find_all('div',{'class':'listBlock ugpa'})
		for ugpa in ugpas:
			ugpa = str(ugpa.text)
			ugpa = ugpa.replace('\n','')
			#print ugpa
			ugpa_list.append(ugpa)
		#print ugpa_list

		GRE_Q_list = []
		GRE_Qs = tracker_soup.find_all('div',{'class':'listBlock GRE_Q'})
		for GRE_Q in GRE_Qs:
			GRE_Q = str(GRE_Q.text)
			GRE_Q = GRE_Q.replace('\n','')
			#print GRE_Q.text
			GRE_Q_list.append(GRE_Q)
		#print GRE_Q_list

		GRE_V_list = []
		GRE_Vs = tracker_soup.find_all('div',{'class':'listBlock GRE_V'})
		for GRE_V in GRE_Vs:
			GRE_V = str(GRE_V.text)
			GRE_V = GRE_V.replace('\n','')
			#print GRE_V.text
			GRE_V_list.append(GRE_V)
		#print GRE_V_list

		GRE_AWA_list = []
		GRE_AWAs = tracker_soup.find_all('div',{'class':'listBlock GRE_AWA'})
		for GRE_AWA in GRE_AWAs:
			GRE_AWA = str(GRE_AWA.text)
			GRE_AWA = GRE_AWA.replace('\n','')
			#print GRE_AWA.text
			GRE_AWA_list.append(GRE_AWA)
		#print GRE_AWA_list

		submitted_list = []
		submitteds = tracker_soup.find_all('div',{'class':'listBlock submitted'})
		for submitted in submitteds:
			submitted = str(submitted.text)
			submitted = submitted.replace('\n','')
			submitted = submitted.replace(' ','')
			submitted_list.append(submitted)
		#print submitted_list

		
		result_list = []
		results = tracker_soup.find_all('div',{'class':'listBlock result'})
		for result in results:
			result = str(result.text)
			result = result.replace('\n','').replace('\t','')
			result_list.append(result)
		#print result_list

		
		raw = [school_name_list,program_type_list,ugpa_list,GRE_Q_list,GRE_V_list,GRE_AWA_list,submitted_list,result_list]
		tracker_list = np.array(raw)
		tracker_list = np.transpose(tracker_list)
		#print tracker_list
		
		for i in range(20):
			print str(i+1)+'.',school_name_list[i],program_type_list[i],ugpa_list[i],GRE_Q_list[i],GRE_V_list[i],GRE_AWA_list[i],submitted_list[i],result_list[i]

		'''
		#r1 至r7 为分割后的正则表达式删选方法
		r1 = '<div class="listBlock program">.*?<span class="programTitle"><a.*?>(.*?)</a>.*?<span class="type">(.*?)</span>.*?</div>'
		r2 = '.*?<div class="listBlock ugpa">.*?<div class="titleText">(.*?)</div>'
		r3 = '.*?<div class="listBlock GRE_Q">.*?<div class="titleText">(.*?)</div>'
		r4 = '.*?<div class="listBlock GRE_V">.*?<div class="titleText">(.*?)</div>'
		r5 = '.*?<div class="listBlock GRE_AWA">.*?<div class="titleText">(.*?)</div>'
		r6 = '.*?<div class="listBlock submitted">.*?<div class="titleText">(.*?)</div>.*?</div>'
		r7 = '.*?<div class="listBlock result">.*?<div class="titleText">.*?<span class="qnt_field_result_.*?">(.*?)</span>.*?<div class="secondRow">(.*?)</div>.*?'
		
		pattern = re.compile(r1+r2+r3+r4+r5+r6+r7,re.S)
		items = re.findall(pattern,content)
		tracker = [] #创建一个用于储存爬取结果的tracker 列表
		list_num = 0
		for item in items:
			list_num += 1
			print list_num,item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]
			tracker.append([item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]])
		return tracker
		'''
spider = qtspider()
spider.getPageContent(raw_input('input page number: '))