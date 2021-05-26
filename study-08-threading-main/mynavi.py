# STEP3~4
import os
import time
import datetime
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import threading

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

def extract(driver, page, exp_name_list, fin_employment_status_list, fin_workplace_list, fin_salary_list, success, fail):
    log(f'{page}ページ目抽出スタート')

    # ページ終了まで繰り返し取得
    count = 1

    # 検索結果の1頁分の全求人情報を取得
    name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
    employment_status_list = driver.find_elements_by_class_name('labelEmploymentStatus')
    table_list = driver.find_elements_by_class_name('tableCondition')

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


def output_file(exp_name_list, fin_employment_status_list, fin_workplace_list, fin_salary_list, success, fail, search_keyword):
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

def main():
    log('処理開始')
    search_keyword = input("検索したいキーワードを入力してください：")
    log(f'検索キーワード：{search_keyword}')

    multi_threads = ['driver1', 'driver2', 'driver3']
    n_threads = int(input("ご希望のスレッド数（1〜3）を入力してください："))
    log(f'スレッド数：{n_threads}')

    url = "https://tenshoku.mynavi.jp/"
    
    # Chromeを立ち上げる
    for i in range(0, n_threads):
        if os.name == 'nt': #Windows
            multi_threads[i] = set_driver("chromedriver.exe", False)
        elif os.name == 'posix': #Mac
            multi_threads[i] = set_driver("chromedriver", False)

    # Webサイトを開く
    multi_threads[0].get(url)
    time.sleep(5)

    # ポップアップを閉じる
    close_popup(multi_threads[0])

    # 指定キーワードで検索
    search(multi_threads[0], search_keyword)

    # グローバル変数定義
    exp_name_list = []
    fin_employment_status_list = []
    fin_workplace_list = []
    fin_salary_list = []
    success = 0
    fail = 0
    page = 1

    start_time = time.time()

    ## データ抽出
    # while True:
    while page <6:
        # スレッド数が1つの場合
        if n_threads == 1:
            while page <= 6:
                extract(multi_threads[0], page, exp_name_list, fin_employment_status_list, fin_workplace_list, fin_salary_list, success, fail)
                next_page = multi_threads[0].find_elements_by_class_name('iconFont--arrowLeft')
                if len(next_page) > 0:
                    page += 1
                    url = next_page[0].get_attribute('href')
                    multi_threads[0].get(url)
                else:
                    break

        # スレッド数が2つ以上の場合
        else:
            # スレッド1（1頁目）
            if page == 1:
                thread = threading.Thread(target=extract, args=(multi_threads[0], page, exp_name_list, fin_employment_status_list, fin_workplace_list, fin_salary_list, success, fail))
                thread.start()
                next_page = multi_threads[0].find_elements_by_class_name('iconFont--arrowLeft')
            # スレッド1（3頁以降）
            elif len(next_page) > 0:
                    page += 1
                    url = next_page[0].get_attribute('href')
                    multi_threads[0].get(url)
                    thread = threading.Thread(target=extract, args=(multi_threads[0], page, exp_name_list, fin_employment_status_list, fin_workplace_list, fin_salary_list, success, fail))
                    thread.start()
            else:
                break
            # スレッド2
            if len(next_page) > 0:
                page += 1
                url = next_page[0].get_attribute('href')
                multi_threads[1].get(url)
                thread = threading.Thread(target=extract, args=(multi_threads[1], page, exp_name_list, fin_employment_status_list, fin_workplace_list, fin_salary_list, success, fail))
                thread.start()
                next_page = multi_threads[1].find_elements_by_class_name('iconFont--arrowLeft')
            else:
                break
            # スレッド3
            if n_threads == 3:
                if len(next_page) > 0:
                    page += 1
                    url = next_page[0].get_attribute('href')
                    multi_threads[2].get(url)
                    thread = threading.Thread(target=extract, args=(multi_threads[2], page, exp_name_list, fin_employment_status_list, fin_workplace_list, fin_salary_list, success, fail))
                    thread.start()
                    next_page = multi_threads[2].find_elements_by_class_name('iconFont--arrowLeft')
                else:
                    break

            thread_list = threading.enumerate()
            thread_list.remove(threading.main_thread())
            if len(thread_list) > 1:
                for thread in thread_list:
                    thread.join()

    elapsed_time = time.time() - start_time
    log(f'スクレイピング速度（スレッド数-{n_threads}）：{elapsed_time}秒')

    # ブラウザを閉じる
    for i in range(1, n_threads):
        multi_threads[i].quit()

    # 抽出データのファイル出力
    output_file(exp_name_list, fin_employment_status_list, fin_workplace_list, fin_salary_list, success, fail, search_keyword)
    
if __name__ == '__main__':
    main()