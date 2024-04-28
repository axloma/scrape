import requests
from bs4 import BeautifulSoup
import os
import shutil
import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By #TODO use by toget element by css selector
# driver = webdriver.Chrome()


# Define the initial URL to scrape

class SCARE():
	initial_url = ''
	weburl = ''
	# lsurls = []
	# lsurls.append(initial_url)
	filetext = 'amaz.txt'
	jsonname = 'dis.json'
	#######initial chromum driver for DYNAMIC SCRAPING
	s = Service(ChromeDriverManager().install())
	driver = webdriver.Chrome(service=s)
	cls = ""	
	tklst = []	
	urllist = []
	diclist = []
	created = False

	def __init__(self,initial_url,nextidx,filetext,fname,jsonname) :

		#######initial chromum driver for DYNAMIC SCRAPING
		# self.s = Service(ChromeDriverManager().install())
		# self.driver = webdriver.Chrome(service=self.s)

		# driver = webdriver.Chrome()
		self.lsurls =[]
		self.initial_url = initial_url
		self.weburl = initial_url
		self.lsurls.append(initial_url)
		# self.lsurls.insert(0,initial_url)
		self.filetext = filetext
		self.next_idx = nextidx
		self.response = requests.get(self.initial_url)
		self.soup = BeautifulSoup(self.response.text, 'html.parser')
		self.fname = fname
		self.jsonname = jsonname

	
	def save(self):
		with open(self.filetext,'w') as f:        
						f.writelines([f"{line}\n" for line in self.lsurls])
		
		# with  open(self.jsonname, "a") as out_file:		
		# 	json.dump(diclist,out_file, indent = 4,ensure_ascii=False)

	# Function to scrape a single page	
	def scrape_p(self):
		#########SCRAPE DYNAIC WITH SELINUM 
		#Step 4: Fetch content from a dynamic website
		self.driver.get(self.initial_url)
		self.js_content = self.driver.page_source
		#Step 5: Parse the HTML content using Beautiful Soup
		self.soup = BeautifulSoup(self.js_content, "html.parser")

		#SCRAPE NORMAL PAGE WITH BS
		response = requests.get(self.initial_url)
		# time.sleep(10)
		# self.soup = BeautifulSoup(response.text, 'html.parser')
  
		# Find all links - adjust the selector to find the required links
		try:
			links = self.soup.find_all(class_=self.next_idx, href=True)
			linksid = False
			if not links:
				print("ERRx")
				links = self.soup.find_all(id=self.next_idx, href=True)
				linksid = True
			print(response.status_code,self.initial_url)	
			# Follow each link (you may want to add conditions here)
		except Exception as l:
			print(l,"LINKERROR")
		for link in links:   
			# Construct the full URL if necessary
			next_page_url = link['href']
			print(next_page_url)
			next_page_url = self.checklink(next_page_url)
			# if not next_page_url.startswith('http'):
			# 	next_page_url = requests.compat.urljoin(self.initial_url, next_page_url)	
			try:
				if linksid:
					if  x := link['data-next'] is  None:
						print("FINSH")
						break
						# p = link['data-next']
						# print(type(p))
						# print(p,"P")
	  
					# else:
					# 	print("FINSH")
					# 	break
				if next_page_url is not None :
					self.lsurls.append(next_page_url)
					print(f'Following link to: {next_page_url}')
					# print(self.lsurls)
					self.initial_url = next_page_url
					print(self.initial_url,"INITIAL")
					# self.lsurls.append(next_page_url)			
					# time.sleep(7)
					self.scrape_p()  # Recursive call to scrape the next page					
			except Exception as e:
				print("E",e)

	#
	def checklink(self,link):
		if not link.startswith('http'):
			link = requests.compat.urljoin(self.initial_url, link)
			print("LINK MODIFIED TO ",link)
		return link
    			# https://m.media-amazon.com/images/I/61pstBPRgcL._AC_SY550_.jpg
	   
	#DOWNlLOAD EACH IMG METHOD 
	def downimg(self,img,name):
		src = img['src']
		alt = img['alt']
		# if not src.startswith('http'):
		# 	src = requests.compat.urljoin(self.initial_url, src)
		src = self.checklink(src)
		match = re.search(r"^(.+/)?(.+)\.(.+)$",src)
		print(match.group(2))
		newalt = name + alt.replace(' ' ,'-').replace('/','').replace('.','') + '.jpg'
		if match.group(2) is not None:
			x = match.group(2)
			x = x.replace(' ' ,'-').replace('/','').replace('.','') + '.' + match.group(3)
			newalt = name + x
		with open(newalt,'wb') as f :
					im = requests.get(src)
					f.write(im.content)
		return newalt
