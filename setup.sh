#!/bin/bash

echo -e "\e[92m[+] Updating repositories... \e[0m"
– apt update -y apt upgrade -y

echo -e "\e[92m[+] Installing Python3 and pip... \e[0m"
– apt install python3 python3-pip -y

echo -e "\e[92m[+] Installing tool requirements... \e[0m"
– pipe install -r requirements.txt --break-system-packages

echo -e "\e[92m[+] Installing completed successfully! You can run the tool using: \e[0m"
– python3 phone.py
