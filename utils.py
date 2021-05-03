# ATENÇÃO: Esse código foi produzido pela MaestroTECH Software e liberado com
# licença MIT.

import os

from time import sleep
from random import choice
from string import ascii_letters, digits

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert

global driver
driver = None
global default_timeout
default_timeout = 5


alphanumeric = ascii_letters + digits

def startup(url):
    global driver
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def random_string(prefix='Test', length=10):
    return prefix + '-' + choice(ascii_letters) + ''.join(choice(alphanumeric) for i in range(length-1))

def wait_spinner():
    sleep(0.11) # Enough time for the spinner to show up.
    WebDriverWait(driver, default_timeout).until(EC.invisibility_of_element_located((By.ID, 'spinner')))

def wait_for_element(elementId, timeout=default_timeout):
    WebDriverWait(driver, default_timeout).until(EC.presence_of_element_located((By.ID, elementId)))

def wait_for_element_by_name(elementName, timeout=default_timeout):
    WebDriverWait(driver, default_timeout).until(EC.presence_of_element_located((By.NAME, elementName)))

def wait_and_click(elementId, timeout=default_timeout):
    wait_for_element(elementId, default_timeout)
    driver.find_element_by_id(elementId).click()

def wait_for_name_and_click(elementName, timeout=default_timeout):
    wait_for_element_by_name(elementName, timeout)
    driver.find_element_by_name(elementName).click()

def wait_for_xpath_and_click(elementId, elementXPath, timeout=default_timeout):
    # Click on System tab
    wait_for_element(elementId, timeout)
    # Click on System tab
    driver.find_element_by_xpath(elementXPath).click()

def scroll_and_click_byId(elementId):
    element = driver.find_element_by_id(elementId)
    scroll_and_click(element)

def scroll_and_click(element):
    actions = ActionChains(driver)
    actions.move_to_element(element)
    sleep(1)
    actions.click(element).perform()

# Select an option from a given 'select_id' element. Please add 'selectId' property to use this method
def choose_from_select(select_id, select_option):
    select_option_id = select_id + '_' + select_option.replace(" ", "_")

    scroll_and_click(driver.find_element_by_id(select_id))
    WebDriverWait(driver, default_timeout).until(EC.presence_of_element_located((By.ID, 'menu-')))
    WebDriverWait(driver, default_timeout).until(EC.presence_of_element_located((By.ID, select_option_id)))
    scroll_and_click(driver.find_element_by_id(select_option_id))
    WebDriverWait(driver, default_timeout).until(EC.invisibility_of_element_located((By.ID, 'menu-')))
    WebDriverWait(driver, default_timeout).until(EC.invisibility_of_element_located((By.ID, select_option_id)))

def choose_first_from_select(selectId, timeout=default_timeout, skipNotFound=False, sleepAfter=False):
    try:
        choose_from_select_by_index(selectId, 1, timeout)
        if (sleepAfter):
            sleep(default_timeout)
    except:
        if (skipNotFound):
            print(selectId + " not found in the form. Skipping")
        else:
            raise Exception(selectId + ' not found')

def choose_from_select_by_index(selectId, index, timeout=default_timeout):
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, selectId)))
        SelectElement = Select(driver.find_element_by_id(selectId))
        SelectElement.select_by_index(index)


def choose_from_modal_table(dialogId, itemText):
    WebDriverWait(driver, default_timeout).until(EC.presence_of_element_located((By.ID, 'table_' + dialogId)))
    # Click on an element that contains text
    fill_text_field(dialogId + '_search', itemText)
    wait_and_click('button_'+ dialogId +'_search')
    sleep(default_timeout / 2)
    scroll_and_click(driver.find_element_by_xpath(f"//td[contains(text(),'{itemText}')]"))

def choose_from_radio_buttom(radio_group_id, radio_value):
    radio_option_id = radio_group_id + '_' + radio_value.replace(" ", "_")
    scroll_and_click(driver.find_element_by_id(radio_option_id))

def fill_text_field(fieldId, text):
    driver.find_element_by_id(fieldId).send_keys(text)

def fill_text_field_and_enter(fieldId, text):
    driver.find_element_by_id(fieldId).send_keys(text, Keys.ENTER)

def fill_text_field_random(fieldId, prefix='Test', length=10):
    randomText = random_string(prefix, length)
    fill_text_field(fieldId, randomText)
    return randomText

def fill_text_field_phone(fieldId, phone='555-123456'):
    fill_text_field(fieldId, phone)

def fill_text_field_email(fieldId, email='contato@maestrotechsoft.com'):
    fill_text_field(fieldId, email)

def alert_confirm():
    sleep(1)
    alert = Alert(driver)

    # Click OK alert to confirm
    print("Confirm alert: " + alert.text)
    driver.switch_to.alert.accept()

def wait_and_click_util_empty(elementId, i=1, maxI=1000):
    try:
        if (i > maxI) :
            print ("Max I: " + i)
            return
        wait_and_click(elementId)
        i = i + 1
        wait_and_click_util_empty(elementId, i=i, maxI=maxI)
    except:
        print("No more elements after: " + str(i))

def click(elementId):
    driver.find_element_by_id(elementId).click()

def menu_navigation(navbar, side_menu, side_menu_item):
    wait_and_click('navlink_' + navbar)
    sleep(1) # wait to be visible
    wait_and_click('sidemenu_' + side_menu)
    sleep(1) # wait to be visible
    try:
        wait_and_click('sidemenu_item_' + side_menu_item)
    except:
        wait_and_click('sidemenu_' + side_menu)
        sleep(1) # wait to be visible
        wait_and_click('sidemenu_item_' + side_menu_item)

def save_form_and_check_for(elementId):
    click('button_Save')
    wait_for_element(elementId)

def fill_date_field(elementId):
    # Select datepicker object
    wait_for_element(elementId)
    datePicker = driver.find_element_by_id(elementId)
    datePicker.find_element_by_class_name('react-datetime-picker__calendar-button__icon').click()
    sleep(1)
    datePickerCalendar = datePicker.find_element_by_class_name('react-calendar__viewContainer')
    datePickerCalendar.find_element_by_class_name('react-calendar__month-view__days__day').click()

def fill_file_upload_field(elementId):
    fill_text_field(elementId, os.getcwd() + '/SAM/Resources/Logo.png')
