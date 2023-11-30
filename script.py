from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time

driver = webdriver.Edge()
driver.get("https://weathershopper.pythonanywhere.com/")

temp = driver.find_element(By.XPATH, "//*[@id='temperature']")
temp_value = temp.text.split(" ")[0]

def buy():
    cart = driver.find_element(By.XPATH, "/html/body/nav/ul/button")
    cart.click()

    stripe = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/button")

    stripe.click()
    
    driver.switch_to.frame("stripe_checkout_app")

    elem = driver.find_element(By.XPATH, "//*[@id='email']")
    # print(elem)
    elem.send_keys("test@gmail.com")
    driver.find_element(By.XPATH, "//*[@id='card_number']").send_keys("4242")
    driver.find_element(By.XPATH, "//*[@id='card_number']").send_keys("4242")
    driver.find_element(By.XPATH, "//*[@id='card_number']").send_keys("4242")
    driver.find_element(By.XPATH, "//*[@id='card_number']").send_keys("4242")
    driver.find_element(By.XPATH, "//*[@id='cc-exp']").send_keys("10")
    driver.find_element(By.XPATH, "//*[@id='cc-exp']").send_keys("30")
    driver.find_element(By.XPATH, "//*[@id='cc-csc']").send_keys("300")
    driver.find_element(By.XPATH, "//*[@id='billing-zip']").send_keys("12344")
    driver.find_element(By.XPATH, "//*[@id='submitButton']").click()


def selector(boxes, t):
    spf_50 = []
    for box in boxes:
        obj = {}
        title = box.find_element(By.CSS_SELECTOR, "p.font-weight-bold.top-space-10")
        price = box.find_element(By.CSS_SELECTOR, "p:nth-child(3)")
        btn = box.find_element(By.TAG_NAME, "button")
        if title.text.lower().find(t.lower()) > 0: 
            obj["title"] = title.text
            obj["price"] = re.sub(r'[^0-9]', '', str(price.text))
            obj["btn"] = btn
            spf_50.append(obj)
        sorted_obj = sorted(spf_50, key=lambda x: x['price'])
    return sorted_obj

if int(temp_value) > 34:
    print("ABOVE")
    sun_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/a/button")
    sun_btn.click()
    boxes = driver.find_elements(By.CSS_SELECTOR, "div.text-center.col-4")
    spf_50 = selector(boxes, "SPF-50")
    spf_30 = selector(boxes, "SPF-30")
    print(spf_50[0]['title'] + " " + spf_50[0]['price'])
    print(spf_30[0]['title'] + " " + spf_30[0]['price'])
    spf_50[0]['btn'].click()
    spf_30[0]['btn'].click()
    time.sleep(10)
    buy()

elif int(temp_value) < 19:
    print("BELOW")
    moist_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/a/button")
    moist_btn.click()
    boxes = driver.find_elements(By.CSS_SELECTOR, "div.text-center.col-4")
    aloe = selector(boxes, "Aloe")
    almond = selector(boxes, "Almond")
    print(aloe[0]['title'] + " " + aloe[0]['price'])
    print(almond[0]['title'] + " " + almond[0]['price'])
    aloe[0]['btn'].click()
    almond[0]['btn'].click()
    time.sleep(10)
    buy()

driver.quit()