from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pandas as pd
import requests

options = webdriver.ChromeOptions()
#prefs = {"profile.default_content_setting_values.notifications": 2}
#options.add_experimental_option("prefs", prefs)
#options.add_argument('blink-settings=imagesEnabled=false')
#options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument("--incognito")
#options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=options)
# browser.implicitly_wait(20)
browser.get('https://www.google.com/')
browser.execute_script('document.body.style.MozTransform = "scale(0.25)";')

courses_info = pd.DataFrame(columns=['name', 'link', 'imglink'])
course_name = []
course_link = []
course_imglink = []


for i in range(1, 10):

    url = 'https://www.udemy.com/courses/development/?locale=en_US&p=' + str(i)
    browser.get(url)
    sleep(2)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
    sleep(1)
    browser.execute_script("window.scrollTo(0,0)")

    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    courseList = soup.find('div', class_='course-list--container--3zXPS')
    courses = courseList.findAll('div', class_='popper--popper--2r2To popper--popper-hover--3YydE')
    # images = browser.find_elements_by_tag_name('img')
    # print(len(images))
    # for image in images:
    #     print(image.get_attribute('src'))

    for course in courses:
        link = course.find('a', class_='udlite-custom-focus-visible browse-course-card--link--3KIkQ').get('href')
        name = course.find('div', class_="udlite-focus-visible-target udlite-heading-md course-card--course-title--vVEjC").text
        imglink = course.find('img', class_='course-card--course-image--3QvbQ browse-course-card--image--35hYN').attrs['src']

        print(imglink)
        course_name.append(name)
        course_link.append('https://www.udemy.com' + link)
        course_imglink.append(imglink)

    print(f'page {i} scraped')

browser.close()

courses_info.name = course_name
courses_info.link = course_link
courses_info.imglink = course_imglink

courses_info.to_csv('development_imglinks.csv', encoding='utf_8_sig')
