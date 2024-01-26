# send_msgs.py is the script that sends the messages.

from playwright.sync_api import sync_playwright
import subprocess
import sys
import logging
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
import pyperclip

# get root path from .env file
load_dotenv()
root_path = os.getenv("root_path")

# subprocess to open Chrome with remote debugging (commented - since it opens in the bat file)
# subprocess.Popen([
#     "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
#     "--remote-debugging-port=9222"
# ])
logging.basicConfig(filename='log.log', level=logging.INFO, encoding='utf-8')


# y harris
# function to send a single message to a single phone number
def send_to_one_number(page, phone_number, message):
    page.wait_for_timeout(3000)

    # check for the lang of whatsapp web
    html = page.content()
    if 'lang="en"' in html: lang='english'
    if 'lang="he"' in html: lang='hebrew'

    # click the new chat button
    if lang == 'english': chat_title = 'New chat'
    if lang == 'hebrew': chat_title = 'צ\'אט חדש'
    new_chat_selector = f'div[title="{chat_title}"]'
    page.click(new_chat_selector)
    page.wait_for_timeout(1000)

    # click on the search box and type the phone number
    if lang == 'english': term_to_search = "Search input textbox"
    if lang == 'hebrew': term_to_search = "תיבת טקסט להזנת החיפוש"
    search_box_selector = f'div[title="{term_to_search}"]'
    page.click(search_box_selector)
    page.type(search_box_selector, phone_number)
    page.wait_for_timeout(3000)

    # after typing, just press enter
    page.keyboard.press('Enter')
    page.wait_for_timeout(1000)

    # check if the phone number is saved as a contact, in the html code there will be "No results found for"
    # look in the html source code for "No results found for"
    term_to_search_en = "No results found for"
    term_to_search_heb = "לא נמצאו תוצאות"
    # get html code
    html = page.inner_html('body')
    # check if the term is in the html code
    if term_to_search_en in html or term_to_search_heb in html:
        print('No results found for this phone numsber')
        page.wait_for_timeout(1000)
        page.keyboard.press('Escape')
        return False
        

    # click on the message box and type the message
    if lang == 'english': msg_box_title = 'Type a message'
    if lang == 'hebrew': msg_box_title = 'הקלדת הודעה'

    msg_box_selector = f'div[title="{msg_box_title}"]'
    page.wait_for_selector(msg_box_selector)
    page.click(msg_box_selector)


    # # Replace line breaks with Shift+Enter
    # lines = message.split('\n')
    # for line in lines:
    #     page.type(msg_box_selector, line)
    #     page.keyboard.down('Shift')
    #     page.keyboard.press('Enter')
    #     page.keyboard.up('Shift')

    # Set the clipboard content to the original message
    pyperclip.copy(message)
    # Focus on the message input box
    page.click(msg_box_selector)
    # Paste the message from the clipboard
    page.keyboard.down('Control')
    page.keyboard.press('V')
    page.keyboard.up('Control')

    page.keyboard.press('Enter') # send the message

    # send_button_selector = 'button[data-tab="11"]' 
    # page.wait_for_selector(send_button_selector)
    # page.click(send_button_selector) # click on send button
    
    page.wait_for_timeout(3000)
    return True


