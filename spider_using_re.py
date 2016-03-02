'''
使用re 来筛选的爬虫
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
