from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from data_auth import username, password, hashtag
import time
import random
from selenium.common.exceptions import  NoSuchElementException

class InstagramBot():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("chromedriver\chromedriver.exe")
    
    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self):
        browser = self.browser
        browser.get("https://www.instagram.com")
        time.sleep(random.randrange(3, 5))

        #Поиск и ввод username
        username_input = browser.find_element_by_name("username")
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(4) #Задержка

        #Поиск и ввод пароля
        password_input = browser.find_element_by_name("password")
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(5)
 
    def like_prhoto_by_hashtag(self, hashtag):
        browser = self.browser
        browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        time.sleep(5)

        #Проскролить ленту
        for i in range(1, 4):
            browser.execute_script("window.scroll(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        #Получение ссылки на посты
        hrefs = browser.find_elements_by_tag_name("a")
        
        urls_posts = [item.get_attribute("href") for item in hrefs if "/p/" in item.get_attribute("href")]
        print(urls_posts)

        #ставим лайк под каждым постом 
        for url in urls_posts:
            try:
                browser.get(url)
                button_like = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button").click()
                time.sleep(random.randrange(10, 30)) #засыпает чтобы не забанили
            except Exception as ex:
                print(ex)
                self.close_browser()

    # проверка по xpath сущуствует ли элемент на странице
    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # ставим лайки на пост по прямой ссылке
    def put_exactly_like(self, userpost):
        browser = self.browser
        browser.get(userpost)
        time.sleep(4)
        #проверка на корректный ввод поста
        wrong_userpage = "/html/body/div[1]/section/main/div/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого поста нет, проверьте URL")
        else:
            print("Пост успешно найден, ставим лайк")
            time.sleep(2)
            botton_like = "/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button"
            browser.find_element_by_xpath(botton_like).click()
            time.sleep(2)
            print(f"Like поставлен {userpost}")
            self.close_browser()
    
    # ставим лайки по ссылке на аккаунт пользователя
    def put_many_likes(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя нет, проверьте URL")
        else:
            print("Пользователь успешно найден, ставим лайк")
            time.sleep(2)

            #сколько скролить страницу аккаунта
            posts_count = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text
            posts_count = str(posts_count[0])+str(posts_count[2: ])
            posts_count = int(posts_count)
            loops_count = int(posts_count / 400)
            print(loops_count)

            #собирает ссылки на все посты
            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name("a")
                hrefs = [item.get_attribute("href") for item in hrefs if "/p/" in item.get_attribute("href")]
                for href in hrefs:
                    posts_urls.append(href)
                browser.execute_script("window.scroll(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))
                print(f"Итерация {i}")
                time.sleep(2)
            
            file_name = userpage.split("/") [-2]
            
            # убирает повторяющиеся ссылки на посты
            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)
            # сохранение списка ссылок в новый файл
            with open(f"{file_name}_set.txt", "a") as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            #ставим лайки на рандомный пост
            with open(f"{file_name}_set.txt", "r") as file:
                urls_list = file.readlines()
                for post_url in urls_list:
                    try:
                        browser.get(post_url)
                        time.sleep(2)
                        botton_like = "/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button"
                        browser.find_element_by_xpath(botton_like).click()
                        time.sleep(random.randrange(80,100))
                        # time.sleep(2)
                        print(f"Like поставлен {post_url}")
                    except Exception as ex:
                        print(ex)
                        self.close_browser()
            self.close_browser()

my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.put_many_likes("....")