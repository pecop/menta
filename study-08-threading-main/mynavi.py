# STEP3~4
import os
import time
import datetime
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import threading
import re
import math

LOG_DIR = './log/'
URL = "https://tenshoku.mynavi.jp/"
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
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
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logStr = f'[{now}] {text}'   
    with open(LOG_FILE_PATH, 'a', encoding='utf-8-sig') as f:
        f.write(logStr + '\n')    
    print(logStr)

def close_popup(driver):
    try:
        # ポップアップを閉じる
        while driver.find_element_by_class_name("karte-close"):
            driver.execute_script('document.querySelector(".karte-close").click()')
            time.sleep(5)
    except:
        pass

def search(driver, search_keyword):
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

def extract(driver, n_threads, i):
    # 変数定義
    exp_name_list = []
    fin_employment_status_list = []
    fin_workplace_list = []
    fin_salary_list = []
    success = 0
    fail = 0
    page = i
    opps_per_page = 50
    
    # 全ヒット数取得
    total_opps_element = driver.find_elements_by_class_name('result__num')
    total_opps = total_opps_element[0].find_elements_by_tag_name('em')
    total_page = math.ceil(int(total_opps[0].text) / opps_per_page)
    while True:
        if total_page >= page:
            next_page_element = driver.find_elements_by_class_name('iconFont--arrowLeft')
            url_element = next_page_element[0].get_attribute('href')
            next_page_url = re.sub('pg\d{1,}', f'pg{page}', url_element)
            driver.get(next_page_url)
            time.sleep(5)

            log(f'{page}ページ目抽出スタート')

            # ページ終了まで繰り返し取得
            count = 1

            # 検索結果の1頁分の全求人情報を取得
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
                        log(f'{page}ページ目{count}件目抽出完了')       
                    except:
                        fail += 1
                        log(f'{page}ページ目{count}件目抽出失敗')         
                    finally:
                        count += 1

            log(f'{page}ページ目抽出完了')
            page += n_threads
        else:
            break

    driver.quit()
    return exp_name_list, fin_employment_status_list, fin_workplace_list, fin_salary_list, success, fail

def output_file(exp_name_list, fin_employment_status_list, fin_workplace_list, fin_salary_list, success, fail, search_keyword):
    d = {
        '会社名': exp_name_list,
        '雇用形態': fin_employment_status_list,
        '勤務地': fin_workplace_list,
        '給与': fin_salary_list
    }

    df = pd.DataFrame(d)
    log(f'処理完了　抽出求人数：{len(df)}件　成功件数：{success}件 失敗件数：{fail}件')
    file_name = CSV_FILE_PATH.format(keyword=search_keyword, now=now)
    if os.path.exists(file_name):
        df.to_csv(file_name, index=False, header=False, encoding='utf-8-sig', mode='a')
    else:
        df.to_csv(file_name, index=False, encoding='utf-8-sig', mode='a')
        

def multi_thread(search_keyword, n_threads, i):
    # Chromeを立ち上げる
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)

    # Webサイトを開く
    driver.get(URL)
    time.sleep(5)

    # ポップアップを閉じる
    close_popup(driver)

    # 指定キーワードで検索
    search(driver, search_keyword)

    ## データ抽出
    exp_name_list, fin_employment_status_list, fin_workplace_list, fin_salary_list, success, fail = extract(driver, n_threads, i)

    # 抽出データをファイル出力
    output_file(exp_name_list, fin_employment_status_list, fin_workplace_list, fin_salary_list, success, fail, search_keyword)

def main():
    log('処理開始')

    # 検索キーワード指定
    search_keyword = input("検索したいキーワードを入力してください：")
    log(f'検索キーワード：{search_keyword}')

    # スレッド数指定
    # multi_threads = ['driver1', 'driver2', 'driver3']
    n_threads = int(input("ご希望のスレッド数を入力してください："))
    log(f'スレッド数：{n_threads}')
    
    # スタート時間記録
    start_time = time.time()

    #スレッド実行
    threads = []
    for i in range(1, n_threads + 1):
        threads.append(threading.Thread(target=multi_thread, args=(search_keyword, n_threads, i)))
        threads[i-1].start()

    # 全てのスレッド終了待ち
    thread_list = threading.enumerate()
    thread_list.remove(threading.main_thread())
    for thread in thread_list:
        thread.join()

    # スクレイピング速度計測
    elapsed_time = time.time() - start_time
    elapsed_time = round(elapsed_time, 1)
    log(f'スクレイピング速度（スレッド数：{n_threads}）：{elapsed_time}秒')
    
if __name__ == '__main__':
    main()