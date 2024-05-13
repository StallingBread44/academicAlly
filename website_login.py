from selenium import webdriver

url = 'https://hac.friscoisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f'
username = "304551"
password = "DEBA1243$"
driver = webdriver.Chrome("/Users/samueldeepak/Downloads/chromedriver-mac-arm64.zip")
driver.get(url)
