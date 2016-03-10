import requests
from lxml import etree
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import sys
reload(sys)

sys.setdefaultencoding('utf-8')
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def towrite(itemdict):
	f.writelines(itemdict['program_name'] + ', ' + itemdict['program_type'] + '\n')
	f.writelines(itemdict['ugpa'] + ', ' + itemdict['gre_q'] + ', ' + itemdict['gre_v'] + ', ' + itemdict['gre_awa'] + '\n' )
	f.writelines(itemdict['submitted'] + ', ' + itemdict['interview'] + '\n')
	f.writelines(itemdict['result'] + ', ' + itemdict['receive_time'] + ', ' + itemdict['days_to_result'] + '\n' )
	f.writelines(unicode(itemdict['note']) + '\n')
	# f.writelines('=====================\n')

def qtspider(url):
	headers={
	"authority":"www.quantnet.com",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
	"scheme":"https",
	"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"accept-encoding":"gzip, deflate, sdch",
	"accept-language":"zh-CN,zh;q=0.8,en;q=0.6",
	"cache-control":"max-age=0",
	}
	html = requests.get(url, headers = headers, verify = False)
	selector = etree.HTML(html.text)
	trackers = selector.xpath('//*[@class="applicationListItem"]')
	item = {}
	for tracker in trackers:
			program_name = tracker.xpath('div[2]/div/h3/span[1]/a/text()')
			program_type = tracker.xpath('div[2]/div/h3/span[2]/text()')
			ugpa = tracker.xpath('div[3]/div/text()')
			gre_q = tracker.xpath('div[4]/div/text()')
			gre_v = tracker.xpath('div[5]/div/text()')
			gre_awa = tracker.xpath('div[6]/div/text()')
			submitted = tracker.xpath('div[7]/div/text()')
			interview = tracker.xpath('div[7]/span/text()')
			if interview:
				interview = interview[0]
			else:
				interview = 'no interview'
			result = tracker.xpath('div[8]/div/div[1]/span[1]/text()')
			receive_time = tracker.xpath('div[8]/div/div[1]/span[2]/text()')
			if receive_time:
			    receive_time = receive_time[0]
			else:
			    receive_time = 'not received yet'
			days_to_result = tracker.xpath('div[8]/div/div[2]/text()')
			note = tracker.xpath('div[9]/div/div/div/text()')
			item['program_name'] = program_name[0]
			item['program_type'] = program_type[0]
			item['ugpa'] = ugpa[0]
			item['gre_q'] = gre_q[0]
			item['gre_v'] = gre_v[0]
			item['gre_awa'] = gre_awa[0]
			item['submitted'] = submitted[0].strip(' \n\t\n ')
			item['interview'] = interview
			item['result'] = result[0]
			item['receive_time'] = receive_time
			item['days_to_result'] = days_to_result[0].strip(' \n\t\n ')
			item['note'] = note[0]
			# print item 
			towrite(item)

if __name__ == '__main__':
	with open('/Users/Aldridge/qtspider/result.csv','a') as f:
		for i in range(1,21):
			new_page = 'https://www.quantnet.com/tracker/?page=' + str(i)
			print 'processing page %d...'%i
			qtspider(new_page)

