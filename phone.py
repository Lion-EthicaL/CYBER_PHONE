import os
import phonenumbers
import pycountry
import pytz
from datetime import datetime
from phonenumbers import geocoder, carrier, timezone, region_code_for_number, PhoneNumberType
from phonenumbers import number_type, PhoneNumberType

#=========Terminal Colors (ANSI Escape Codes)============
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def show_banner():
    #=========CLI ASCII Banner for the tool==============
    banner = rf"""
{GREEN}{BOLD}         ⠀        ⠀
                                    .------.
                                    |P.--. |
                                    | :/\: |
                                    | (🎭) |
                                    | '--'P|
                                    `------'
             .------.
             |E.--. |
             | :/\: |
             | (🎭) |
             | '--'E|
             `------'             ⣀⣀⣀⣀
                             ⠀⢀⣠⣴⣾⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀      ⠀         ⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀
⠀⠀.------.               ⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁
  |N.--. |             ⢀⣴⣿⣿⣿⣿⣿⠿⠋⠉⠉⠻⢿⡿⠟⠁
  | :/\: |            ⣴⣿⣿⣿⣿⣿⠟⠁
  | (🎭) |          ⢀⣾⣿⣿⣿⣿⠟⠁
  | '--'N|         ⢀⣾⣿⣿⣿⣿⠏⠀                .------.
  `------'         ⣾⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀             |H.--. |
                   ⣿⣿⣿⣿⣿⣿⣿⡷⠀               | :/\: |
                  ⠀⢿⣿⣿⣿⣿⣿⠟⠁                | (🎭) |
                    ⠙⢿⣿⠟⠁                  | '--'H|
                                           `------'⠀
⠀⠀            ⠀       ⠀  .------.
            ⠀            |O.--. |
                         | :/\: |
                         | (🎭) |
                         | '--'O|
                         `------'
  _______   __  __     ______     __   __     ______
 / \  == \ /\ \_\ \   /\  __ \   /\ '-.\ \   /\  ___\
  \ \  _-/ \ \  __ \  \ \ \/\ \  \ \ \--\ \  \ \  __\
   \ \_\    \ \_\ \_\  \ \_____\  \ \_\\'\_\  \ \_____\
    \/_/     \/_/\/_/   \/_____/   \/_/ \/_/   \/_____/

              {RESET}
{CYAN}>>>>>>>>>>>>>>>>Mini OSINT Phone Analyzer v1.0<<<<<<<<<<<<<{RESET}
{YELLOW}>>>>>>>>>>>>>>Created by Lion-EthicaL Developer<<<<<<<<<<<<{RESET}
    """
    print(banner)

