from modules import colors
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import warnings
 
class FindPercent:
    def get_percent(self,actual_price, discount_price):
        actual_price = actual_price[3:]
        if ',' in actual_price:
            actual_price = actual_price.replace(',', '')
        actual_price = int(actual_price)

        discount_price = discount_price[3:]
        if ',' in discount_price:
            discount_price = discount_price.replace(',', '')
        discount_price = int(discount_price)

        if actual_price < discount_price:
            percent = (actual_price/discount_price)*100

        elif actual_price > discount_price:
            percent = (discount_price/actual_price)*100

        else:
            percent = actual_price

        percent = abs(percent - 100)

        return int(percent)


class OutPutFile():
    def __init__(self, titles, links, act_prices, prices_after_dis):
        with open('output.txt', 'a+') as f:
            for (titles, links, act_prices, prices_after_dis) in zip(titles, links, act_prices, prices_after_dis) :
                f.write("[TITLE] ==> {0}\t||\t[ACTUAL PRICE] ==> {1}\t||\t[PRICE AFTER DISCOUNT] ==> {2}\t||\t[LINK] ==> {3}\n\n".format(titles, act_prices, prices_after_dis, links) )


class Daraz(FindPercent):
    def __init__(self, url, require_percent, browser_open):
        self.url = url
        self.require_percent = require_percent
        self.browser_open = browser_open
        self.titles = []
        self.links = []
        self.act_prices = []
        self.prices_after_dis = []
        self.exit = 0

        if self.browser_open == 1:
            self.driver = webdriver.Firefox()
            self.driver.minimize_window()
        else:
            self.browser_handler()

        try :
            self.driver.get(url)
        except:
            print("Oops! Something went wrong. Check your internet connection.")
            self.driver.quit()
            exit()
        

        try:
            not_found = self.driver.find_element_by_xpath('//*[@class="box--XEzLA"]/div[1]').text
            self.driver.quit()
            self.exit = 1
        except:
            self.div_len = self.driver.find_elements_by_xpath('//*[@class="box--ujueT"]/div')

        if self.exit == 1:
            exit()
        self.get_details()

    def browser_handler(self):
        warnings.simplefilter("ignore")
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

        options = Options()
        options.headless = True
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

                #create a Firefox browser instance object Options
        profile = webdriver.FirefoxProfile()
                #disable CSS load
        profile.set_preference('permissions.default.stylesheet',2)
                #disable images loading
        profile.set_preference('permissions.default.image',2)
                #disable flash plug
        profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',False)
                #Start the Firefox browser with custom settings
        self.driver = webdriver.Firefox(options=options, firefox_profile = profile)


    def get_details(self):
        for i in range(1, len(self.div_len)):
            try:
                title_name=self.driver.find_element_by_xpath('//*[@class="box--ujueT"]/div['+str(i)+']/div/div/div[2]/div[2]/a')
                self.title = title_name.get_attribute('title')

                target_link=self.driver.find_element_by_xpath('//*[@class="box--ujueT"]/div['+str(i)+']/div/div/div[2]/div[2]/a')
                self.link = target_link.get_attribute('href')

                self.discount_price=self.driver.find_element_by_xpath('//*[@class="box--ujueT"]/div['+str(i)+']/div/div/div[2]/div[3]/span').text
                try:
                    self.actual_price=self.driver.find_element_by_xpath('//*[@class="box--ujueT"]/div['+str(i)+']/div/div/div[2]/div[4]/span[1]/del').text
                    percent = self.get_percent(self.actual_price, self.discount_price)

                except:
                    # actual_price = "Not found"
                    continue
                

                if percent >= self.require_percent:
                    if len(self.title) < 65:
                        temp = str(self.title)
                        self.title = (temp+'.').ljust(65)
                    else:
                        self.title = self.title[0:60]+'.....'

                    if len(self.actual_price) < 12:
                        temp = 12 - len(self.actual_price)
                        xyz = ' '*temp
                        self.actual_price = str(self.actual_price) + str(xyz)

                    if len(self.discount_price) < 12:
                        temp = 12 - len(self.discount_price)
                        temp = ' '*temp
                        self.discount_price = str(self.discount_price) + str(xyz)

                    print(f'{colors.bcolors.NOTICE}[TITLE]{colors.bcolors.ENDC} {self.title} {colors.bcolors.OKGREEN}[ACTUAL PRICE]{colors.bcolors.ENDC} {self.actual_price} {colors.bcolors.RED}[PRICE AFTER DISCOUNT]{colors.bcolors.ENDC} {self.discount_price}')
                    print(f'{colors.bcolors.OKBLUE}[LINK]{colors.bcolors.ENDC} {self.link}') 
                    print("--------------------------------------------------------------------------------------------------------------------------------------->")
                    
                    self.titles.append(self.title)
                    self.links.append(self.link)
                    self.act_prices.append(self.actual_price)
                    self.prices_after_dis.append(self.discount_price)

            except:
                pass
        print(f'{colors.bcolors.RED}{len(self.titles)} products found in this page{colors.bcolors.ENDC}')
        self.driver.quit()
        OutPutFile(self.titles, self.links, self.act_prices, self.prices_after_dis)

        

