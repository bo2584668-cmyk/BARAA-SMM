import os
import time
import random
from flask import Flask, request, jsonify
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

def get_driver():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    return uc.Chrome(options=options)

@app.route('/api/order', methods=['GET'])
def run_bot():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"status": "error", "message": "الرابط مطلوب"}), 400

    results = []
    # قراءة الحسابات من الملف الرئيسي
    accounts_path = os.path.join(os.path.dirname(__file__), '..', 'accounts.txt')
    
    if not os.path.exists(accounts_path):
        return jsonify({"status": "error", "message": "ملف الحسابات غير موجود"}), 500

    with open(accounts_path, "r") as f:
        accounts = [line.strip().split(':') for line in f if ":" in line]

    driver = None
    try:
        driver = get_driver()
        # سننفذ أول حساب فقط لتجنب الـ Timeout في Vercel (خطة مجانية)
        user, pw = accounts[0]
        
        driver.get("https://www.tiktok.com")
        wait = WebDriverWait(driver, 20)
        
        # تسجيل الدخول
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(user)
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(pw)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        time.sleep(10) # انتظار الكابتشا يدوياً أو التخطي الآلي
        
        # المتابعة
        driver.get(target_url)
        time.sleep(5)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow') or contains(., 'متابعة')]")))
        btn.click()
        
        return jsonify({"status": "completed", "user": user})
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500
    finally:
        if driver:
            driver.quit()

@app.route('/')
def home():
    return "سيرفر الرشق يعمل بنجاح - 2026"
