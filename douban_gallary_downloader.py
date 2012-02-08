#!/usr/bin/python
#it's ugly ,but it works :-)

from BeautifulSoup import BeautifulSoup
import urllib2
import urllib
import sys
import os
import time

#proxy = urllib2.ProxyHandler({'http': '172.19.1.2:8217'})
#opener = urllib2.build_opener(proxy)
#urllib2.install_opener(opener)

if len(sys.argv) != 4:
	print "usage: ./xxx douban_url out_path pic_cnt"
	sys.exit(1)

input_url = sys.argv[1]
output_path = sys.argv[2]
all_cnt = int(sys.argv[3])

if os.path.isdir(output_path):
	os.chdir(output_path)
else:
	print "dir not exist ,mkdir "
	os.mkdir(output_path)
	os.chdir(output_path)

if input_url[:7]!="http://":
	input_url = "http://"+input_url



headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		 'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7',
		 'Accept-Language':'zh-cn,zh;q=0.5',
		 'Cache-Control':'max-age=0',
		 'Connection':'keep-alive',
		 'Keep-Alive':'115',
		 'Referer':"http://www.renren.com",
		 'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.14) Gecko/20110221 Ubuntu/10.10 (maverick) Firefox/3.6.14'
		}

now_url = input_url
pic_cnt = 0
soup=None
pic_list=None

print "input url is "+ input_url
print "output path is " + output_path

while True:
	try:
		req = urllib2.Request(now_url, headers=headers)		
		response = urllib2.urlopen(req)
		doc = response.read()
		soup = BeautifulSoup(doc)
		
		pic_list = soup.findAll(attrs={"class":"mainphoto"})
		print "html markup is "+str(pic_list)
		next_url = soup.findAll(attrs={"class":"mainphoto"})[0]["href"]
		if next_url.find("douban.com") == -1:
			next_url = "http://www.douban.com"+next_url
		print "next url is "+next_url
		pic_url =  soup.findAll(attrs={"class":"mainphoto"})[0].contents[1]["src"]
		print "pic url is "+pic_url
		pic_content = urllib.urlopen(pic_url).read()
		pic_name = pic_url.split("/")[-1]
		pic_file = open(pic_name,"wb")
		pic_file.write(pic_content)
		pic_file.close()
		pic_cnt += 1
		print "save pic to "+pic_name +"in dir "+output_path

		time.sleep(10)
		
		if next_url == input_url:
			break
		else:
			now_url = next_url
	except Exception,err:
		print err
		print soup
		print pic_list
		break
	
print "downloaded "+ str(pic_cnt)+" in all :-)"

