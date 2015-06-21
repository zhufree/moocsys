#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import re
import urllib2 

def getcourseinfo():
    hand_url='http://www.icourse163.org'
    pageSoup=BeautifulSoup(urllib2.urlopen(urllib2.Request(hand_url)))
    #print pageSoup
    boxs=pageSoup.find_all('a',{'class':re.compile('courseCard')})
    titles=[box['title'] for box in boxs]
    schools=[box.p.string for box in boxs]
    img_urls=[box.img['src'] for box in boxs]
    info_urls=[hand_url+box['href'] for box in boxs]
    teachers=[BeautifulSoup(urllib2.urlopen(urllib2.Request(info_url))).find('h3',{'class':'f-fc3'}).string for info_url in info_urls]
    return (titles,teachers,schools,img_urls)
