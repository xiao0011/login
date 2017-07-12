#coding:utf8

import unittest         #引入测试组件
import HTMLTestRunner   #引入测试生成结果组件

from time import sleep
from selenium import webdriver # 引入浏览器驱动
from selenium.webdriver.support.select import Select # 引入浏览器驱动的元素路径选择包



class TestCase(unittest.TestCase):  #定义类
    '''
    父类会在对象开始时调用这个方法
    '''
    def setUp (self): #定义类下面的方法
        chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        self.driver  = webdriver.Chrome(chromedriver)
        self.baseUrl = "http://120.25.234.145/cloud/index.php"   #定义一个请求地址/域名

    """
    结束每个测试后的清理工作
    :return:
    """
    def tearDown(self) :
        self.driver.quit() #退出浏览器

    def openPage (self, url):
        self.driver.get(self.baseUrl + url)

    """
    登录的用例
    :return:
    """
    def login(self):
        self.openPage("/Login/Login/index") # 打开登录页面
        self.driver.implicitly_wait(5)      # 等待加载5秒
        self.setElement("id,username", "463811@qq.com") # 查找账号的input然后赋值
        self.setElement("id,userpwd", "123456") # 查找密码的input然后赋值
        self.getElement("c,login-btn").click() # 点击登录
        sleep(2) # 等待2秒

        # 断言判断当前登录成功的url 和 预期的url是否一致 
        self.assertEqual(self.baseUrl + "/Manage/BenchWork/index", self.driver.current_url, u"登录失败")

    """
    查找元素的方法
    selector参数的格式(查找方式, 查找的值) id,name 元素的id属性是name
    """
    def getElement(self, selector):
        """
        to locate element by selector
        :arg
        selector should be passed by an example with "i,xxx"
        "x,//*[@id='langs']/button"
        :returns
        DOM element
        """
        if ',' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split(',')[0]
        selector_value = selector.split(',')[1]

        if selector_by == "i" or selector_by == 'id':
            element = self.driver.find_element_by_id(selector_value)
        elif selector_by == "n" or selector_by == 'name':
            element = self.driver.find_element_by_name(selector_value)
        elif selector_by == "c" or selector_by == 'class_name':
            element = self.driver.find_element_by_class_name(selector_value)
        elif selector_by == "l" or selector_by == 'link_text':
            element = self.driver.find_element_by_link_text(selector_value)
        elif selector_by == "p" or selector_by == 'partial_link_text':
            element = self.driver.find_element_by_partial_link_text(selector_value)
        elif selector_by == "t" or selector_by == 'tag_name':
            element = self.driver.find_element_by_tag_name(selector_value)
        elif selector_by == "x" or selector_by == 'xpath':
            element = self.driver.find_element_by_xpath(selector_value)
        elif selector_by == "s" or selector_by == 'selector_selector':
            element = self.driver.find_element_by_css_selector(selector_value)
        else:
            raise NameError("Please enter a valid type of targeting elements.")

        return element

    """
    设置匹配元素的值
    """
    def setElement(self, selector, value):
        el = self.getElement(selector)

        el.clear()
        el.send_keys(value)



suite  = unittest.TestSuite(); # 声明一个测试套件
buf    = open("./result.html", "wb") # 创建一个测试结果文件
runner = HTMLTestRunner.HTMLTestRunner(stream=buf, title="Ranzhi Test Result", description="Test Case Run Result") #声明测试运行对象

suite.addTest(TestCase('login'))   # 添加一个登录的测试用例到测试套件里
runner.run(suite) # 运行测试， 并且将结果生成为HTML
buf.close() # 关闭文件输出
