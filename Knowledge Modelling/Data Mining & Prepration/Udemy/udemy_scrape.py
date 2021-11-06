# -*- coding: utf-8 -*-
"""Udemy_scrape.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C9y6HBDGCHKCpeJ_GPgAsglEIiQ7ZHfX

#1.Preparation
"""

!apt update
!apt install chromium-chromedriver
!pip install selenium

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pandas as pd
import requests
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument('blink-settings=imagesEnabled=false')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=options)
browser.implicitly_wait(20)

courses_info = pd.DataFrame(columns = ['name','description','link','instructors','rating','length','level','bestseller','price','enroll','language'])
course_name = []
descriptions = []
course_link = []
instructors = []
ratings = []
lengths = []
difficulties = []
bestsellers = []
prices = []
enrolls= []
languages =[]

for i in range(1,303):

    url = 'https://www.udemy.com/courses/music/?locale=en_US&p=' + str(i)
    browser.get(url)

    sleep(7)
    html = browser.page_source
    soup = BeautifulSoup(html,'lxml')
    courseList = soup.find('div',class_ = 'course-list--container--3zXPS')
    courses = courseList.findAll('div',class_ = 'popper--popper--2r2To popper--popper-hover--3YydE')

    for course in courses:
        link = course.find('a',class_ = 'udlite-custom-focus-visible browse-course-card--link--3KIkQ').get('href')
        try:
            instructor = course.find('div', class_ = 'udlite-text-xs course-card--instructor-list--nH1OC').text
        except:
            instructor = ''
        try:
            rating = course.find('span', class_ = 'udlite-heading-sm star-rating--rating-number--2o8YM').text
        except:
            rating = ''
        name = course.find('div',class_ ="udlite-focus-visible-target udlite-heading-md course-card--course-title--vVEjC").text
        info = course.findAll('span',class_ = 'course-card--row--29Y0w')
        length = info[0].text
        level =  info[-1].text
        try:
            desc = course.find('p',class_='udlite-text-sm course-card--course-headline--2DAqq').text
        except:
            desc = ''
        try:
            price_tag = course.find('div',class_='price-text--container--103D9 course-card--price-text-container--XIYmk')
            price = price_tag.findAll('span')[2].text
        except:
            price = ''
        try:
            bestseller = course.find('div',class_ = 'udlite-badge udlite-heading-xs udlite-badge-bestseller ').text
        except:
            bestseller = ''
        #print(bestseller)
        #html_course = requests.get('https://www.udemy.com'+link).content
        #soupcourse = BeautifulSoup(html_course,'lxml')
        #enroll = soupcourse.find('div',{'data-purpose':'enrollment'}).text
        #language = soupcourse.find('div',class_= 'clp-lead__element-item clp-lead__locale').text
        course_name.append(name)
        descriptions.append(desc)
        course_link.append('https://www.udemy.com'+link)
        instructors.append(instructor)
        ratings.append(rating)
        lengths.append(length)
        difficulties.append(level)
        bestsellers.append(bestseller)
        prices.append(price)
        #enrolls.append(enroll.strip())
        #languages.append(language.strip())
    print(f'page {i} scraped')


browser.close()

courses_info.name = course_name
courses_info.description = descriptions
courses_info.link = course_link
courses_info.instructors = instructors
courses_info.rating = ratings
courses_info.length = lengths
courses_info.level = difficulties
courses_info.bestseller = bestsellers
courses_info.price = prices

courses_info.to_csv('courses_info_music.csv',encoding='utf_8_sig')

