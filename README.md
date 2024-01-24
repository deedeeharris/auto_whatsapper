# Auto WhatsApper

Auto WhatApper is a Streamlit web app that automates the process of sending WhatsApp messages to multiple recipients, either phone numbers or contacts/groups. It utilizes the Playwright library to interact with the WhatsApp Web interface.

## Prerequisites

- Python 3.12.x
- Streamlit
- Playwright library
- Google Chrome
- Microsoft Office Excel

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/deedeeharris/auto_whatsapper.git
    ```

2. Navigate to the cloned repository:

    ```bash
    cd auto_whatsapper
    ```

3. Edit the `.env` file and set the `root_path` variable to the parent folder where you cloned this repository. For example:

    ```ini
    # .env

    root_path=/path/to/parent/folder
    ```
4. Create a virtual env in the root_path folder, and activate it. For example:
    
        
        cd /path/to/parent/folder
        python -m venv wa
        .\wa\Scripts\activate
        

5. Install the required Python packages using the following command:

    ```bash
    pip install -r requirements.txt
    ```

6. Install Playwright using the following command:

    ```bash
    playwright install
    ```

   This will download the necessary browser binaries.

7. Edit the bat file in the root_path folder, and update the root path accordingly.

8. In addition, make sure the your default chrome.exe path in the bat file is correct (this script will control your chrome browser, and not a standard chrome driver).

## Usage

1. Initiate a WhatsApp Web session by scanning the QR code on the [WhatsApp Web](https://web.whatsapp.com/) page, ensuring that it remains logged into your Chrome profile.

2. Close all open Chrome windows.

3. On Windows, open the .bat file in the root_path folder. This will open a new Chrome window (in debug mode) and start a Streamlit server.

4. Use the Streamlit app interface to send messages to phone numbers or contacts/groups. The app will automatically open the relevant Excel files.

### Customizing Messages

- You can enter the text of the message within the app (click the "Open txt message" button to open the message.txt file), which updates the data/message.txt file.

### Input Data

- Phone numbers are sourced from the data/numbers.xlsx file, whether they exist in your contacts or not.
- Contacts and group names are retrieved from the data/contacts.xlsx file, encompassing both saved contacts and groups of which you are a member.

## Logging

- Message delivery status is logged in the `log.log` file.

## Warning

- This app is for educational purposes only. Please use it responsibly and at your own risk.
- It is not recommended to use this app to send messages to large numbers of recipients, as this may result in your phone number being blocked by WhatsApp.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

----

**By [Yedidya Harris](https://www.linkedin.com/in/yedidya-harris/)**
