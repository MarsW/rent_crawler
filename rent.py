# encoding: utf-8

import urllib2,urllib
from lxml import etree
import json

import geo

import datetime
import time

import MySQLdb

_DB_ip=""
_DB_account=""
_DB_passwd=""
_DB_table=""

def insert(sql):
	db = MySQLdb.connect(_DB_ip,_DB_account,_DB_passwd,_DB_table )
	cursor = db.cursor()
	cursor.execute("SET NAMES UTF8")
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
		print sql
		return 0
	db.close()
	return 1

def main():
	
	db = MySQLdb.connect(_DB_ip,_DB_account,_DB_passwd,_DB_table )
	cursor = db.cursor()
	sql = "SELECT `url` FROM `rent`"
	try:
		cursor.execute(sql)
	except:
		print "SELECT Error"
	results = cursor.fetchall()
	
	db_urls=[]
	
	for i in results:
		db_urls.append(i[0])
	
	url_list = []
	#台北市 3房
	url_list.append("http://rent.591.com.tw/index.php?module=search&action=rslist&is_new_list=1&type=1&searchtype=1&region=1&orderType=desc&listview=img&pattern=3&rentprice=20000,35000")
	#台北市 4房
	url_list.append("http://rent.591.com.tw/index.php?module=search&action=rslist&is_new_list=1&type=1&searchtype=1&region=1&orderType=desc&listview=img&pattern=4&rentprice=20000,35000")	
	#新北市 3房
	url_list.append("http://rent.591.com.tw/index.php?module=search&action=rslist&is_new_list=1&type=1&searchtype=1&region=3&orderType=desc&listview=img&pattern=3&rentprice=20000,35000")	 
	#新北市 4房
	url_list.append("http://rent.591.com.tw/index.php?module=search&action=rslist&is_new_list=1&type=1&searchtype=1&region=3&orderType=desc&listview=img&pattern=4&rentprice=20000,35000")	
	
	for urls in url_list:
		req = urllib2.Request(urls+"&firstRow=0")
		response = urllib2.urlopen(req)
		html = response.read()
		data1 = json.loads(html)
		count = data1['count']

		for firstrow in range(0,200):
			print urls+"&firstRow="+str(firstrow*20)
			if firstrow*20 > int(count):
				break
			req = urllib2.Request(urls+"&firstRow="+str(firstrow*20))
			response = urllib2.urlopen(req)
			html = response.read()
			data1 = json.loads(html)
			page = etree.HTML(data1['main'])
			
			for i in page.xpath(u"//div[@class='shList ']"):
				price = i.xpath(u".//li[@class='price fc-org']/strong/text()")[0].encode('utf8').replace(",","").replace("元","")
				
				temp = i.xpath(u".//li[@class='info']/div/p/text()")[0].encode('utf8')
				address = temp.split("　")
				if len(address)>1:
					address = address[1]
				else:
					address = address[0]
				address = address.replace(" ","").replace("-","")

				layout = i.xpath(u".//li[@class='info']/div/p/span/text()")[0].encode('utf8')
				
				url = "http://rent.591.com.tw/"+i.xpath(u".//li[@class='info']/div/a/@href")[0]
				img_url = i.xpath(u".//li[@class='info']/div/a/img/@src")[0] 
				print price,address,layout
			
				if url in db_urls:
					print price,address,layout,"Existed"
					continue


				#通勤時間 ======================================
				#input_address = geo.get_location(address)
				duration_marsw = geo.get_duration11(address)
				duration_awoo = geo.get_duration12(address)
				duration_akoung = geo.get_duration13(address)
				try:
					duration_marsw = duration_marsw.encode('utf8')
				except:
					duration_marsw = duration_marsw
				try:
					duration_awoo = duration_awoo.encode('utf8')
				except:
					duration_awoo = duration_awoo
				try:
					duration_akoung = duration_akoung.encode('utf8')
				except:
					duration_akoung = duration_akoung

				#通勤時間限制
				marsw=0
				rating_marsw=0
				if duration_marsw!="":
					temp1 = duration_marsw.replace(" ","").replace("分","")
					if "小時" in temp1:
						temp1 = temp1.split("小時")
						marsw = int(temp1[0])*60+int(temp1[1])
					else:
						marsw = int(temp1)
				if marsw>=30:
					rating_marsw=-1

				awooo=0
				rating_awoo=0
				if duration_awoo!="":
					temp2 = duration_awoo.replace(" ","").replace("分","")
					if "小時" in temp2:
						temp2 = temp2.split("小時")
						awooo = int(temp2[0])*60+int(temp2[1])
					else:
						awooo = int(temp2)
				if awooo>=30:
					rating_awoo=-1

				#Output ============================================
				print price,address,layout,#,url,img_url
				print "翁:",duration_marsw,"嗚:",duration_awoo#,"貢:",duration_akoung

				mtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
				
				if rating_marsw==-1 and rating_awoo==-1:
					sql = """INSERT INTO  `marsw`.`rent` (
						`sn` ,`price` ,`layout` ,`furniture` ,
						`address` ,`marsw` ,`awooo` ,`akoung` ,`note` ,
						`url` ,`img_url` ,
						`rating_marsw` ,`rating_akoung` ,`rating_awoo` ,`rating_fufu` ,
						`mtime`
						)
						VALUES ( NULL , '%d',  '%s', NULL , 
							'%s', '%s' , '%s' , '%s' , NULL ,  
							'%s', '%s' , 
							'-1' , NULL , '-1' , NULL ,  
							'%s'
						)"""%(int(price), layout,address,duration_marsw,duration_awoo,duration_akoung,url,img_url,mtime)
					insert(sql)
				elif rating_marsw==-1:
					sql = """INSERT INTO  `marsw`.`rent` (
						`sn` ,`price` ,`layout` ,`furniture` ,
						`address` ,`marsw` ,`awooo` ,`akoung` ,`note` ,
						`url` ,`img_url` ,
						`rating_marsw` ,`rating_akoung` ,`rating_awoo` ,`rating_fufu` ,
						`mtime`
						)
						VALUES ( NULL , '%d',  '%s', NULL , 
							'%s', '%s' , '%s' , '%s' , NULL ,  
							'%s', '%s' , 
							'-1' , NULL , NULL , NULL ,  
							'%s'
						)"""%(int(price), layout,address,duration_marsw,duration_awoo,duration_akoung,url,img_url,mtime)
					insert(sql)
				elif rating_awoo==-1:
					sql = """INSERT INTO  `marsw`.`rent` (
						`sn` ,`price` ,`layout` ,`furniture` ,
						`address` ,`marsw` ,`awooo` ,`akoung` ,`note` ,
						`url` ,`img_url` ,
						`rating_marsw` ,`rating_akoung` ,`rating_awoo` ,`rating_fufu` ,
						`mtime`
						)
						VALUES ( NULL , '%d',  '%s', NULL , 
							'%s', '%s' , '%s' , '%s' , NULL ,  
							'%s', '%s' , 
							NULL , NULL , '-1' , NULL ,  
							'%s'
						)"""%(int(price), layout,address,duration_marsw,duration_awoo,duration_akoung,url,img_url,mtime)
					insert(sql)
				else:
					sql = """INSERT INTO  `marsw`.`rent` (
						`sn` ,`price` ,`layout` ,`furniture` ,
						`address` ,`marsw` ,`awooo` ,`akoung` ,`note` ,
						`url` ,`img_url` ,
						`rating_marsw` ,`rating_akoung` ,`rating_awoo` ,`rating_fufu` ,
						`mtime`
						)
						VALUES ( NULL , '%d',  '%s', NULL , 
							'%s', '%s' , '%s' , '%s' , NULL ,  
							'%s', '%s' , 
							NULL , NULL , NULL , NULL ,  
							'%s'
						)"""%(int(price), layout,address,duration_marsw,duration_awoo,duration_akoung,url,img_url,mtime)
					insert(sql)
				
			break
if __name__ == "__main__":
	main()
	
	
	