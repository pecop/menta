### 検索ツールサンプル
### これをベースに課題の内容を追記してください

# 検索ソース
# source=["ねずこ","たんじろう","きょうじゅろう","ぎゆう","げんや","かなお","ぜんいつ"]

# STEP3
import pandas as pd

# csvの読み込み
def read_csv(csv_file):
    imported_source = pd.read_csv(csv_file)
    source_list = []
    for character in imported_source['キャラクターリスト']:
        source_list.append(character)
    return source_list

### 検索ツール
def search(source_list):
    word = input("鬼滅の登場人物の名前を入力してください >>> ")
    
    ### ここに検索ロジックを書く
    # STEP1
    if word in source_list:
        print(f"{word}が見つかりました")
    else:
        print(f"{word}は見つかりませんでした")
        
        # STEP2
        source_list.append(word)
    
    # STEP4
    df_source = pd.DataFrame(source_list, columns=['キャラクターリスト'])
    df_source.to_csv('source_output.csv', index=None, encoding='utf_8_sig')

if __name__ == "__main__":
    source_list = read_csv('source.csv')
    search(source_list)