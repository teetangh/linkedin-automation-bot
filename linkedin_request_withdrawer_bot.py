# LinkedIn Connection Withdrawal Automation bot for Ubuntu 18.04
import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

LINKEDIN_USERNAME = os.getenv('LINKEDIN_USERNAME')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')

# print(LINKEDIN_USERNAME)
# print(LINKEDIN_PASSWORD)

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(
    "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
time.sleep(2)

# ************************* Login *************************

username = driver.find_element_by_xpath("//*[@id='username']")
password = driver.find_element_by_xpath("//*[@id='password']")

username.send_keys(LINKEDIN_USERNAME)
password.send_keys(LINKEDIN_PASSWORD)

time.sleep(1)

submit = driver.find_element_by_xpath("//button[@type='submit']")
submit.click()

# Go to the pending connection requests page
driver.get(
    "https://www.linkedin.com/mynetwork/invitation-manager/sent/")

# Find the last page number
last_page_number = driver.find_element_by_xpath(
    "//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']/li[last()]").text

print(last_page_number)
# Reverse iterate over the pages from last_page_number to 1
for page_number in range(int(last_page_number), 0, -1):
    try:
        driver.get(
            "https://www.linkedin.com/mynetwork/invitation-manager/sent/?filterCriteria=&invitationType=&page={}".format(page_number))

        all_buttons = driver.find_elements_by_tag_name("button")

        withdraw_buttons = [
            btn for btn in all_buttons if btn.text == "Withdraw"]

        # Reverse iterate over the withdraw buttons
        for withdraw_button in reversed(withdraw_buttons):
            try:
                driver.execute_script("arguments[0].click();", withdraw_button)
                time.sleep(0.1)

                confirmation_buttons = driver.find_elements_by_tag_name(
                    "button")

                for confirmation_button in confirmation_buttons:
                    if confirmation_button.text == "Withdraw":
                        driver.execute_script(
                            "arguments[0].click();", confirmation_button)
                    time.sleep(0.1)
            except Exception as e:
                print(e)
                continue

    except Exception as e:
        print(e)
        continue
driver.quit()
