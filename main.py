import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from twilio.rest import Client

# Constants
URL = 'https://www.cowin.gov.in/home'
ELEMENT_XPATH = '/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div' \
                '/div/div[2]/form '
account_sid = 'AC4effe82a63150e1840bce6f0c50caa28'
auth_token = '7ecfef9e143d6569145263309eb6da02'
phno = 'whatsapp:+14155238886'
client = Client(account_sid, auth_token)


def main(pin, ct):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('/Users/rajanjaiswal/Downloads/chromedriver')
    driver.get(URL)
    info = f"*Covid Vaccine Availability in {pin}*\n\n"
    age_group = "Age 18+"
    count = 0
    try:
        driver.find_element_by_id("mat-input-0").send_keys(pin)
        driver.find_element_by_class_name("pin-search-btn").click()
        time.sleep(2)
        locations = driver.find_elements_by_class_name("center-name-title")
        status = driver.find_elements_by_class_name("slots-box")
        dates = driver.find_elements_by_class_name("availability-date")

        for index, location in enumerate(locations):
            for i in range(7):
                slots = status[i + index * 7].text.split("\n")[0].strip()
                if slots != "NA" and slots != "Booked":
                    agelimit = status[i + index *
                                      7].text.split("\n")[2].strip()
                    if agelimit == age_group:
                        vaccine = status[i + index * 7].text.split("\n")[1].strip()
                        date = dates[i].text
                        count = count + 1
                        info = info + f'Location - {location.text}\nSlots - *{slots}*\nVaccine - {vaccine}\nAge group - 18+\nDate - {date}\n\n'
    except TimeoutException:
        print("Could not find the desired element")
    finally:
        driver.quit()

    info = info + 'Book your slots now - https://selfregistration.cowin.gov.in/'
    if count != 0 and cached_message != info:
        message = client.messages.create(
            body=info, from_=phno, to=f'whatsapp:{ct}')
        print(f'message sent, sid = {message.sid}')
    return info


if __name__ == '__main__':
    print("Hi! I'm C-Bot. I will be your assistant for searching nearby Covid Vaccination Medial Facilities. I'll "
          "inform you when slots are available in your area. - RJ\nPlease enter your area PINCODE")
    pincode = input('>')
    print("Enter your Whatsapp number including country code without any spaces")
    contact = input('>')
    print(
        f"Now send a Whatsapp message \'join curve-bread\' from your number to {phno} and then press enter...")
    input()
    print("You're done. You will receive Whatsapp notifications when vaccine is available in your area")
    global cached_message
    cached_message = ''
    while True:
        cached_message = main(pincode, contact)
        time.sleep(10)
