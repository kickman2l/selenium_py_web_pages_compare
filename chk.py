import requests
import os
import hashlib
import time
from selenium import webdriver
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException


if os.path.exists('errors.txt'):
    os.remove('errors.txt')
if os.path.exists('success.txt'):
    os.remove('success.txt')
if os.path.exists('not_success.txt'):
    os.remove('not_success.txt')


def get_status_code(url):
    try:
        r = requests.head(url)
        return r.status_code
    except StandardError:
        return False

with open("input.txt") as linksFile:
    content = linksFile.readlines()
Links = [x.strip() for x in content]

cleanedArray = []

for i in Links:
    if "www.schneider-electric.xyz" in i:
        cleanedArray.append(i)


cssJsArray = []
imageArray = []
jspArray = []
linksArray = []
arrForChk = []


def cln_array(lnk):
    data = get_status_code(lnk)
    if (data == 200) or (data == 301):
        return lnk
    else:
        f = open("errors.txt", "a")
        f.write(str(data) + "==" + str(lnk) + "\n")

def check_element_exists():
    try:
        if browser.find_element_by_id("support-bar"):
            print "exists"
            return True
    except NoSuchElementException:
        return False


pool = ThreadPool(24)
arrForChk = pool.map(cln_array, cleanedArray)
arrForChk = [i for i in arrForChk if i is not None]

counter = 0
browser = webdriver.PhantomJS()
browser.maximize_window()
for link in arrForChk:
    browser.get(link)
    time.sleep(3)
    if check_element_exists():
        browser.find_element_by_css_selector("[id=support-bar] label").click()
        time.sleep(1)
    browser.save_screenshot("ss/" + str(counter) + 'xyz_img.png')
    browser.get(link.replace("www.schneider-electric.xyz", "www.schneider-electric.com"))
    time.sleep(3)
    if check_element_exists():
        browser.find_element_by_css_selector("[id=support-bar] label").click()
    time.sleep(1)
    browser.save_screenshot("ss/" + str(counter) + 'com_img.png')
    with open("ss/" + str(counter) + "xyz_img.png", "rb") as xyz_image:
        xyz_string = hashlib.md5(xyz_image.read()).hexdigest()
        xyz_image.close()
    with open("ss/" + str(counter) + "com_img.png", "rb") as com_image:
        com_string = hashlib.md5(com_image.read()).hexdigest()
        com_image.close()
    if xyz_string == com_string:
        f = open("success.txt", "a")
        f.write(link + "\n")
        os.remove("ss/" + str(counter) + 'xyz_img.png')
        os.remove("ss/" + str(counter) + 'com_img.png')
    else:
        f = open("not_success.txt", "a")
        f.write(link + "\n")
    counter += 1
    print str(counter) + "==" + link

browser.quit()

#$("#support-bar label span").click(); getting element



#
# print "===========16=============="
# startTime = datetime.now()
# dataArr = []
# pool = ThreadPool(8)
# dataArr = pool.map(chk_list, arrForChk)
# print datetime.now() - startTime

# print "===========32=============="
# startTime = datetime.now()
# dataArr = []
# browser = webdriver.PhantomJS()
# pool = ThreadPool(32)
# dataArr = pool.map(chk_list, arrForChk)
# print datetime.now() - startTime


# if ((".css" in link) or (".js" in link)) and (".jsp" not in link):
#     cssJsArray.append(link)
# elif (".png" in link) or (".jpg" in link) or (".jpeg" in link) or (".gif" in link):
#     imageArray.append(link)
# elif ".jsp" in link:
#     jspArray.append(link)
# elif ".cfm" not in link:
#     linksArray.append(link)
