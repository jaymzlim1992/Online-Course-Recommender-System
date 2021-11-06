# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path
from bs4 import BeautifulSoup

#all pages starting from index 1 will be scraped
start_directory_page = 1

url_noPage = 'https://www.coursera.org/directory/courses?page='

#lists to store data of courses from the same directory page
title = []
category = []
sub_category = []
course_project = []
difficulty = []
requirements = []
instructors = []
institution = []
number_enrolled = []
avg_rating = []
ratings_count = []
free_without_cert = []
cert_cost = []
duration = []
skills = []
main_lang = []
subtitle_lang = []
description = []
link = []

def create_csv():
    courses_df = pd.DataFrame(columns=["Title", "Category", "Sub-category", "CourseOrProject", "Difficulty", "Requirements",
                                       "Instructor(s)", "Institution(s)", "No. of Students Enrolled", "Rating", "No. of ratings",
                                       "Free Access?", "Upgrade to Cert", "Duration", "Skills", "Main Language",
                                       "Subtitles", "Description", "Link"])
    courses_df.to_csv('coursera_courses_eng.csv', index=False, encoding='utf_8_sig')

def create_error_file():
    with open('coursera_scraping_report.txt', 'w') as f:
        f.write('Here are the courses which did not get scraped, and their error messsages:\n')
        f.close()

#scrapes data from a course and appends it to the list
def scrape_indiv_course(courseName):
    url = "https://www.coursera.org/" + courseName
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text,'html.parser')

    #call the appropriate scraping function based on Project or Course
    if 'Guided Project' not in soup.text:
        scrape_course_details(soup,courseName)
    else:
        scrape_project_details(soup,courseName)

def scrape_course_details(soup,courseName):
    #If the course main language is not English, we do not scrape it
    try:
        about_section = soup.find('div', class_='_1b7vhsnq m-t-2')
        about_items = about_section.find_all('div', class_='_16ni8zai m-b-0')
        if about_items[-1].text != "English":
            with open('coursera_scraping_report.txt', 'a') as f:
                f.write(f'Error: "{courseName}" is not an English course.\n')
            return
    except:
        with open('coursera_scraping_report.txt', 'a') as f:
            f.write(f'Error: Unable to get main language of course "{courseName}".\n')
        return
    course_project.append('Course')
    try:
        category.append(soup.find_all('div', class_='_1ruggxy')[1].contents[0].get_text())
    except:
        category.append("Not mentioned")
    try:
        sub_category.append(soup.find_all('div', class_='_1ruggxy')[2].contents[0].get_text())
    except:
        sub_category.append("Not mentioned")

    try:
        about_section = soup.find('div', class_='_1b7vhsnq m-t-2')
        about_items = about_section.find_all('div', class_='_1tu07i3a')
        main_lang.append(about_items[-1].find('div',class_='_16ni8zai m-b-0').get_text())
    except:
        main_lang.append("Not mentioned")
        subtitle_lang.append("Not mentioned")
        difficulty.append("Not mentioned")
    try:
        subtitle_lang.append(about_items[-1].find('div',class_='font-sm text-secondary').text.replace('Subtitles: ',''))
    except:
        subtitle_lang.append("Not mentioned")
    try:
        difficulty_ = about_items[-3].contents[0].get_text()
        difficulty_keywords = ['beginner', 'advanced', 'intermediate', 'level']
        if not any(keyword in difficulty_.lower() for keyword in difficulty_keywords):
            difficulty_ = "Not mentioned"
        difficulty.append(difficulty_)
    except:
        difficulty.append("Not mentioned")
    try:
        requirements_ = about_items[-3].find('div', class_='rc-CML show-soft-breaks').get_text()
        if requirements_.strip() == "":
            requirements_ = "Not mentioned"
        requirements.append(requirements_)
    except:
        requirements.append("Not mentioned")

    try:
        title.append(soup.find('h1', class_='banner-title banner-title-without--subtitle m-b-0').get_text().strip(" "))
    except:
        title.append("Not mentioned")
    try:
        avg_rating.append(soup.find('div',class_='rc-ReviewsOverview__totals__rating').get_text())
    except:
        avg_rating.append("Not mentioned")
    try:
        ratings_count.append(soup.find('div', class_='_wmgtrl9 color-white ratings-count-expertise-style').span.get_text().split(' ')[0].replace(',',''))
    except:
        ratings_count.append("Not mentioned")
    try:
        institution_ = ""
        institution_soup = soup.find_all('h3', class_='headline-4-text bold rc-Partner__title')
        for i in institution_soup:
            institution_ = institution_ + i.get_text() + ", "
        institution_ = institution_.strip(", ")
        if institution_ == "":
            institution_ = "Not mentioned"
        institution.append(institution_)
    except:
        institution.append("Not mentioned")

    #we get description, duration, language, subtitles, skills from here
    try:
        description.append(about_section.find('div',class_='m-t-1 description').get_text().replace('"',"'"))
    except:
        description.append("Not mentioned")
    try:
        duration_container = soup.find('div',class_='ProductGlance').find_all('div',class_='_16ni8zai m-b-0 m-t-1s')[-1]
        duration.append(duration_container.span.get_text())
    except:
        duration.append("Not mentioned")

    try:
        skills_ = ""
        skills_html = about_section.find_all('span',class_='_1q9sh65')
        for skill in skills_html:
            skills_ = skills_ + skill.get_text() + ", "
        skills_ = skills_.strip(", ")
        if skills_ == "":
            skills_ = "Not mentioned"
        skills.append(skills_)
    except:
        skills.append("Not mentioned")

    #get instructor details
    try:
        instructor_section = soup.find('div',class_='rc-InstructorListSection')
    except:
        instructors.append("Not mentioned")
    try:
        instructors_html = instructor_section.find_all('h3',class_='instructor-name headline-3-text bold')
        instructors_ = ""
        for instructor in instructors_html:
            instructors_ = instructors_ + instructor.contents[0] + ", "
        instructors_ = instructors_.strip(", ")
        instructors.append(instructors_)
    except:
        instructors.append("Not mentioned")
    try:
        if 'Enroll for Free' in soup.get_text():
            free_without_cert_ = 'Yes'
        else:
            free_without_cert_ = 'No'
    except:
        free_without_cert_ = "Not mentioned"
    free_without_cert.append(free_without_cert_)

    try:
        paid_course_text = 'If you only want to read and view the course content, you can audit the course for free'
        if paid_course_text in soup.find('div', class_='FAQs p-t-5 p-b-1 bg-light-blue').get_text():
            cert_cost_ = 'Paid'
        else:
            cert_cost_ = 'Free'
    except:
        cert_cost_ = "Not mentioned"
    cert_cost.append(cert_cost_)

    try:
        number_enrolled_ = soup.find('div',class_='rc-ProductMetrics').get_text().replace(',','').replace('already enrolled','').strip()
    except:
        number_enrolled_ = "Not mentioned"
    number_enrolled.append(number_enrolled_)

    link_ = "https://www.coursera.org/" + courseName.strip('/')
    link.append(link_)

