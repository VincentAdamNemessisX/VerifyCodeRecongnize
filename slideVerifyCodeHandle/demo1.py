"""
# File       : demo1.py
# Time       : 3:12 PM
# Author     : vincent
# version    : python 3.8
# Description:
"""
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

USERNAME = '15637185519'
PASSWORD = 'ZTXic3344'


class CrackGeetest:
    def __init__(self):
        """
        初始化
        :return:
        """
        self.url = 'https://passport.zhihuishu.com/'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWORD

    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return:
        """
        self.browser.find_element(By.ID, 'lUsername').send_keys(self.username)
        self.browser.find_element(By.ID, 'lPassword').send_keys(self.password)
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'wall-sub-btn')))
        return button

    def get_position(self):
        """
        获取验证码位置
        :return:
        """
        # img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))
        img = self.browser.find_element(By.CLASS_NAME, 'yidun_bg-img')
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        print(location, size)
        return top, bottom, left, right

    def get_screenshot(self):
        """
        获取网页截图
        :return:
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_slider(self):
        """
        获取滑块
        :return:
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'yidun_jigsaw')))
        return slider

    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :param name:
        :return:
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    @staticmethod
    def is_pixel_equal(image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1:
        :param image2:
        :param x:
        :param y:
        :return:
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1:
        :param image2:
        :return:
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    @staticmethod
    def get_track(distance):
        """
        根据偏移量获取移动轨迹
        :param distance:
        :return:
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0
        while current < distance:
            if current < mid:
                # 加速度为2
                a = 2
            else:
                # 加速度为-3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, tracks):
        """
        拖动滑块到缺口处
        :param slider:
        :param tracks:
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()


if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.get('https://passport.zhihuishu.com/')
    browser.find_element(By.ID, 'lUsername').send_keys('15637185519')
    browser.find_element(By.ID, 'lPassword').send_keys('ZTXic3344')
    browser.find_element(By.CLASS_NAME, 'wall-sub-btn').click()
    image = browser.find_element(By.CLASS_NAME, 'yidun_bg-img')
    # browser.close()

    # crack = CrackGeetest()
    # crack.browser.get(crack.url)
    # button = crack.get_geetest_button()
    # button.click()
    # image1 = crack.get_geetest_image('captcha1.png')
    # slider = crack.get_slider()
    # slider.click()
    # image2 = crack.get_geetest_image('captcha2.png')
    # gap = crack.get_gap(image1, image2)
    # print('缺口位置', gap)
    # track = crack.get_track(gap - 10)
    # crack.move_to_gap(slider, track)
