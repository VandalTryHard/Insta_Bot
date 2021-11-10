from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from data_auth import username, password, hashtag
import time
import random

# def login(username, password):
#     try:
#           #открывает хром и заходит на сайт
#         browser = webdriver.Chrome("C:/Users/Val/Desktop/Py/Insta_Bot/chromedriver/chromedriver")
#         browser.get("https://www.instagram.com")
#         time.sleep(random.randrange(3, 5))

#         #Поиск и ввод username
#         username_input = browser.find_element_by_name("username")
#         username_input.clear()
#         username_input.send_keys(username)

#         time.sleep(2) #Задержка

#         #Поиск и ввод пароля
#         password_input = browser.find_element_by_name("password")
#         password_input.clear()
#         password_input.send_keys(password)

#         password_input.send_keys(Keys.ENTER)
#         time.sleep(10)


#         browser.close()
#         browser.quit()

#     except Exception as ex: # если что-то пойдет не так
#         print(ex)
#         browser.close()
#         browser.quit()


# login(username, password)

def search_hashtag(username, password, hashtag):
    browser = webdriver.Chrome("chromedriver\chromedriver.exe")  # путь до хрома
    try:
          #заходит на сайт
        browser.get("https://www.instagram.com")
        time.sleep(random.randrange(3, 5))

        #Поиск и ввод username
        username_input = browser.find_element_by_name("username")
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2) #Задержка

        #Поиск и ввод пароля
        password_input = browser.find_element_by_name("password")
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

        # лайк по хештегам
        try: 
            browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
            time.sleep(5)

            # browser.close()
            # browser.quit()

            #Проскролить ленту
            for i in range(1, 4):
                browser.execute_script("window.scroll(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))

            #Получение ссылки на посты
            hrefs = browser.find_elements_by_tag_name("a")
            
            urls_posts = [item.get_attribute("href") for item in hrefs if "/p/" in item.get_attribute("href")]
            print(urls_posts)
            # urls_posts = []
            # for item in hrefs:
            #     href = item.get_attribute("href")
            #     if "/p/" in href:
            #         urls_posts.append(href)
            #         print(href)

            #ставим лайк под каждым постом 
            for url in urls_posts:
                try:
                    browser.get(url)
                    button_like = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button").click()
                    time.sleep(random.randrange(10, 30)) #засыпает чтобы не забанили
                except Exception as ex:
                    print(ex)

        except Exception as ex:
            print(ex)
            browser.close()
            browser.quit()

    except Exception as ex: # если что-то пойдет не так
        print(ex)
        browser.close()
        browser.quit()

search_hashtag(username, password, hashtag)
    