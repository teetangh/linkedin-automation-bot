# LinkedIn Connection Automation bot for Ubuntu 18.04
import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

LINKEDIN_USERNAME = os.getenv('LINKEDIN_USERNAME')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')

print(LINKEDIN_USERNAME)
print(LINKEDIN_PASSWORD)

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(
    "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
time.sleep(2)

# ************************* Login *************************

username = driver.find_element_by_xpath("//*[@id='username']")
password = driver.find_element_by_xpath("//*[@id='password']")

username.send_keys(LINKEDIN_USERNAME)
password.send_keys(LINKEDIN_PASSWORD)

time.sleep(2)

submit = driver.find_element_by_xpath("//button[@type='submit']")
submit.click()

# ************************* Connections *************************

# FAANG Meta Facebook Google Amazon Netflix Microsoft Apple
# DoorDash Roblox Stripe Twich Instacart Uber Lyft Twitter Linked In
# Pinetrest Bloomberg Robinhood Box Two Sigma Byte Dance Tik Tok
# Air Bnb Nuro Ui Path Oracle Data Bricks Waymo Dropbox Coinbase Snap
# Nvdia Reddit Splunk Coursera Square Mozilla Yelp Ebay Affirm Github
# Wish Etsy Shopify AMD IBM

applications = [
    # {
    #     "companyName": "Gojek",
    #     "jobPosition": "linkedin.com/jobs/view/3279191880",
    #     "connection_requests_limit": 5
    # },
    # {
    #     "companyName": "Citi",
    #     "jobPosition": "Java Developer",
    #     "connection_requests_limit": 10
    # },
    {
        "companyName": "Razorpay",
        "jobPosition": "Software Engineer - 6484",
        "connection_requests_limit": 12
    },
    # {
    #     "companyName": "Synopsys",
    #     "jobPosition": "Software Engineer 1",
    #     "connection_requests_limit": 10
    # }
]

for application in applications:
    try:
        print("Application: " +
              application["companyName"] + " - " + application["jobPosition"])

        driver.get("https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22us%3A0%22%5D&keywords=" +
                   application["companyName"] + "&origin=FACETED_SEARCH")
        time.sleep(2)

        page = 1
        connection_requests_sent = 0
        company_comleted = False

        while connection_requests_sent < application["connection_requests_limit"] and not company_comleted:
            all_buttons = driver.find_elements_by_tag_name("button")

            for button in all_buttons:
                print(button.text)

            # For the connect button.
            # For the follow buttons, open the person's profile in a new tab, and click the more->connect button.
            # Once the connect button is clicked, click on "Add a note" and type "Hello, I am interested in your profile." and click "Send".

            connect_buttons = [
                btn for btn in all_buttons if btn.text == "Connect"]
            follow_buttons = [
                btn for btn in all_buttons if btn.text == "Follow"]
            message_buttons = [
                btn for btn in all_buttons if btn.text == "Message"]

            for connect_button in connect_buttons:
                # btn.click() # this wont work because this is interrupted
                driver.execute_script("arguments[0].click();", connect_button)
                time.sleep(2)

                # Click on "Add a note" and type "Hello, I am interested in your profile." and click "Send".
                # If the "Add a note" button is not present, then click on "We don't know each other" and click "Connect".
                try:

                    we_dont_know_each_other = driver.find_element_by_xpath(
                        "//button[@aria-label='We don't know each other']")
                    # make aria-checked="true"
                    driver.execute_script(
                        "arguments[0].setAttribute('aria-checked', 'true')", we_dont_know_each_other)

                    connect_button = driver.find_element_by_xpath(
                        "//button[@aria-label='Connect']")
                    driver.execute_script(
                        "arguments[0].click();", connect_button)

                    connect_button2 = driver.find_element_by_xpath(
                        "//button[@aria-label='Connect']")
                    driver.execute_script(
                        "arguments[0].click();", connect_button2)

                    time.sleep(2)

                except:
                    time.sleep(0.1)

                finally:
                    add_note = driver.find_element_by_xpath(
                        "//button[@aria-label='Add a note']")

                    # person name is "Aditya Sharma"
                    peron_name = driver.find_element_by_xpath(
                        "//span[@class='flex-1']").text
                    # You can add a note to personalize your invitation to Aditya Sharma.
                    peron_name = peron_name.replace(
                        "You can add a note to personalize your invitation to ", "")
                    print("Sending Request to ", peron_name,
                          "Connection Requests Sent: ", connection_requests_sent + 1, " / ", application["connection_requests_limit"])
                    first_name = peron_name.split(" ")[0]
                    driver.execute_script("arguments[0].click();", add_note)
                    time.sleep(2)

                # Type "Hello, I am interested in your profile." and click "Send".
                message = driver.find_element_by_xpath(
                    "//textarea[@id='custom-message']")

                message.send_keys("Hey {first_name},\n I am Kaustav and I am looking for an FTE position at {companyName}. Could you please refer me for this position? I have previously interned at Samsung, Bangalore as an SDE intern and as a PRISM scholar, and at Hevo Data as an SDE intern.\nJob: {jobPosition}".format(
                    first_name=first_name, companyName=application["companyName"], jobPosition=application["jobPosition"]))

                send_now = driver.find_element_by_xpath(
                    "//button[@aria-label='Send now']")
                time.sleep(10)
                driver.execute_script("arguments[0].click();", send_now)
                time.sleep(2)

                connection_requests_sent += 1
                if connection_requests_sent >= application["connection_requests_limit"]:
                    company_comleted = True
                    print("Company completed `{companyName}`".format(
                        companyName=application["companyName"]))
                    break

            # Go to the next page.
            # If the next page is not found, then break.
            # https://www.linkedin.com/search/results/people/?keywords=coinswitch&page=2
            if not company_comleted:
                page += 1
                next_page = driver.get("https://www.linkedin.com/search/results/people/?keywords=" +
                                       application["companyName"] + "&page=" + str(page))
                time.sleep(2)
    except Exception as e:
        print(e)
        continue

# Close the browser.
driver.close()
print("Done with all applications.")
