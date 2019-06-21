from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import parameters
from parsel import Selector
import csv


def validateField(field):
    if field:
        pass
    else:
        field = ''
    return field

row = ['Name', 'Job Title', 'Location', 'School', 'About', 'LinkedIn Url']
writer = csv.writer(open(parameters.file_name, 'w+', encoding='utf-8'))
writer.writerow(row)

driver = webdriver.Chrome()

def login():
    driver.get('https://www.linkedin.com/login')
    sleep(5)
    # email and password if found then this if block works otherwise its skiped ...
    if parameters.email and parameters.password:
        email_field = driver.find_element_by_xpath('//input[@id="username"]')
        password_field = driver.find_element_by_xpath('//input[@id="password"]')

        email_field.send_keys(parameters.email)
        password_field.send_keys(parameters.password)

        login_btn = driver.find_element_by_xpath('//button[@type="submit"]')
        login_btn.click()
    

def search():
    sleep(5)
    driver.get("https://www.google.com/ncr")
    sleep(5)
    search_query = driver.find_element_by_name('q')
    search_query.send_keys(parameters.search_query)
    sleep(3)
    search_query.send_keys(Keys.RETURN)
    sleep(5)


def find_profile():
    linkedIn_urls = driver.find_elements_by_xpath('//cite[@class="iUh30"]')
    sleep(2)
    linkedIn_urls = [url.text for url in linkedIn_urls]
    sleep(5)
    for profile_url in linkedIn_urls:
        print(f'\n{profile_url}\n')
        driver.get(profile_url)
        sleep(5)
        sel = Selector(text=driver.page_source)

        name = sel.xpath('//li[@class="inline t-24 t-black t-normal break-words"]/text()').extract_first()
        job_title = sel.xpath('//h2[@class="mt1 t-18 t-black t-normal"]/text()').extract_first()
        location = sel.xpath('//li[@class="t-16 t-black t-normal inline-block"]/text()').extract_first()
        school = sel.xpath('//*[@id="ember90"]/text()').extract_first()
        about = sel.xpath('//p[@class="pv-about__summary-text mt4 t-14 ember-view"]//span/text()').extract()

        if about:
            sent = ' '
            for sentence in about:
                sent += sentence.strip()
            about = sent

        if school:
            school = school.strip()

        if location:
            location = location.strip()

        if name:
            name = name.strip()

        if job_title:
            job_title = job_title.strip()        

        linkedin_url = driver.current_url
        name = validateField(name)
        job_title = validateField(job_title)
        location = validateField(location)
        school = validateField(school)
        linkedin_url = validateField(linkedin_url)
        about = validateField(about)

        print(f'Name: {name}')
        print(f'Job Title: {job_title}')
        print(f'Location: {location}')
        print(f'School: {school}')
        print(f'LinkedIn Url: {linkedin_url}')
        print(f'About: {about}')

        sleep(2)

        writer.writerow(["".join(map(chr, name.encode('utf-8'))), 
                        "".join(map(chr, job_title.encode('utf-8'))),
                            "".join(map(chr, location.encode('utf-8'))),
                            "".join(map(chr, school.encode('utf-8'))),
                            "".join(map(chr, about.encode('utf-8'))),
                            "".join(map(chr, linkedin_url.encode('utf-8'))) ])


login()
search()

next_page_url = ''
for i in range(2):
    if i > 0:
        driver.get(next_page_url)
    sel = Selector(text=driver.page_source)
    next_page_url = "https://www.google.com" + sel.xpath('//a[@id="pnnext"]/@href').extract_first()
    print(f'\n{next_page_url}\n')
    sleep(5)
    find_profile()
    sleep(5)
    driver.quit()
    sleep(10)
    driver = webdriver.Chrome()
    sleep(5)
    if i != 1:
        login()
    sleep(5)
    

sleep(2)
print(f"\n------Task Complete------\n")
driver.quit()
