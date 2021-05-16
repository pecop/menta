import requests
import urllib
import math
import datetime
import pandas as pd


# def get_api(url):
#     result = requests.get(url)
#     return result.json()
def get_api(url, payload):
    result = requests.get(url, params=payload)
    return result.json()


def test_main():
    # keyword = "鬼滅"
    # url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&keyword={}&applicationId=1019079537947262807".format(
    #     keyword)
    # print(get_api(url))

    # # STEP2
    # kwd = input("検索したいキーワードを入力してください>> ")
    # url ="https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
    # payload = {
    #     'applicationId': 1019079537947262807,
    #     'format': 'json',
    #     'keyword': kwd
    # }
    # r = get_api(url, payload)
    # count = 0
    # try:
    #     for i in r['Items']:
    #         item = i['Item']
    #         count += 1
    #         item_name = item['itemName']
    #         item_price = item['itemPrice']
    #         print(f'商品No.{count}')
    #         print(f'商品名: {item_name}')
    #         print(f'価格: {item_price}円')
    #         print('===============================================')
    # except Exception as e:
    #     print(e)

    
    ## STEP3
    # kwd = input("検索したいキーワードを入力してください>> ")
    # url ="https://app.rakuten.co.jp/services/api/Product/Search/20170426"
    # payload = {
    #     'applicationId': 1019079537947262807,
    #     'format': 'json',
    #     'keyword': kwd
    # }
    # r = get_api(url, payload)   
    # count = 0
    # try:
    #     for i in r['Products']:
    #         item = i['Product']
    #         count += 1
    #         item_name = item['productName']
    #         max_price = item['maxPrice']
    #         min_price = item['minPrice']
    #         print(f'商品No.{count}')
    #         print(f'商品名: {item_name}')
    #         print(f'最高価格: {max_price}円')
    #         print(f'最低価格: {min_price}円')
    #         print('===============================================')
    # except Exception as e:
    #     print(e)

    
    ## STEP4
    # genre = input("検索したいジャンルIDを入力してください>> ")
    url ="https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628"
    payload = {
        'applicationId': 1019079537947262807,
        # 'genreId': genre
        'genreId': 100283
    }
    r = get_api(url, payload)   
    ranking_list = []
    item_name_list = []
    item_price_list = []
    try:
        for i in r['Items']:
            item = i['Item']
            item_rank = item['rank']
            item_name = item['itemName']
            item_price = item['itemPrice']
            print(f'ランキングNo.{item_rank}')
            print(f'商品名: {item_rank}')
            print(f'価格: {item_price}円')
            print('===============================================')
            ranking_list.append(item_rank)
            item_name_list.append(item_rank)
            item_price_list.append(item_price)
    except Exception as e:
        print(e)

    ranking_dict = {
                'ランキングNo.': ranking_list,
                '商品名': item_name_list,
                '価格': item_price_list,
            }
    ranking_df = pd.DataFrame(ranking_dict)
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    ranking_df.to_csv(f'item_ranking_{now}.csv', index=False, encoding='utf-8-sig')
    ## STEP5
    assert len(ranking_df) == 30

test_main()