def scrape_project_details(soup,courseName):
    # If the project (course) main language is not English, we do not scrape it
    try:
        about_items = soup.find_all('span', class_='_1rcyblj')
        main_lang_ = ""
        for item in about_items:
            if "English" in item:
                main_lang_ = item.get_text()
        if "English" not in main_lang_:
            with open('coursera_scraping_report.txt', 'a') as f:
                f.write(f'Error: "{courseName}" is not an English project.\n')
            return
    except:
        with open('coursera_scraping_report.txt', 'a') as f:
            f.write(f'Error: Unable to get main language of project "{courseName}".\n')
        return
    main_lang.append(main_lang_)
    subtitle_lang.append("N/A")
    course_project.append('Project')

    try:
        title.append(soup.find('h1', class_='_125g251l _gkjc69').get_text().strip(" "))
    except:
        title.append("Not mentioned")
    try:
        category.append(soup.find_all('div', class_='_1ruggxy')[1].contents[0].get_text())
    except:
        category.append("Not mentioned")
    try:
        sub_category.append(soup.find_all('div', class_='_1ruggxy')[2].contents[0].get_text())
    except:
        sub_category.append("Not mentioned")
    try:
        difficulty_ = soup.find_all('div', class_='_8m7gipb _1f096on')[1].contents[1].get_text()
        difficulty_keywords = ['beginner', 'advanced', 'intermediate', 'level']
        if not any(keyword in difficulty_.lower() for keyword in difficulty_keywords):
            difficulty_ = "Not mentioned"
        difficulty.append(difficulty_)
    except:
        difficulty.append("Not mentioned")
    try:
        requirements.append(soup.find_all('div', class_='_1tu07i3a')[-1].find('div', class_='rc-CML show-soft-breaks').get_text())
    except:
        requirements.append("Not mentioned")

    avg_rating.append("N/A")
    ratings_count.append("N/A")
    try:
        institution.append(soup.find('img',class_='_1g3eaodg _3raxy0')['title'])
    except:
        institution.append("Not mentioned")

    #we get description, duration, language, subtitles, skills from here
    description_ = ""
    try:
        description_ = description_ + soup.find('div',class_='_1lkgrbf').get_text() + "\n"
    except:
        pass
    try:
        description_= description_ + soup.find('p',class_='_g61i7y').get_text().replace('"',"'") + "\n"
    except:
        description_= description_ + "Not mentioned"
    try:
        description_ = description_ + soup.find('p',class_='_1w111ra').get_text() + "\n"
    except:
        pass
    try:
        desc_steps = soup.find_all('li',class_='_18u04q8')
        for step in desc_steps:
            description_ = description_ + step.get_text() + "\n"
    except:
        pass
    description.append(description_)

    try:
        duration.append(about_items[0].get_text())
    except:
        duration.append("Not mentioned")

    try:
        skills_ = ""
        skills_section = soup.find('div',class_='Skills _14ced0o')
        skills_html = skills_section.find_all('span',class_='_1q9sh65')
        for skill in skills_html:
            skills_ = skills_ + skill.get_text() + ", "
        skills_ = skills_.strip(", ")
        skills.append(skills_)
    except:
        skills.append("Not mentioned")

    #get instructor details
    try:
        instructors_html = soup.find_all('h3',class_='instructor-name headline-3-text bold')
        instructors_ = ""
        for instructor in instructors_html:
            instructors_ = instructors_ + instructor.contents[0] + ", "
        instructors_ = instructors_.strip(", ")
        instructors.append(instructors_)
    except:
        instructors.append("Not mentioned")
    try:
        if 'Free Guided Project' in soup.get_text():
            free_without_cert_ = 'Free Guided Project'
        else:
            free_without_cert_ = 'No'
    except:
        free_without_cert_ = "Not mentioned"
    free_without_cert.append(free_without_cert_)

    try:
        paid_course_text = 'Auditing is not available for Guided Projects.'
        if paid_course_text in soup.get_text():
            cert_cost_ = 'Paid'
        else:
            cert_cost_ = 'Free'
    except:
        cert_cost_ = "Not mentioned"
    cert_cost.append(cert_cost_)

    number_enrolled.append("N/A")

    link_ = "https://www.coursera.org/" + courseName.strip('/')
    link.append(link_)