def analyze_phone_number(phone_input):
    try:
        # ========Parse the input phone number=========
        parsed_number = phonenumbers.parse(phone_input, None)
        is_valid = phonenumbers.is_valid_number(parsed_number)

        if not is_valid:
            print(f"{RED}[❌] Error: The number is invalid or not in use.{RESET}")
            return

        print(f"\n{GREEN}[✅] Number analyzed successfully: {phone_input}{RESET}")
        print(f"{BLUE}" + "=" * 59 + f"{RESET}")


        # 1.===========Country / Location info=========
        r_code = region_code_for_number(parsed_number); base_country = geocoder.description_for_number(parsed_number, "en") or (pycountry.countries.get(alpha_2=r_code).name if r_code else "Global"); detailed_loc = geocoder.description_for_valid_number(parsed_number, "en"); num_type = number_type(parsed_number); type_str = "Mobile" if num_type == PhoneNumberType.MOBILE else "Fixed Line" if num_type == PhoneNumberType.FIXED_LINE else "VoIP" if num_type == PhoneNumberType.VOIP else "Premium Rate" if num_type == PhoneNumberType.PREMIUM_RATE else "Shared Cost" if num_type == PhoneNumberType.SHARED_COST else "Toll Free" if num_type == PhoneNumberType.TOLL_FREE else "Unknown Type"; full_location = f"{base_country} ({detailed_loc}) [{type_str}]" if detailed_loc and detailed_loc != base_country else f"{base_country} [{type_str}]"


        print(f"{CYAN}[•] Country/Location:{RESET} {BOLD}{full_location}{RESET}")


        # 2.========Carrier / Service Provider info=========
        service_provider = carrier.name_for_number(parsed_number, "en")
        if service_provider:
            print(f"{CYAN}[•] Carrier/Provider:{RESET} {BOLD}{service_provider}{RESET}")
        else:
            print(f"{CYAN}[•] Carrier/Provider:{RESET} {YELLOW}Unknown (Could be a landline){RESET}")


        # 3.============Timezone info================
        tz_list = timezone.time_zones_for_number(parsed_number)
        tz_info = "Unknown"
        if tz_list and list(tz_list)[0] != "Etc/Unknown":
            try:
                tz = pytz.timezone(list(tz_list)[0])
                now_there = datetime.now(tz)
                offset = now_there.strftime('%z')
                gmt_offset = f"GMT{offset[:3]}:{offset[3:]}"
                time_str = now_there.strftime('%I:%M %p')
                tz_info = f"{list(tz_list)[0]} ({gmt_offset}) | Local Time: {time_str}"
            except:
                tz_info = ", ".join(tz_list)

        print(f"{CYAN}[•] Timezone(s):{RESET} {BOLD}{tz_info}{RESET}")


        # 4.=======Standard International Format=========
        international_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        print(f"{CYAN}[•] International Format:{RESET} {GREEN}{international_format}{RESET}")
        print(f"{BLUE}" + "=" * 59 + f"{RESET}")
        # Prepare data packet and save it globally
        report_data = {"International Format": international_format, "Country/Location": full_location, "Carrier/Provider": service_provider or "Unknown", "Timezone & Local Time": tz_info}; save_report(phone_input, report_data)

    except Exception as e:
        print(f"{RED}[-] An error occurred during analysis: {e}{RESET}")


    # 5.=======Smart links to search for the number across leak platforms and search engines========
def google_dorking(phone_number):
    print(f"\n\033[93m[!] Generating Google Dorking Links for OSINT...\033[0m")
    print("\033[94m" + "=" * 50 + "\033[0m")
    clean_num = phone_number.replace(" ", "").replace("-", "")
    dorks = {
        "Global Search": f"https://google.com\"{clean_num}\"",
        "Social Networks (FB, IG, X)": f"https://google.comsite:facebook.com+OR+site:instagram.com+OR+site:twitter.com+\"{clean_num}\"",
        "Leak Sites & Pastebin": f"https://google.comsite:pastebin.com+OR+site:github.com+OR+site:gitlab.com+\"{clean_num}\"",
        "Phone Directories / Spam": f"https://google.comsite:tellows.com+OR+site:whocalledme.com+\"{clean_num}\""
    }
    for name, link in dorks.items():
        print(f"\033[96m[•] {name}:\033[0m\n    \033[4m{link}\033[0m\n")
    print("\033[94m" + "=" * 59 + "\033[0m")

    # 6.======This automatically creates a formatted text report named after the checked number======
def save_report(phone_number, data_dict):
    import os
    clean_num = phone_number.replace(" ", "").replace("-", "").replace("+", "")
    filename = f"report_{clean_num}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"=== OSINT PHONE REPORT FOR: {phone_number} ===\n")
            for key, value in data_dict.items():
                f.write(f"[•] {key}: {value}\n")
            f.write("=" * 59 + "\n")
        print(f"\033[92m[📝] OSINT Report saved successfully as: {filename}\033[0m")
    except Exception as e:
        print(f"\033[91m[-] Failed to save report: {e}\033[0m")

if __name__ == "__main__":
    while True:
        import os; os.system('clear' if os.name == 'posix' else 'cls'); show_banner()
        num = input("\033[1m[🔎]Enter phone number📞\033[92m(ex.,+112600000000):\033[0m").strip()
        if num.lower() in ['exit', 'quit'] or not num:
            print("\033[91m[!] Exiting Mini OSINT Tool. Goodbye!\033[0m"); break
        analyze_phone_number(num); google_dorking(num)
        input("\n\033[93mPress Enter to check another number or type 'exit' to quit...\033[0m")


    # 7.======This automatically triggers the Google Dorking search=========
    google_dorking(num)


