from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from data_auth import username, password, hashtag
import time
import random
from selenium.common.exceptions import  NoSuchElementException
import requests
import os

class InstagramBot():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("chromedriver\chromedriver.exe")
    
    # метод закрывающий браузер
    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    # логин
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
    
    # ставит лайки по hashtag
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
        
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        #ставим лайк под каждым постом 
        for url in posts_urls:
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
        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого поста нет, проверьте URL")
            self.close_browser()
        else:
            print("Пост успешно найден, ставим лайк")
            time.sleep(2)
            botton_like = "/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button"
            browser.find_element_by_xpath(botton_like).click()
            time.sleep(2)
            print(f"Like поставлен {userpost}")
            self.close_browser()
    
    # метод собирает ссылки на все посты пользователя
    def get_all_posts_urls(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя нет, проверьте URL")
        else:
            print("Пользователь успешно найден.")
            time.sleep(2)

            #сколько скролить страницу аккаунта
            posts_count = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text
            # posts_count = str(posts_count[0])+str(posts_count[2: ])
            posts_count = int(posts_count)
            loops_count = int(posts_count / 10)
            print(loops_count)

            #собирает ссылки на все посты
            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
                for href in hrefs:
                    posts_urls.append(href)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))
                print(f"Итерация {i}")
                time.sleep(2)
            
            file_name = userpage.split("/")[-2]

            # сохранение списка ссылок в файл
            with open(f"{file_name}.txt", "w") as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")
            
            # убирает повторяющиеся ссылки на посты
            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            # сохранение списка ссылок в новый файл
            with open(f"{file_name}_set.txt", "w") as file:
                for post_url in set_posts_urls:
                    file.write(post_url + "\n")

    # ставим лайки по ссылке на аккаунт пользователя
    def put_many_likes(self, userpage):
        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)
        
        #ставим лайки на рандомный пост
        with open(f"{file_name}_set.txt") as file:
            urls_list = file.readlines()
            for post_url in urls_list[0:6]:
                try:
                    browser.get(post_url)
                    time.sleep(2) 
                    like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                    browser.find_element_by_xpath(like_button).click()
                    # time.sleep(random.randrange(80,100))
                    time.sleep(2)
                    print(f"Like поставлен {post_url}")
                except Exception as ex:
                    print(ex)
                    self.close_browser()
        self.close_browser()

    # скачивает контент со страницы
    def download_userpage_content(self, userpage):
        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/") [-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        # создание папки для сохранения контента
        if os.path.exists(f"{file_name}"):
            print("Папка уже существует")
        else:
            os.mkdir(file_name)
        

        # ЗДЕСЬ ПРОБЛЕМА НЕ СКАЧИВАЕТСЯ!!! д3
        # скачиваем контент
        img_and_video_src_urls = []
        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()
            for post_url in urls_list[0:10]:
                try:
                    browser.get(post_url)
                    time.sleep(10)
                    
                    #ищет картинку или видео на странице
                    img_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img"
                    video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
                    post_id = post_url.split("/")[-2]

                    if self.xpath_exists(img_src):
                        img_src_url = browser.find_element_by_xpath(img_src).get_attribute("src")
                        img_and_video_src_urls.append(img_src_url)
                        # сохраняем изображение
                        get_img = requests.get(img_src_url)
                        with open(f"{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)

                    elif self.xpath_exists(video_src):
                        video_src_url = browser.find_element_by_xpath(video_src).get_attribute("src")
                        img_and_video_src_urls.append(video_src_url)
                        # сохраняем видео
                        get_video = requests.get(video_src_url, stream=True)
                        with open(f"{file_name}/{file_name}_{post_id}_video.mp4", "wb") as video_file:
                            for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    video_file.write(chunk)

                    else:
                        print("Что-то пошло не так.")
                        img_and_video_src_urls.append(f"{post_url}, нет ссылки!")

                    print(f"Контент {post_url} скачен!")

                except Exception as ex:
                    print(ex)
                    self.close_browser()
            self.close_browser()
        
        with open(f'{file_name}/{file_name}_img_and_video_src_urls.txt', 'a') as file:
            for i in img_and_video_src_urls:
                file.write(i + "\n")

my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.download_userpage_content("https://www.instagram.com/tommyhellatrigger/")