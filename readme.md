# Auto WhatApper

Auto WhatApper is a Python script that automates the process of sending WhatsApp messages to multiple recipients, either phone numbers or contacts/groups. It utilizes the Playwright library to interact with the WhatsApp Web interface.

## Prerequisites

- Python 3.x
- Playwright library
- Google Chrome

## Installation

1. Install Python 3.x from [python.org](https://www.python.org/).
2. Install the required Python packages using the following command:

    ```bash
    pip install -r requirements.txt
    ```

3. Make sure Google Chrome is installed on your system.

## Usage

### 1. Setup

- Start a WhatsApp Web session by scanning the QR code on the [WhatsApp Web](https://web.whatsapp.com/) page.
- Open Google Chrome with remote debugging enabled:

    ```bash
    "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
    ```

### 2. Running the Script

- To send messages to phone numbers:

    ```bash
    python send_msgs.py numbers
    ```

- To send messages to contacts/groups:

    ```bash
    python send_msgs.py contacts
    ```

### 3. Customizing Messages

- Customize your messages by editing the `data/message.txt` file.

### 4. Input Data

- Phone numbers are read from the `data/numbers.xlsx` file.
- Contacts/groups names are read from the `data/contacts.xlsx` file.

## Logging

- Message delivery status is logged in the `log.log` file.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

**By [Yedidya Harris](https://www.linkedin.com/in/yedidyaharris/)**
