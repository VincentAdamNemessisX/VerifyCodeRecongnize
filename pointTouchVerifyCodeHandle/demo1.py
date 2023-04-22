"""
# File       : demo1.py
# Time       : 3:09 PM
# Author     : vincent
# version    : python 3.8
# Description:
"""
import time
from io import BytesIO
from PIL import Image
from pointTouchVerifyCodeHandle.chaojiyingAPIRecognizeAnyCode import Chaojiying_Client
import selenium.webdriver as webdriver
from selenium.webdriver.support.wait import WebDriverWait

EMAIL = 'vincentadamnemessis@gmail.com'
PASSWORD = 'ZTXic3344'


CHAOJIYING_USERNAME = 'vincentadam'
CHAPJIYING_PASSWORD = 'ZTXic3344'
CHAOJIYING_SOFT_ID = 'e824e24ff8bc3d650c1b9d07a59317a6'
CHAOJIYING_KIND = 9102


def get_points(captcha_result):
    """
    解析识别结果
    :param captcha_result: 识别结果
    :return: 坐标元组
    """
    groups = captcha_result.get('pic_str').split('|')
    locations = [[int(number) for number in group.split(',')] for group in groups]
    return locations


class CrackTouClick:
    def __init__(self):
        self.url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD
        self.chaojiying = Chaojiying_Client(CHAOJIYING_USERNAME, CHAPJIYING_PASSWORD, CHAOJIYING_SOFT_ID)

    def open(self):
        """
        打开浏览器输入网址
        :return: None
        """
        self.browser.get(self.url)
        email = self.wait.until(lambda x: x.find_element_by_id('J-userName'))
        password = self.wait.until(lambda x: x.find_element_by_id('J-password'))
        email.send_keys(self.email)
        password.send_keys(self.password)

    def get_touclick_button(self):
        """
        获取初始验证按钮
        :return: button
        """
        button = self.wait.until(lambda x: x.find_element_by_class_name('touclick-image'))
        return button

    def get_position(self):
        """
        获取验证码位置
        :return: position
        """
        img = self.wait.until(lambda x: x.find_element_by_class_name('touclick-image'))
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return top, bottom, left, right

    def get_screenshot(self):
        """
        获取网页截图
        :return: screenshot
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_touclick_image(self, name='captcha.png'):
        """
        获取验证码图片
        :param name: 图片保存位置
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def touch_click_words(self, locations):
        """
        点按验证
        :param locations: 坐标元组
        :return: None
        """
        for location in locations:
            print(location)
            webdriver.ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_button(), location[0],
                                                                             location[1]).click().perform()
            time.sleep(1)
