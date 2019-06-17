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
        field=''
    return field


driver = webdriver.Firefox()
driver.get('https://www.linkedin.com/')


sleep(1)

writer = csv.writer(open(parameters.file_name, 'w+'))
writer.writerow(['Name', 'Job Title', 'Location', 'School', 'LinkedIn Url'])

if parameters.email and parameters.password:
    try:
        # If login fields not found in 1st page
        login = driver.find_element_by_xpath('//a[@class="nav__button-secondary"]')
        login.click()

        email_field = driver.find_element_by_xpath('//input[@id="username"]')
        password_field = driver.find_element_by_xpath('//input[@id="password"]')
        
        email_field.send_keys(parameters.email)
        password_field.send_keys(parameters.password)

        login_btn = driver.find_element_by_xpath('//button[@type="submit"]')
        login_btn.click()

    except:
        # If login fields found in 1st page
        email_field = driver.find_element_by_xpath('//input[@class="login-email reg-field__input"]')
        password_field = driver.find_element_by_xpath('//input[@class="login-password reg-field__input"]')

        email_field.send_keys()
        password_field.send_keys()

        login_btn = driver.find_element_by_xpath('//input[@class="login submit-button"]')
        login_btn.click() 

driver.get("https://www.google.com/")

english_format = driver.find_element_by_link_text('English')
english_format.click()
sleep(1)

search_query = driver.find_element_by_name('q')
search_query.send_keys(parameters.search_query)

search_query.send_keys(Keys.RETURN)
sleep(1)

linkedIn_urls = driver.find_elements_by_xpath('//cite[@class="iUh30"]')
linkedIn_urls = [url.text for url in linkedIn_urls]
sleep(1)

for profile_url in linkedIn_urls:
    driver.get(profile_url)
    sleep(2)
    sel = Selector(text=driver.page_source)

    if parameters.email and parameters.password:
        print("\nemail found\n")
        name = sel.xpath('//li[@class="inline t-24 t-black t-normal break-words"]/text()').extract_first().strip()
        job_title = sel.xpath('//h2[@class="mt1 t-18 t-black t-normal"]/text()').extract_first().strip()
        location = sel.xpath('//li[@class="t-16 t-black t-normal inline-block"]/text()').extract_first().strip()
        school = sel.xpath('//li[@href="#education-section"]//span[@class="lt-line-clamp__line lt-line-clamp__line--last"]/text()').extract_first()
        if school:
            school = school.strip()
    else:
        print("\nemail not found\n")
        name = sel.xpath('//div[@class="topcard__info-container"]/h1[@class="topcard__name"]/text()').extract_first().strip()
        job_title = sel.xpath('//div[@class="topcard__info-container"]//h2[@class="topcard__headline"]/text()').extract_first().strip()
        location = sel.xpath('//div[@class="topcard__info-container"]//h3[@class="topcard__location"]/text()').extract_first().strip()
        school = sel.xpath('//div[@class="topcard-links--flex"]//span[@class="topcard-links__description"]/text()').extract_first()
        if school:
            school = school.strip()
        
    linkedin_url = driver.current_url

    name = validateField(name)
    job_title = validateField(job_title)
    location = validateField(location)
    school = validateField(school)
    linkedin_url = validateField(linkedin_url)

    print(f'Name: {name}')
    print(f'Job Title: {job_title}')
    print(f'Location: {location}')
    print(f'School: {school}')
    print(f'LinkedIn Url: {linkedin_url}')

    writer.writerow([ "".join(map(chr, name.encode('utf-8'))), 
                    "".join(map(chr, job_title.encode('utf-8'))), 
                    "".join(map(chr, location.encode('utf-8'))),
                    "".join(map(chr, school.encode('utf-8'))),
                    "".join(map(chr, linkedin_url.encode('utf-8'))) ])

sleep(1)
print(f"\n------Task Complete------\n")
driver.quit()