# if not elname.startswith('http'):
#             	elname = requests.compat.urljoin(self.initial_url, elname)
	def con(self,element,patern):
		match = re.search(r"^.*img.*$",patern)
		elname = element.select_one(patern)	
		print(elname.name)	
		if match:		
			print("DOWNLOADING IMG")	
			elname = self.downimg(elname,"fmg")	
		elif elname.name == 'a':
			elnamex = str(elname.text).strip()
			ellink = elname.get('href')
			return elnamex ,ellink
		else:
			elname = str(elname.text).strip()
	
		return elname

	# def get_P(self,cls,xname,price="",disc="",img1="",img2=""):  
 
	def openfile(self):
		with open(self.filetext,'r') as file:
			for line in file :	
				self.urllist.append(line.strip())

	def get_P(self,cls,*ar):

		#TODO create folder if not exist 
		if not self.created:               
			try:
					os.mkdir(os.path.join(os.getcwd(),self.fname))
					shutil.copy(self.filetext,self.fname)
					self.created = True
					
			except:              
				print("error")	
		else:
			print("DIRECTORY ALREADY EXIST CONT")

		self.cls = cls	
		self.tklst = list(ar)	
		os.chdir(os.path.join(os.getcwd(),self.fname))
		# urllist = []
		lst = list(ar)
		
		failedurl = []
		incr = 1
		# with open(self.filetext,'r') as file:
		# 	for line in file :	
		# 		self.urllist.append(line.strip())
		# 	print(self.urllist,"LLL")

		for url in self.urllist:		
			response = requests.get(url) 
			print(url,response.status_code,'sTATUS')
			if response.status_code != 200:
				print("FAILED")
				failedurl.append(url)
				self.get_P(self.cls,self.tklst)
			# else: 
			# 	self.urllist.remove(url)
	
			# soup = BeautifulSoup(response.content,'html.parser')

					#########SCRAPE DYNAIC WITH SELINUM 
			#Step 4: Fetch content from a dynamic website
			self.driver.get(url)
			js_content = self.driver.page_source
			#Step 5: Parse the HTML content using Beautiful Soup
			soup = BeautifulSoup(js_content, "html.parser")

			elements = soup.find_all(attrs={'class':cls})		
			for element in elements:
				try:
					dic = {}
					# elname = element.find(class_=name)
					# xname.replace('\'','')
					# print(lst)
					# elname = element.select_one(lst[0])		
					# elname = str(elname.text).strip()
					elname = self.con(element,lst[0])
					eldisc = self.con(element,lst[1])
					# eldisc = eldisc[0]
					elprice = self.con(element,lst[2])
					ellink = self.con(element,lst[3])
					ellink = ellink[1]
					elfmg = self.con(element,lst[4])
					
					dic['name'] = elname
					dic['disc'] = eldisc
					dic['price'] = elprice
					ellink = self.checklink(ellink)
					dic['link'] = ellink
					dic['fmg'] = elfmg
					print(elname,eldisc,elprice,ellink,elfmg)
		
					# for n in element.descendants:
					# 	if n.name == "img" :
					# 		pass
							# print(n,"FOUND ")

					dic["id"] = incr
					# print(dic['name'])
					self.diclist.append(dic)
					# lst.append(dic)
					incr = incr + 1
					
				except Exception as e :
					print("EROR",e)
			# time.sleep(3)
		with  open(self.jsonname, "w") as out_file:		
			json.dump(self.diclist,out_file, indent = 4,ensure_ascii=False)	
		# while len(failedurl) > 0 :
		# 	self.get_P(self.cls,self.tklst)
		with open('filedurl.txt','w') as fu:
			fu.writelines([f"{line}\n" for line in failedurl])
			print(len(failedurl),"LINK FAILED")
		


			#out_file.write(x)
	# get_P(initial_url,'siomarlall','siomarlall.json')


# firsttry = SCARE('https://siomar.net/product-category/e-liquids/','next page-numbers','new.txt')

# firsttry.scrape_page2()
# firsttry.scrape_p()
# firsttry.save()

###########amazon

# stry = SCARE('https://www.amazon.eg/-/en/s?i=hpc&rh=n%3A21858029031&fs=true&language=en&qid=1714067321&ref=sr_pg_1','s-pagination-item s-pagination-next s-pagination-button s-pagination-separator','amaz.txt','amazonaccess','amazonacess.json')
# stry.scrape_p()
# stry.save()
# stry.openfile()
# stry.get_P('sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20',
# 		   'h2 a span.a-size-base-plus','h2 a span.a-size-base-plus','span.a-price-whole','h2 a.a-link-normal','img')




elclan = SCARE('https://el-clan.com/collections/liquid','load-more-button','elclanl.txt','elclan','elclanl.json')
elclan.scrape_p()
elclan.save()
elclan.openfile()
elclan.get_P('w33','h3 span','h3 a','div p.price','h3 a','img')

# 'next page-numbers'


