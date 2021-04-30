import time
import regex as re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def current_url():
    print("{} {}".format(botname,driver.current_url))

def wait():
    time.sleep(t_sec)


def title():
    print("\n-----------------------------------------")
    print("--------    Runal's Udemy Bot    --------")
    print("-----------------------------------------\n")


def open_chrome_browser(path):
    global driver
    driver = webdriver.Chrome(path)


def open_udmy_site():
    print("{} Opening udemy.com.....".format(botname))
    driver.get("http://udemy.com")
    print("{} On Udemy Page!:".format(botname), driver.title)


def open_udmy_login_page():
    print("{} Opening udemy login page.....".format(botname))
    u_login_page = driver.find_element_by_class_name("header--gap-auth-button--7KoL0")
    u_login_page.click()
    print("{} On login page!".format(botname))


def login_udmy(emid,pwd):
    u_email = driver.find_element_by_id("email--1")
    u_email.send_keys(emid)
    print("{} Email typed!".format(botname))

    time.sleep(2)

    u_pwd = driver.find_element_by_id("id_password")
    u_pwd.send_keys(pwd)
    print("{} Password typed!".format(botname))

    time.sleep(2)

    print("{} Submiting login details.......".format(botname))
    u_login_btn = driver.find_element_by_id("submit-id-submit")
    u_login_btn.click()
    print("{} Login Succ!".format(botname))


def find_course_links(file):
    c_link_li = []
    c = 0
    fh = open(file)
    time.sleep(1)
    print("{} Reading File: {}.......".format(botname,file))
    time.sleep(1)
    print("{} Finding links in: {} file.......".format(botname,file))
    for line in fh:
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
        c_link_li = c_link_li + url
    time.sleep(1)
    # ALL Course links are stored in the list
    print("{} Links Found!-".format(botname))
    time.sleep(1)
    for url in c_link_li:
        c = c + 1
        #time.sleep(1)
        print("{} {}. {}".format(botname, c, url))

    print()
    return c_link_li


def udemy_login():
    open_udmy_site()
    wait()
    print()
    open_udmy_login_page()
    wait()
    login_udmy(email,password)
    wait()


def open_site(site_name,url):
    print("{} {}. Opening {} url.....".format(botname,count,site_name))
    driver.get(url)
    print("{} {}. On {} site: {}".format(botname,count,site_name,url))


def switch_to_tab1():
    driver.switch_to.window(driver.window_handles[0])
    print("{} {}. Back to Tab-1".format(botname,count))


def switch_to_tab2():
    driver.switch_to.window(driver.window_handles[1])
    print("{} {}. On Tab-2: {}".format(botname,count, driver.current_url))

def close_tab():
    driver.close()
    print("{} {}. Tab closed!".format(botname, count))


def btn_tp_enroll_now():
    #using class name
    tp_enroll_btn = driver.find_element_by_class_name("rh_button_wrapper")
    return  tp_enroll_btn

def btn_go_to_course():
    #using xpath find btn text - Go to Course
    u_go_to_course_btn = driver.find_element_by_xpath("//*[text()='Go to course']")
    return u_go_to_course_btn

def btn_buy_now():
    #using xpath find btn text - Buy Now
    u_buy_now_btn = driver.find_element_by_xpath("//*[text()='Buy now']")
    return u_buy_now_btn

def btn_enroll_now():
    #using xpath find btn text - Enroll Now
    u_enroll_now_btn = driver.find_element_by_xpath("//*[text()='Enroll now']")
    return u_enroll_now_btn








email = "ADD YOUR EMAIL ID HERE"
password = "ADD YOUR PASSWORD HERE"
browser_path = "chromedriver.exe"
botname = "[Runal's Udemy Bot]"
count = 0
t_sec = 4
error_url_li = []
en_url_li =[]


# ----- Bot Starts ------

title()

#All course links of TP site are stored in the List -- tp_course_link_list
tb_course_link_list = find_course_links("New_Course_links.txt")


print("{} Opening Chrome....".format(botname))
open_chrome_browser(browser_path)
udemy_login()


for tb_course_url in tb_course_link_list:
    print()
    count = count + 1
    open_site("TB",tb_course_url)
    wait()
    btn_tp_enroll_now().click()
    print("{} {}. Switching to udmey site....".format(botname, count))
    wait()
    switch_to_tab2()
    wait()

    print("{} {}. Checking Course details....".format(botname, count))
    try:
        btn_enroll_now().click()
        print("{} {}. Enrolling....".format(botname, count))
        wait()

        print("{} {}. Selecting state....".format(botname, count))
        u_state_select_btn = driver.find_element_by_id("billingAddressSecondarySelect")
        u_state_select_btn.click()
        time.sleep(2)
        u_state_mh_btn = driver.find_element_by_xpath("//*[text()='Maharashtra']")
        u_state_mh_btn.click()
        print("{} {}. Selected - Maharashtra".format(botname, count))
        wait()
    
        #using xpath find btn - last Enroll Now btn
        xpath_u_final_en_btn = "/html/body/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button"
        uf_enroll_now_btn = driver.find_element_by_xpath(xpath_u_final_en_btn)
        uf_enroll_now_btn.click()
        wait()
        print("{} {}. --- Enrolled!  ---".format(botname, count))

        en_url = driver.current_url
        en_url_li.append(en_url)
  

    except:
        try:
            btn_go_to_course()
            print("{} {}. --- Already Enrolled! [ Go to course ] ---".format(botname, count))

        except:
            try:
                btn_buy_now()
                print("{} {}. --- Oops! [ Buy Now ] ---".format(botname, count))

            except:
                print("********* Error! *********")
                url = driver.current_url
                error_url_li.append(url)



    wait()
    close_tab()
    switch_to_tab1()


print("\n*** Error urls: ***")
if len(error_url_li) > 0:
    for x in error_url_li:
        print(x)
else:
    print("0")

print()

print("\n*** Enrolled urls: ***")
if len(en_url_li) > 0:
    for x in en_url_li:
        print(x)
else:
    print("0")