def get_page_links(url):
    service = Service(binary_path)
    service.start()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Remote(service.service_url,options=options)
    driver.get(url);
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, 'html.parser')
    courses_html = soup.find_all('li',class_='MuiTypography-root css-v4ktz5 MuiTypography-body1')

    course_links = []
    for course in courses_html:
        course_links.append(course.a["href"])

    driver.quit()
    return course_links

def scrape_all(list):
    for course in list:
        scrape_indiv_course(course)
    #scrape_indiv_course(list[0])

def output_to_csv():
    #create df using dictionary of data lists
    courses_info_combine = pd.DataFrame({"Title":title, "Category":category, "Sub-category":sub_category, "CourseOrProject":course_project,
                                         "Difficulty":difficulty, "Requirements":requirements, "Instructor(s)":instructors,
                                         "Institution":institution, "No. of Students Enrolled":number_enrolled, "Rating":avg_rating,
                                         "No. of ratings":ratings_count, "Free Access?":free_without_cert, "Upgrade to Cert":cert_cost,
                                         "Duration":duration, "Skills":skills, "Main Language":main_lang, "Subtitles":subtitle_lang,
                                         "Description:":description, "Link":link})
    #appending data to csv
    courses_info_combine.to_csv('coursera_courses_eng.csv', mode='a', index=False, header=None, encoding='utf-8-sig')

def clear_lists():
    global title
    global category
    global sub_category
    global course_project
    global difficulty
    global requirements
    global instructors
    global institution
    global number_enrolled
    global avg_rating
    global ratings_count
    global free_without_cert
    global cert_cost
    global duration
    global skills
    global main_lang
    global subtitle_lang
    global description
    global link
    title = []
    category = []
    sub_category = []
    course_project = []
    difficulty = []
    requirements = []
    instructors = []
    institution = []
    number_enrolled = []
    avg_rating = []
    ratings_count = []
    free_without_cert = []
    cert_cost = []
    duration = []
    skills = []
    main_lang = []
    subtitle_lang = []
    description = []
    link = []

if __name__ == '__main__':
    create_csv()
    create_error_file()
    #for index in range(start_directory_page,end_directory_page+1):
    page_index = start_directory_page
    pageUrl = f'{url_noPage}{page_index}'
    while requests.get(pageUrl).status_code == 200:
        print(pageUrl)
        course_links = get_page_links(pageUrl)
        scrape_all(course_links)
        output_to_csv()
        clear_lists()
        page_index = page_index + 1
        pageUrl = f'{url_noPage}{page_index}'
