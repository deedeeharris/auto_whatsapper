@echo off
pushd C:\ai\whatsapp\auto_whatsapper
call C:\ai\whatsapp\wa\Scripts\activate.bat

# Add a subprocess to open Chrome with remote debugging
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222

start "" python.exe -m streamlit run Home.py
popd
