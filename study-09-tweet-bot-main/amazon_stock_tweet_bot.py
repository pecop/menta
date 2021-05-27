import datetime
import os
import time
import tweepy
from dotenv import load_dotenv
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import schedule

class Twitter():
    def __init__(self):
        load_dotenv(verbose=True)
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.consumer_key = os.environment.get('CONSUMER_KEY')
        self.consumer_secret = os.environment.get('CONSUMER_SECRET')
        self.access_token = os.environment.get('ACCESS_TOKEN')
        self.access_token_secret= os.environment.get('CONSUMER_KEY')

    def authenticate(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, result):
        self.authenticate()
        self.api.update_status(result)

class Amazon():
    def __init__(self):
        load_dotenv(verbose=True)
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.url = os.environment.get('AMAZON_URL')

    def set_driver(self, driver_path, headless_flg):
        # Chromeドライバーの読み込み
        options = ChromeOptions()

        # ヘッドレスモード（画面非表示モード）の設定
        if headless_flg == True:
            options.add_argument('--headless')

        # 起動オプションの設定
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
        # options.add_argument('print-level=3')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--incognito')          # シークレットモードの設定を付与

        # ChromeのWebDriverオブジェクトを作成する。
        return Chrome(ChromeDriverManager().install(), options=options)

    def access_web_page(self):
        if os.name == 'nt': #Windows
            self.driver = self.set_driver("chromedriver.exe", False)
        elif os.name == 'posix': #Mac
            self.driver = self.set_driver("chromedriver", False)
        # Webサイトを開く
        self.driver.get(self.url)
        time.sleep(5)

    def check_stock(self):
        self.access_web_page()
        # 「カートにいれる」ボタンの有無確認
        if self.driver.find_element_by_id("add-to-cart-button"):
            product_name = self.driver.find_element_by_id("productTitle".text)
            # result = f"『{product_name}』の在庫あり！"
            result = "APIからTweetできたーーーー！（＾ω＾）"
        else:
            result = None
        
        print(result)
        return result
    
def main():
    # prev_result = None
    global prev_result

    # while True:
    # Amazon在庫チェック
    result = Amazon.checkstock()
    if result and not prev_result:
        # ツイート
        Twitter.tweet(result)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{now}]「{result}」のツイート完了')
        prev_result = result
    elif not result and prev_result:
        prev_result = result
    # time.sleep(1)

if __name__ == '__main__':
    # main()
    prev_result = None
    schedule.every(1).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)