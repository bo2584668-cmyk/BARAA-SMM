import time
import os
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- 1. إعدادات الرشق (تأكد من وضع الرابط الصحيح هنا) ---
TARGET_URL = "https://www.tiktok.com"  # ضع رابط الهدف هنا
FOLLOW_LIMIT = 5   
MIN_SLEEP = 25      
MAX_SLEEP = 50      

def load_accounts(file_path):
    accounts = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            for line in f:
                if ":" in line:
                    user, pw = line.strip().split(":")
                    accounts.append((user, pw))
    return accounts

def get_driver():
    options = uc.ChromeOptions()
    # إعدادات Codespaces الضرورية 2026
    options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    # تزييف الهوية لتبدو كمتصفح حقيقي
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = uc.Chrome(options=options)
    return driver

def start_bot():
    all_accounts = load_accounts("accounts.txt")
    if not all_accounts:
        print("❌ خطأ: ملف accounts.txt غير موجود أو فارغ")
        return

    selected = all_accounts[:FOLLOW_LIMIT]
    print(f"🚀 بدء المهمة لـ {len(selected)} متابع...")

    for i, (username, password) in enumerate(selected):
        print(f"👤 [{i+1}/{len(selected)}] جاري العمل بـ: {username}")
        driver = None
        try:
            driver = get_driver()
            # الذهاب مباشرة لصفحة الإيميل
            driver.get("https://www.tiktok.com")
            
            # انتظار ظهور الحقول
            wait = WebDriverWait(driver, 20)
            user_input = wait.until(EC.presence_of_element_id("username")) # تيك توك يستخدم ID أحياناً
            
            user_input.send_keys(username)
            driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password)
            time.sleep(random.uniform(1, 3))
            
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            print("⏳ انتظر تسجيل الدخول (فحص الكابتشا).. سيتم الانتظار 15 ثانية")
            time.sleep(15) 

            # الذهاب للهدف
            driver.get(TARGET_URL)
            time.sleep(random.uniform(5, 8))

            # الضغط على زر المتابعة بطريقة مرنة
            follow_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow') or contains(., 'متابعة')]")))
            follow_btn.click()
            print(f"✅ تم المتابعة بنجاح!")

        except Exception as e:
            print(f"❌ فشل الحساب {username} (ربما كابتشا أو تغير في الموقع)")
        
        finally:
            if driver:
                driver.quit()
            
            if i < len(selected) - 1:
                wait_time = random.randint(MIN_SLEEP, MAX_SLEEP)
                print(f"💤 انتظار أمني لمدة {wait_time} ثانية...")
                time.sleep(wait_time)

    print("🏁 اكتملت المهمة!")

if __name__ == "__main__":
    start_bot()

