from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time

# 等待time
while not (t := datetime.now()).hour == 19 or t.minute != 9: time.sleep(0.5)

d = datetime.now() + timedelta(days=30)
date = f"{d.year-1911}{d.month:02d}{d.day:02d}"

opt = webdriver.ChromeOptions()
for arg in ["--disable-blink-features=AutomationControlled"]: opt.add_argument(arg)
opt.add_experimental_option("excludeSwitches", ["enable-automation"])
opt.add_experimental_option('useAutomationExtension', False)
opt.page_load_strategy = 'eager'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opt)
wait = WebDriverWait(driver, 15)
js = driver.execute_script

driver.get("https://www.mvdis.gov.tw/m3-emv-trn/exm/locations#gsc.tab=0")
Select(driver.find_element(By.ID, 'licenseTypeCode')).select_by_visible_text('普通重型機車')

inp = driver.find_element(By.ID, 'expectExamDateStr')
js("arguments[0].removeAttribute('readonly');", inp)
inp.send_keys(date)

Select(driver.find_element(By.ID, 'dmvNoLv1')).select_by_visible_text('臺中區監理所（中彰投）')
wait.until(lambda d: "彰化" in d.find_element(By.ID, 'dmvNo').text)
s = Select(driver.find_element(By.ID, 'dmvNo'))
next(s.select_by_visible_text(o.text) for o in s.options if "彰化監理站" in o.text)

js("document.querySelector('a[onclick=\"query();\"]').click()")
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "blockUI")))
js("document.querySelectorAll('.blockUI').forEach(e=>e.remove())")

btns = driver.find_elements(By.XPATH, "//a[contains(@onclick,'preAdd')]")
if btns: js("arguments[0].click();", btns[0])

wait.until(EC.presence_of_element_located((By.ID, 'idNo')))
js("document.querySelectorAll('.blockUI').forEach(e=>e.remove())")

for id_, val in [('idNo','A1234567890'),('birthdayStr','0900101'),('name','王小名'),('contactTel','0912345678'),('email','123@gmail.com')]:
    driver.find_element(By.ID, id_).send_keys(val)

time.sleep(300)
driver.quit()
