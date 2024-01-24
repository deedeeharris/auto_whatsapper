# send_msgs.py is the script that sends the messages.

from playwright.sync_api import sync_playwright
import subprocess
import sys
import logging
import pandas as pd

# subprocess to open Chrome with remote debugging (commented - since it opens in the bat file)
# subprocess.Popen([
#     "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
#     "--remote-debugging-port=9222"
# ])
logging.basicConfig(filename='log.log', level=logging.INFO)

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


    # Replace line breaks with Shift+Enter
    lines = message.split('\n')
    for line in lines:
        page.type(msg_box_selector, line)
        page.keyboard.down('Shift')
        page.keyboard.press('Enter')
        page.keyboard.up('Shift')

    page.keyboard.press('Enter') # send the message

    # send_button_selector = 'button[data-tab="11"]' 
    # page.wait_for_selector(send_button_selector)
    # page.click(send_button_selector) # click on send button
    
    page.wait_for_timeout(3000)
    return True


# function to send a single message to a single phone number
def send_to_one_contact(page, contact, message):
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

    result_selector = f'span[title="{contact}"]'
    try:
        page.wait_for_selector(result_selector, timeout=3000)
        page.click(result_selector)
    except:
        print(f'Timeout: Selector "{result_selector}" not found within 3 seconds.')
        page.keyboard.press('Escape')
        return False

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

    # Replace line breaks with Shift+Enter
    lines = message.split('\n')
    for line in lines:
        page.type(msg_box_selector, line)
        page.keyboard.down('Shift')
        page.keyboard.press('Enter')
        page.keyboard.up('Shift')


    page.keyboard.press('Enter') # send the message

    # send_button_selector = 'button[data-tab="11"]' 
    # page.wait_for_selector(send_button_selector)
    # page.click(send_button_selector) # click on send button

    page.wait_for_timeout(3000)
    return True


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
    if len(sys.argv) > 2:
        message = sys.argv[2]
    else:
        with open(rf'data\message.txt', 'r', encoding='utf-8') as f:
            message = f.read()
    
    if type_target == 'contacts':
        # send message to all contacts, and log success and failure
        for contact in contacts:
            result = send_to_one_contact(page, contact, message)
            if result:
                logging.info(f'Message sent successfully to {contact}')
            else:
                logging.info(f'Message failed to send to {contact}')

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



    