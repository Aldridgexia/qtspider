1# -*- coding: utf-8 -*-
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

	#生成用于分析的tracker_soup
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
	#获取tracker_soup 中的有效信息
	def getPageContent(self,page_num):
		tracker_soup = self.getPage(page_num)

		#获取项目名称列表
		school_name_list = []
		school_name = tracker_soup.find_all('span',{'class':'programTitle'})
		for school in school_name:
			school_name_list.append(school.text)

		#获取项目类型列表
		program_type_list = []
		program_types = tracker_soup.find_all('span',{'class':'type'})
		for program_type in program_types:
			program_type_list.append(program_type.text)

		#获取ugpa 列表
		ugpa_list = []
		ugpas = tracker_soup.find_all('div',{'class':'listBlock ugpa'})
		for ugpa in ugpas:
			ugpa = str(ugpa.text)
			ugpa = ugpa.replace('\n','')
			ugpa_list.append(ugpa)

		#获取gre 数学成绩列表
		GRE_Q_list = []
		GRE_Qs = tracker_soup.find_all('div',{'class':'listBlock GRE_Q'})
		for GRE_Q in GRE_Qs:
			GRE_Q = str(GRE_Q.text)
			GRE_Q = GRE_Q.replace('\n','')
			GRE_Q_list.append(GRE_Q)

		#获取gre 语文成绩列表
		GRE_V_list = []
		GRE_Vs = tracker_soup.find_all('div',{'class':'listBlock GRE_V'})
		for GRE_V in GRE_Vs:
			GRE_V = str(GRE_V.text)
			GRE_V = GRE_V.replace('\n','')
			GRE_V_list.append(GRE_V)

		#获取gre 作文成绩列表
		GRE_AWA_list = []
		GRE_AWAs = tracker_soup.find_all('div',{'class':'listBlock GRE_AWA'})
		for GRE_AWA in GRE_AWAs:
			GRE_AWA = str(GRE_AWA.text)
			GRE_AWA = GRE_AWA.replace('\n','')
			GRE_AWA_list.append(GRE_AWA)

		#获取提交状态列表
		submitted_list = []
		submitteds = tracker_soup.find_all('div',{'class':'listBlock submitted'})
		for submitted in submitteds:
			submitted = str(submitted.text)
			submitted = submitted.replace('\n','')
			submitted = submitted.replace(' ','')
			submitted_list.append(submitted)

		#获取录取结果列表
		result_list = []
		results = tracker_soup.find_all('div',{'class':'listBlock result'})
		for result in results:
			result = str(result.text)
			result = result.replace('\n','').replace('\t','')
			result_list.append(result)
		#待处理，将三个信息分开展示

		#使用numpy.array 储存以上列表结果并转置 
		raw = [school_name_list,program_type_list,ugpa_list,GRE_Q_list,GRE_V_list,GRE_AWA_list,submitted_list,result_list]
		tracker_list = np.array(raw)
		tracker_list = np.transpose(tracker_list)
		
		#打印出易观察的tracker 信息
		for i in range(20):
			print str(i+1)+'.',school_name_list[i],program_type_list[i],ugpa_list[i],GRE_Q_list[i],GRE_V_list[i],GRE_AWA_list[i],submitted_list[i],result_list[i]

		return tracker_list

spider = qtspider()
#要求用户输入想要爬取的页数
targetNum = raw_input('input page number: ')
for i in range(1,int(targetNum)+1):
	print "Page " + str(i)
	tracker_list = spider.getPageContent(i)

#将tracker_list 写入文件
with open('/Users/Aldridge/qtspider/trackers.txt','w') as f:
	f.write(tracker_list)