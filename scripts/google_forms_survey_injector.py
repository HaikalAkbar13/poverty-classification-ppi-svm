"""
Google Forms Survey Data Automation Injector
Author: Muh Haikal Akbar, S.E.
Research: Poverty Classification & PPI Scorecard (Sulawesi Selatan)

Deskripsi:
Skrip otomasi berbasis Selenium WebDriver untuk memasukkan data survei responden
ke dalam formulir Google Forms secara terstruktur dan terotomatisasi.
"""

import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def inject_survey_data(csv_path="../data/raw/Data Responden.csv", form_url="https://forms.gle/fa3NgDFuV2aKA7mw5", driver_path=None):
    if not os.path.exists(csv_path):
        print(f"Error: File {csv_path} tidak ditemukan.")
        return

    data = pd.read_csv(csv_path)
    total_rows = data.shape[0]
    print(f"Total baris responden yang akan diproses: {total_rows}")

    # Inisialisasi Chrome Driver
    if driver_path and os.path.exists(driver_path):
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service)
    else:
        driver = webdriver.Chrome()

    try:
        driver.get(form_url)
        time.sleep(2)

        for i in range(total_rows):
            nama_responden = str(data.iloc[i][0])
            print(f"[{i+1}/{total_rows}] Menginjeksi data responden: {nama_responden}...")

            # Mengisi data pertanyaan 1 (Nama)
            input_p1 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))
            )
            input_p1.clear()
            input_p1.send_keys(nama_responden)
            time.sleep(0.1)

            # Mengisi pertanyaan radio button & field lainnya (P2 s/d P11)
            for q_idx in range(1, 11):
                jawaban = str(data.iloc[i][q_idx]).strip().lower()
                xpath_container = f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[{q_idx+1}]/div/div/div[2]/div/div'
                
                try:
                    container = driver.find_element(By.XPATH, xpath_container)
                    radio_buttons = container.find_elements(By.XPATH, './/div[@role="radio"]')
                    
                    if radio_buttons:
                        for radio in radio_buttons:
                            label = radio.get_attribute("aria-label")
                            if label and label.strip().lower() == jawaban:
                                radio.click()
                                break
                    else:
                        text_input = container.find_element(By.XPATH, './/input')
                        text_input.clear()
                        text_input.send_keys(jawaban)
                except Exception:
                    pass
                time.sleep(0.05)

            # Submit Form
            submit_btn = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            submit_btn.click()
            time.sleep(0.5)

            # Kembali ke halaman form untuk responden berikutnya
            try:
                back_link = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
                back_link.click()
                time.sleep(1)
            except Exception:
                driver.get(form_url)
                time.sleep(1)

        print("Seluruh data responden berhasil diinjeksi ke formulir survei.")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Skrip siap digunakan. Panggil inject_survey_data() jika ingin mengeksekusi otomasi.")
