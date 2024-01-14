# from capute import Caputre
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class WeiXin():
    def start(self):
        self._login_wx()

    def stop(self):
        pass

    def _login_wx(self):
        login_url = "https://channels.weixin.qq.com/login.html"
        home_url = "https://channels.weixin.qq.com/platform"

        driver = webdriver.Edge()
        driver.get(login_url)
        wait = WebDriverWait(webdriver, timeout=60, poll_frequency=.2)
        
        wait.until(lambda d : EC.url_contains(home_url))
        print("login success")

if __name__ == "__main__":
    WeiXin().start()