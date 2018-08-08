#Author: Pavani Boga ( pavanianapala@gmail.com )
#Date : 08/07/2018
#Job : https://www.upwork.com/jobs/~01977d8f836e122950
#Purpose : This script is intended to collect the various roof accessory parts of different cars and models
#          dump them to csv file
#Run : python thule.py

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import concurrent.futures
import time
import csv
import logging
from random import shuffle

logging.basicConfig(level=logging.INFO, format='%(asctime)s -  %(threadName)s - %(message)s',filename='thule1.log')



def parse(make_str):
    logging.info('Started parsing for the make - {}'.format(make_str))
    with open('{}.csv'.format(make_str),'w') as csvfile:
        field_names = [ 'Make', 'Year', 'Model', 'Roof', 'Product1', 'Product2', 'Product3', 'Price' ]
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        browser = webdriver.Chrome()
        url = 'https://www.thule.com/en-us/us/roof-rack/roof-bars'
        browser.get(url)
        time.sleep(1)
        car_make = Select(browser.find_element_by_id('main_0_mainframed_4_ucFilters_rptrAttributes_Filter_0_AttributeValues_0_ctl00_0_CarSelector_0_carMakesSelect_0'))
        car_make.select_by_visible_text(make_str)
        time.sleep(0.5)
        car_year = Select(browser.find_element_by_id('main_0_mainframed_4_ucFilters_rptrAttributes_Filter_0_AttributeValues_0_ctl00_0_CarSelector_0_carYearSelect_0'))
        try:
            for year in car_year.options:
                if year.text == 'Select year': continue
                car_year.select_by_visible_text(year.text)
                time.sleep(1)
                car_model = Select(browser.find_element_by_id('main_0_mainframed_4_ucFilters_rptrAttributes_Filter_0_AttributeValues_0_ctl00_0_CarSelector_0_carModelSelect_0'))
                for model in car_model.options:
                    if model.text == 'Select model': continue
                    car_model.select_by_visible_text(model.text)
                    time.sleep(2)
                    roofs = browser.find_elements_by_xpath('//*[@class="carselector-roof-preview radio"]/div')
                    for roof in roofs:
                        if roof.get_attribute("style") != "" : continue
                        roof_radio = roof.find_element_by_xpath('.//label')
                        roof_name = roof.find_element_by_xpath('.//label').get_attribute("data-english-name")
                        roof_radio = roof.find_element_by_xpath('.//label')
                        browser.execute_script("arguments[0].click();",roof_radio)
                        time.sleep(3)
                        products = browser.find_elements_by_xpath('//*[@id="frg-products"]/li')
                        for product in products:
                            product_line = product.find_elements_by_xpath('.//*[contains(@id,"ctl01_solutionRepeater_solutionRecommendation")]/a') 
                            product1 = product_line[0].text if len(product_line) >= 2 else 'NA'
                            product2 = product_line[1].text if len(product_line) >= 4 else 'NA'
                            product3 = product_line[2].text if len(product_line) >= 6 else 'NA'
                            price = product.find_element_by_xpath('.//*[@class="price-value"]').text if product.find_element_by_xpath('.//*[@class="price-value"]') else 'NA'
                            row = { 'Make':  make_str, 'Year': year.text, 'Model': model.text, 'Roof': roof_name, 'Product1': product1, 'Product2': product2, 'Product3': product3,'Price': price }
                            writer.writerow(row)
                        if len(products) == 0:  
                            row = { 'Make': make_str, 'Year': year.text, 'Model': model.text, 'Roof': roof_name, 'Product1': 'NA', 'Product2': 'NA', 'Product3': 'NA', 'Price': 'NA' }
                            writer.writerow(row)
        except Exception as e:
            logging.info('Got the exception : {}'.format(e))
    logging.info('Completed parsing for the make - {}'.format(make_str))
    csvfile.close()
    browser.close() 
        

if __name__ == '__main__':
    browser = webdriver.Chrome()
    url = 'https://www.thule.com/en-us/us/roof-rack/roof-bars'
    browser.get(url)
    time.sleep(1)
    car_make = Select(browser.find_element_by_id('main_0_mainframed_4_ucFilters_rptrAttributes_Filter_0_AttributeValues_0_ctl00_0_CarSelector_0_carMakesSelect_0'))
    make_options = list()
    for make in car_make.options:
        if make.text == 'Select make': continue
        make_options.append(make.text)
    browser.close()
    shuffle(make_options)
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        result = executor.map(parse, make_options)

    
