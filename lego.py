#Author: Pavani Boga ( pavanianapala@gmail.com )
#Date : 11/24/2017
#Job : https://www.upwork.com/jobs/~01a921be03ba31a230
#Purpose : This script is intended to collect the user reviews on lego toys(especially the age and build time)
#          dump them to the file /tmp/lego.json, which will be visualized using pandas in jupyter notebook
#Run : python lego.py -f /tmp/lego_urls.txt

from selenium import webdriver
import json
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',help='This file will contain the urls of the lego toys for which reviews needs to be collected')
args = parser.parse_args()


legos = list()
lego_urls = list()

for line in open(args.file).readlines():
    if 'http' in line:
        lego_urls.append(line.strip())


browser = webdriver.Chrome()

for url in lego_urls:

    lego_name = url.split('/')[-1]
    browser.get(url)
    browser.maximize_window()
    reviews = list()

    lego_count = browser.find_element_by_xpath('//*[@class="product-details__piece-count"]').text
    while True:
        lego_reviews = browser.find_elements_by_xpath('//div[contains(@id,"BVRRDisplayContentReviewID")]')
        for review in lego_reviews:
            try:
                author = review.find_element_by_xpath('.//*[@itemprop="author"]').text
                age = review.find_element_by_xpath('.//*[@class="BVRRValue BVRRContextDataValue BVRRContextDataValueage"]').text
                try:
                    days = review.find_element_by_xpath('.//*[@class="BVRRValue BVRRContextDataValue BVRRContextDataValuedays"]').text
                except Exception as e:
                    days = '0'
                try:
                    hrs = review.find_element_by_xpath('.//*[@class="BVRRValue BVRRContextDataValue BVRRContextDataValuehours"]').text
                except Exception as e:
                    hrs = '00'
                try:
                    mins = review.find_element_by_xpath('.//*[@class="BVRRValue BVRRContextDataValue BVRRContextDataValueminutes"]').text
                except Exception as e:
                    mins = '00'
                if days == '0' and hrs == '00':
                    raise Exception('time error')
                else:
                    if days != '0' :
                        time_mins = int(days) * 24 * 60 + int(hrs) * 60 + int(mins)
                    else:
                        time_mins = int(hrs) * 60 + int(mins)
                reviews.append({'author' : author, 'age' : age, 'time_mins' : time_mins })
            except Exception as e:
                pass 
        try:
            next_page = browser.find_element_by_xpath('//a[@name="BV_TrackingTag_Review_Display_NextPage"]')
            next_page.send_keys('\n')
            time.sleep(1)
        except Exception as e:
            break

    legos.append( { 'name': lego_name, 'count' : lego_count, 'reviews': reviews } )

browser.close()

with open('/tmp/lego.json','w') as f:
    json.dump(legos,f,indent=4)
