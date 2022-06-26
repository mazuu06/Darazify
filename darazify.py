from modules.scrape import Daraz
from modules import options
from modules import colors
from modules import clrscr
from modules import banner

clrscr.clear_screen()
banner.Banner()
link = options.get_link()
percent = int(input(f"{colors.bcolors.LOGGING}Enter Minium Discount Percentage [1-100] : {colors.bcolors.ENDC}"))
bswr = input(f"{colors.bcolors.OKGREEN}Do you want to search in browser{colors.bcolors.ENDC} {colors.bcolors.NOTICE}(It can take more time){colors.bcolors.ENDC} [Y/n] : ")

if bswr == "Y" or bswr == "y" :
    browser_open = 1
elif bswr == "N" or bswr == "n" :
    browser_open = 0
else:
    print(f'{colors.bcolors.RED}Invalid input try again{colors.bcolors.ENDC}')
    exit()

clrscr.clear_screen()
open('output.txt', 'w').close()
i = 1

while True:
    url = link + str(i)
    print("<=================================================================================>".center(167))
    print(f'{colors.bcolors.RED}{[i]}{colors.bcolors.ENDC} Trying on --> {colors.bcolors.HEADER}{url}{colors.bcolors.ENDC}'.center(185))
    print("<=================================================================================>".center(167))
    print('\n')
    Daraz(url, percent, browser_open)
    i =i + 1
    