# function to send a single message to a single phone number
def send_to_one_contact(page, contact, message, strip_and_try, contact_info):
    print("Strip and try is ",strip_and_try)
    # check for the lang of whatsapp web
    html = page.content()
    if 'lang="en"' in html: lang='english'
    if 'lang="he"' in html: lang='hebrew'

    # click on the search box and type the phone number
    if lang == 'english': term_to_search = "Search input textbox"
    if lang == 'hebrew': term_to_search = "תיבת טקסט להזנת החיפוש"
    search_box_selector = f'div[title="{term_to_search}"]' # or "תיבת טקסט להזנת החיפוש"
    page.click(search_box_selector)
    page.type(search_box_selector, contact)
    page.wait_for_timeout(3000)



    result_row = {'contact_name': contact, 'Success': False, 'contact_name_stripped': None, 'timestamp': None}
    result_selector = f'span[title="{contact}"]'
    try:
        page.wait_for_selector(result_selector, timeout=3000)
        page.click(result_selector)
        result_row['Success'] = True
        result_row['timestamp'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    except:
        if strip_and_try and ' ' in contact:
            print(f'Timeout: Selector "{result_selector}" not found within 3 seconds. Trying to strip the contact name and try again.')
            stripped_contact = contact.replace(" ", "")
            result_selector_stripped = f'span[title="{stripped_contact}"]'
            result_row['contact_name_stripped'] = stripped_contact
            result_row['timestamp'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            try:
                page.keyboard.press('Escape')
                page.click(search_box_selector)
                page.type(search_box_selector, stripped_contact)
                page.wait_for_selector(result_selector_stripped, timeout=3000)
                page.click(result_selector_stripped)
                result_row['Success'] = True
               
            except:
                print(f'Timeout: Selector "{result_selector_stripped}" not found within 3 seconds.')
                page.keyboard.press('Escape')
                contact_info = pd.concat([contact_info, pd.DataFrame(result_row, index=[0])], ignore_index=True)
                return result_row['Success'], contact_info
        else:
            print(f'Timeout: Selector "{result_selector}" not found. Continuing to next contact.')
            page.keyboard.press('Escape')
            
            result_row['timestamp'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            contact_info = pd.concat([contact_info, pd.DataFrame(result_row, index=[0])], ignore_index=True)
            return result_row['Success'], contact_info



    # term_to_search_en = "No results found for"
    # term_to_search_heb = "לא נמצאו"
    # # get html code
    # html = page.inner_html('body')
    # # check if the term is in the html code
    # if term_to_search_en in html or term_to_search_heb in html:
    #     print('No results found for this phone numsber')
    #     page.wait_for_timeout(1000)
    #     page.keyboard.press('Escape')
    #     return False

    # click on the message box and type the message
    if lang == 'english': msg_box_title = 'Type a message'
    if lang == 'hebrew': msg_box_title = 'הקלדת הודעה'
    msg_box_selector = f'div[title="{msg_box_title}"]'
    page.wait_for_selector(msg_box_selector)
    page.click(msg_box_selector)

    # # Replace line breaks with Shift+Enter
    # lines = message.split('\n')
    # for line in lines:
    #     page.type(msg_box_selector, line)
    #     page.keyboard.down('Shift')
    #     page.keyboard.press('Enter')
    #     page.keyboard.up('Shift')

    # Set the clipboard content to the original message
    pyperclip.copy(message)
    # Focus on the message input box
    page.click(msg_box_selector)
    # Paste the message from the clipboard
    page.keyboard.down('Control')
    page.keyboard.press('V')
    page.keyboard.up('Control')


    page.keyboard.press('Enter') # send the message

    # send_button_selector = 'button[data-tab="11"]' 
    # page.wait_for_selector(send_button_selector)
    # page.click(send_button_selector) # click on send button

    # Wait for the #main element to be available
    page.wait_for_selector('#main')

    # Get the inner HTML of the #main element
    messages = page.query_selector_all('.selectable-text.copyable-text')


    # Save the entire parent including itself to HTML
    for message in messages:
        # Get the parent element
        parent_element = message.evaluate('(element) => element.parentElement.outerHTML')

        # Save the parent element to an HTML file
        with open(f'message_{messages.index(message) + 1}.html', 'w', encoding='utf-8') as file:
            file.write(parent_element)

    page.wait_for_timeout(3000)

    contact_info = pd.concat([contact_info, pd.DataFrame(result_row, index=[0])], ignore_index=True)
    return result_row['Success'], contact_info


# Start a new session with Playwright using the sync_playwright function.
with sync_playwright() as playwright:
    # Connect to an existing instance of Chrome using the connect_over_cdp method.
    browser = playwright.chromium.connect_over_cdp("http://localhost:9222")

    # Retrieve the first context of the browser.
    default_context = browser.contexts[0]

    # Retrieve the first page in the context.
    page = default_context.pages[0]

    page.goto("https://web.whatsapp.com/")

    # read in phone numbers from xlsx file
    df_numbers = pd.read_excel(rf'data\numbers.xlsx')
    phone_numbers = df_numbers['numbers'].tolist()

    # read in contacts and groups names from xlsx file
    df_contacts = pd.read_excel(rf'data\contacts.xlsx')
    contacts = df_contacts['contacts'].tolist()

    # first argument will be contacts or groups names, and seonc argument if provided will be the message
    if len(sys.argv) > 1:
        type_target = sys.argv[1]
    strip_and_try = False  # Default value
    if len(sys.argv) > 2:
        strip_and_try_str = sys.argv[2].lower()  # Convert to lowercase for case-insensitivity
        if strip_and_try_str == 'true':
            strip_and_try = True
    
    # read in msg from txt file
    with open(rf'data\message.txt', 'r', encoding='utf-8') as f:
        message = f.read()

    # create a dataframe to save the contact information
    contact_info = pd.DataFrame(columns=['contact_name', 'contact_name_stripped', 'timestamp', 'Success'])
    
    if type_target == 'contacts':
        # send message to all contacts, and log success and failure
        for contact in contacts:
            result, contact_info = send_to_one_contact(page, contact, message, strip_and_try, contact_info)
            if result:
                logging.info(f'Message sent successfully to {contact}')
            else:
                logging.info(f'Message failed to send to {contact}')

        
        # Save the contact information to an Excel file
        timestamp_str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        excel_filename = rf'data\runs\contacts_log_run_{timestamp_str}.xlsx'
        contact_info.to_excel(excel_filename, index=False)

        # Open the Excel file using subprocess
        subprocess.Popen(['start', rf'{root_path}\auto_whatsapper\{excel_filename}'], shell=True)

    elif type_target == 'numbers':
        # send message to all phone numbers, and log success and failure
        for phone_number in phone_numbers:
            phone_number = str(phone_number)
            print("Trying to send to ",phone_number)
            result = send_to_one_number(page, phone_number, message)
            if result:
                logging.info(f'Message sent successfully to {phone_number}')
            else:
                logging.info(f'Message failed to send to {phone_number}')



    