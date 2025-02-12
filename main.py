import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.mime.text import MIMEText

# Konfiguracja
URL = 'https://www.popmart.com/pl/products/527/THE-MONSTERS---Tasty-Macarons-Vinyl-Face-Blind-Box'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
EMAIL_SENDER = 'multikaka122@gmail.com'
EMAIL_PASSWORD = 'trwv dwjv jqzz mheh'
EMAIL_RECEIVER = 'irzycki.igor@gmail.com'

# Konfiguracja trybu headless
chrome_options = Options()
chrome_options.add_argument("--headless")          # Tryb bezgłowy (brak GUI)
chrome_options.add_argument("--no-sandbox")        # Dla środowisk chmurowych
chrome_options.add_argument("--disable-dev-shm-usage")  # Zmniejszenie zużycia pamięci
chrome_options.add_argument("--disable-gpu")       # Wyłączenie akceleracji GPU (dla serwerów)
chrome_options.add_argument("--window-size=1920,1080")  # Ustawienie rozdzielczości

# Funkcja do pobierania aktualnej godziny
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Funkcja sprawdzająca dostępność produktu
def check_availability():
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(URL)
        time.sleep(5)  # Poczekaj na załadowanie strony

        # Pobierz cały tekst ze strony
        page_text = driver.find_element(By.TAG_NAME, 'body').text

        # Sprawdzanie dostępności przycisku "ADD TO CART"
        if "ADD TO CART" in page_text:
            print(f"✅ [{get_current_time()}] Produkt dostępny!")
            driver.quit()
            return True
        else:
            print(f"❌ [{get_current_time()}] Produkt nadal niedostępny.")
            driver.quit()
            return False

    except Exception as e:
        print(f"⚠️ [{get_current_time()}] Błąd podczas sprawdzania dostępności: {e}")
        driver.quit()
    return False

# Funkcja wysyłająca powiadomienie e-mail
def send_notification():
    msg = MIMEText(f'✅ Produkt jest dostępny! Sprawdź stronę: {URL}')
    msg['Subject'] = 'Powiadomienie o dostępności produktu'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"✉️ [{get_current_time()}] Powiadomienie e-mail wysłane!")
    except Exception as e:
        print(f"⚠️ [{get_current_time()}] Błąd podczas wysyłania powiadomienia: {e}")

# Główna pętla sprawdzająca dostępność produktu
while True:
    print(f"🔍 [{get_current_time()}] Sprawdzanie dostępności produktu...")
    if check_availability():
        send_notification()
        break  # Zatrzymaj bota po wysłaniu powiadomienia
    else:
        print(f"⏳ [{get_current_time()}] Oczekiwanie na ponowne sprawdzenie dostępności...")

    time.sleep(180)  # Sprawdzanie co 3 minut
