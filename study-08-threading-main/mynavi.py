# STEP3
import os
import time
import datetime
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

LOG_DIR = './log/'
now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
LOG_FILE_PATH = LOG_DIR + f'log_{now}.log'
CSV_FILE_PATH = 'extracted_list_{keyword}_{now}.csv'

if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)

def set_driver(driver_path, headless_flg):
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
#     return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)
    return Chrome(ChromeDriverManager().install(), options=options)

def log(text):
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = f'[{now}] {text}'   
    with open(LOG_FILE_PATH, 'a', encoding='utf-8-sig') as f:
        f.write(logStr + '\n')    
    print(logStr)

def main():
    log('処理開始')
    search_keyword = input("検索したいキーワードを入力してください：")
    log(f'検索キーワード：{search_keyword}')

    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
        
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    try:
        # ポップアップを閉じる
        while driver.find_element_by_class_name("karte-close"):
            driver.execute_script('document.querySelector(".karte-close").click()')
            time.sleep(5)
    except:
        pass

    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    exp_name_list = []
    fin_employment_status_list = []
    fin_workplace_list = []
    fin_salary_list = []
    page = 1
    success = 0
    fail = 0

    while True:
        log(f'{page}ページ目抽出スタート')

        # ページ終了まで繰り返し取得
        count = 1

        # 検索結果の一番上の会社名を取得
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        employment_status_list = driver.find_elements_by_class_name('labelEmploymentStatus')
        table_list = driver.find_elements_by_class_name('tableCondition')

        # 1ページ分繰り返し
        log(f'{page}ページ目 - 求人数：{len(name_list)}件')
        for name, employment_status, table in zip(name_list, employment_status_list, table_list):        
            try:
                exp_name_list.append(name.text)
                fin_employment_status_list.append(employment_status.text)
                title_list = table.find_elements_by_tag_name('th')
                content_list = table.find_elements_by_tag_name('td')
                for title, content in zip(title_list, content_list):
                    if title.text == '勤務地':
                        fin_workplace_list.append(content.text)
                    elif title.text == '給与':
                        fin_salary_list.append(content.text)          
                success += 1
                log(f'{count}件目抽出完了')       
            except:
                fail += 1
                log(f'{count}件目抽出失敗')         
            finally:
                count += 1

        log(f'{page}ページ目抽出完了')
        next_page = driver.find_elements_by_class_name('iconFont--arrowLeft')
        if len(next_page) > 0:
            url = next_page[0].get_attribute('href')
            driver.get(url)
            time.sleep(5)
            page += 1
        else:
            break
            
    driver.quit()

    d = {
        '会社名': exp_name_list,
        '雇用形態': fin_employment_status_list,
        '勤務地': fin_workplace_list,
        '給与': fin_salary_list
    }

    df = pd.DataFrame(d)
    log(f'処理完了　抽出求人数：{len(df)}件　成功件数：{success}件 失敗件数：{fail}件')
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    df.to_csv(CSV_FILE_PATH.format(keyword=search_keyword, now=now), index=False, encoding='utf-8-sig')
    
if __name__ == '__main__':
    main()