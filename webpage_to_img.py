from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# driver = webdriver.Firefox()
driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768)  # set the window size that you need
driver.get('https://github.com')
driver.save_screenshot('github.png')
# driver.get('http://ynet.co.il')
# driver.save_screenshot('ynet.png')

"""
Download and extract PhantomJS to /usr/local/bin
"""
