import time
import pyotp
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# === CONFIGURATION ===
client_id = "15YI17TORX-100"             # e.g., "ABCD12345-100"
secret_key = "2HJ9AD57A5"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
# totp_secret = "YOUR_TOTP_SECRET"         # From Google Authenticator app
username = "YOUR_EMAIL_OR_PHONE"
password = "YOUR_PASSWORD"


# === Generate TOTP ===
def get_totp():
    x = pyotp.parse_uri('otpauth://totp/Fryers:ayantab%40google.com?secret=QUDQF2DQOWIPL2FFACUVUMW6S44CYXDV&issuer=Fryers')
    return x.now()


# === Fetch auth code via headless browser ===
def fetch_auth_code():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Step 1: Open login URL
        auth_url = (
            f"https://api.fyers.in/api/v2/generate-authcode?client_id={client_id}"
            f"&redirect_uri={redirect_uri}&response_type=code&state=sample"
        )
        driver.get(auth_url)
        time.sleep(2)

        # Step 2: Login Steps
        driver.find_element(By.NAME, "fy_id").send_keys(username)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        # Step 3: Enter TOTP
        totp = get_totp()
        driver.find_element(By.NAME, "verify-pin").send_keys(totp)
        driver.find_element(By.TAG_NAME, "button").click()

        # Step 4: Wait for redirect and extract code
        time.sleep(5)
        final_url = driver.current_url

        if "code=" not in final_url:
            raise Exception("Auth code not found in URL. Login may have failed.")

        code = final_url.split("code=")[-1].split("&")[0]
        return code

    finally:
        driver.quit()


# === Exchange auth code for access token ===
def generate_access_token(auth_code):
    url = "https://api.fyers.in/api/v2/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "secret_key": secret_key,
        "code": auth_code,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(url, json=payload)
    data = response.json()

    if "access_token" in data:
        return data["access_token"]
    else:
        raise Exception(f"Token generation failed: {data}")


# === MAIN ===
def get_fyers_access_token():
    print("Generating auth code...")
    auth_code = fetch_auth_code()
    print("Auth code fetched:", auth_code)

    print("Generating access token...")
    token = generate_access_token(auth_code)
    print("Access token:", token)
    return token


if __name__ == "__main__":
    get_fyers_access_token()
