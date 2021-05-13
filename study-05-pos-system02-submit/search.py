import pandas as pd
import eel

### デスクトップアプリ作成課題
# STEP6
def kimetsu_search(word, csv_file):
    # 検索対象取得
    df=pd.read_csv(f"./{csv_file}")
    # df=pd.read_csv("./source.csv")
    source=list(df["name"])

    # 検索
    if word in source:
        print(f"『{word}』はいります")
        # STEP3
        eel.view_log_js(f"『{word}』はいます")
    else:
        print(f"『{word}』はいません")
        eel.view_log_js(f"『{word}』はいません")
        # 追加
        #add_flg=input("追加登録しますか？(0:しない 1:する)　＞＞　")
        #if add_flg=="1":
        source.append(word)
    
    # CSV書き込み
    df=pd.DataFrame(source,columns=["name"])
    df.to_csv("./source.csv",encoding="utf_8-sig")
    print(source)
