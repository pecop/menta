### 検索ツールサンプル
### これをベースに課題の内容を追記してください

# 検索ソース
# source=["ねずこ","たんじろう","きょうじゅろう","ぎゆう","げんや","かなお","ぜんいつ"]

# STEP3
import pandas as pd

imported_source = pd.read_csv('source.csv')

source = []

for character in imported_source['キャラクターリスト']:
    source.append(character)

### 検索ツール
def search():
    word = input("鬼滅の登場人物の名前を入力してください >>> ")
    
    ### ここに検索ロジックを書く
    
    # STEP1
    if word in source:
        print("{}が見つかりました".format(word))
    else:
        print("{}は見つかりませんでした".format(word))
        
        # STEP2
        source.append(word)
    
    # STEP4
    df_source = pd.DataFrame(source, columns=['キャラクターリスト'])
    df_source.to_csv('source_output.csv', index=None, encoding='utf_8_sig')

if __name__ == "__main__":
    search()