from .logger import log
from splinter import Browser


browser = Browser('chrome')  # TODO enable profile & session claiming
browser.visit('https://www.google.com')
log.debug('Driver: %s' % browser.driver)
log.debug('Session id: %s' % browser.driver.session_id)
