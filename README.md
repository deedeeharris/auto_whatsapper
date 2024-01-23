# Auto WhatApper

Auto WhatApper is a Streamlit web app that automates the process of sending WhatsApp messages to multiple recipients, either phone numbers or contacts/groups. It utilizes the Playwright library to interact with the WhatsApp Web interface.

## Prerequisites

- Python 3.12.x
- Streamlit
- Playwright library
- Google Chrome
- Microsoft Office Excel

## Installation

1. Install the required Python packages using the following command:

    ```bash
    pip install -r requirements.txt
    ```

2. Install Playwright using the following command:

    ```bash
    playwright install
    ```
 
   This will download the necessary browser binaries.

## Usage

1. Start a WhatsApp Web session by scanning the QR code on the [WhatsApp Web](https://web.whatsapp.com/) page.

2. Open Google Chrome with remote debugging enabled:

    ```bash
    "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
    ```

3. Run the Streamlit app:

    ```bash
    streamlit run Home.py
    ```

4. Access the app in your browser by visiting http://localhost:8501.

5. Use the Streamlit app interface to send messages to phone numbers or contacts/groups. The app will automatically open the relevant Excel files.

### Customizing Messages

- You can enter the text of the message within the app or by editing the `data/message.txt` file.

### Input Data

- Phone numbers are sourced from the data/numbers.xlsx file, whether they exist in your contacts or not.
- Contacts and group names are retrieved from the data/contacts.xlsx file, encompassing both saved contacts and groups of which you are a member.

## Logging

- Message delivery status is logged in the `log.log` file.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

**By [Yedidya Harris](https://www.linkedin.com/in/yedidyaharris/)**
