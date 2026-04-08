from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from datetime import datetime,timedelta
import time
while not(datetime.now().hour==19 and datetime.now().minute==32):time.sleep(0.5)
d=datetime.now()+timedelta(days=30);o=webdriver.ChromeOptions()
o.add_argument("--disable-blink-features=AutomationControlled");o.add_experimental_option("excludeSwitches",["enable-automation"]);o.add_experimental_option('useAutomationExtension',False);o.page_load_strategy='eager'
v=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=o)
W=WebDriverWait(v,15);j=v.execute_script;F=lambda i:v.find_element(By.ID,i);rm=lambda:j("document.querySelectorAll('.blockUI').forEach(e=>e.remove())")
v.get("https://www.mvdis.gov.tw/m3-emv-trn/exm/locations#gsc.tab=0")
Select(F('licenseTypeCode')).select_by_visible_text('普通重型機車')
i=F('expectExamDateStr');j("arguments[0].removeAttribute('readonly');",i);i.send_keys(f"{d.year-1911}{d.month:02d}{d.day:02d}")
Select(F('dmvNoLv1')).select_by_visible_text('臺中區監理所（中彰投）');W.until(lambda _:"彰化" in F('dmvNo').text)
s=Select(F('dmvNo'));[s.select_by_visible_text(x.text) for x in s.options if "彰化監理站" in x.text]
j("document.querySelector('a[onclick=\"query();\"]').click()");W.until(EC.presence_of_element_located((By.CLASS_NAME,"blockUI")));rm()
b=v.find_elements(By.XPATH,"//a[contains(@onclick,'preAdd')]")
if b:j("arguments[0].click();",b[0])
W.until(EC.presence_of_element_located((By.ID,'idNo')));rm()
for k,val in[('idNo','A1234567890'),('birthdayStr','0900102'),('name','張屁炎'),('contactTel','0912345678'),('email','PIYAN@gmail.com')]:F(k).send_keys(val)
time.sleep(300);v.quit()
