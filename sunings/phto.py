from selenium import webdriver
import pickle
import time
driver=webdriver.PhantomJS()
url='https://search.suning.com/%E7%A9%BA%E8%B0%83%E6%8C%82%E6%9C%BA/&iy=0&hf=&sc=0&cf=solr_54103_attrId:%E6%8C%82%E5%A3%81%E5%BC%8F%E7%A9%BA%E8%B0%83&ci=431505&st=0#search-path-box'
driver.get(url)  #此处url填写需要访问的地址
time.sleep(3)
# 获得 cookie信息
driver.get_screenshot_as_file('phan.png')
print('结束！')
