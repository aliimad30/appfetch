SCRIPT_VERSION = "1.1.0"

import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import smtplib

def run_selenium_script():
    while True:  # Loop to run the script every 60 minutes
        try:
            # Initialize WebDriver
            service = webdriver.ChromeService(executable_path='/usr/bin/chromedriver')
            driver = webdriver.Chrome(service=service)

            # Navigate to the website
            driver.get('https://nqa3.nemoqappointment.com/Booking/Booking/Index/vh356kg3s6')

            # Wait for the page to load
            time.sleep(2)

            # Selenium actions
            booking_number_field = driver.find_element(By.ID, "BookingNumber")
            booking_number_field.send_keys("1541422089")

            contact_info_field = driver.find_element(By.ID, "ContactInfo")
            contact_info_field.send_keys("4694411128")

            edit_appointment_button = driver.find_element(By.XPATH, "//input[@value='Edit appointment']")
            edit_appointment_button.click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@value='Edit']"))
            )

            edit_button = driver.find_element(By.XPATH, "//input[@value='Edit']")
            edit_button.click()

            this_week_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "thisweek"))
            )

            this_week_link.click()

            time.sleep(2)

            time_search_first_available_button = driver.find_element(By.XPATH, "//input[@value='First available time']")
            time_search_first_available_button.click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@data-function, 'timeTableCell')]"))
            )

            first_time_cell = driver.find_element(By.XPATH, "//*[contains(@data-function, 'timeTableCell')]")
            aria_label_value = first_time_cell.get_attribute('aria-label')

            retrieved_date = datetime.datetime.strptime(aria_label_value, '%m/%d/%Y %I:%M:%S %p').date()
            comparison_date = datetime.date(2024, 1, 9)

            if retrieved_date < comparison_date:
                print(f'An Earlier Appointment Exists on {retrieved_date}')
                sender = 'filamaworldlive@gmail.com'
                password = 'hpkqoljarzssbduj'
                recipient = '4694411128@tmomail.net'

                smtp_server = 'smtp.gmail.com'
                smtp_port = 587

                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender, password)
                msg = f'An Earlier Appointment, {retrieved_date}, is Available.'
                headers = f"Subject: {msg}\r\n"
                
                server.sendmail(sender, recipient, headers)
                server.quit()
                print('Message sent')
            else:
                print('No Earlier Appointment Exists')
        except Exception as e:
            print("An error occurred:", e)
        finally:
            driver.quit()
            print("WebDriver quit successfully")

        # Wait for 60 minutes before the next run
        print("Waiting for 60 minutes before the next run.")
        time.sleep(3600)

# Start the script
run_selenium_script()