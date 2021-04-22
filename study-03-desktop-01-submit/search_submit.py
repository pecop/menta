import pandas as pd
import eel

### デスクトップアプリ作成課題
# STEP6
def kimetsu_search(word, csv_file):
    # 検索対象取得
    df=pd.read_csv("./{}".format(csv_file))
    # df=pd.read_csv("./source.csv")
    source=list(df["name"])

    # 検索
    if word in source:
        print("『{}』はいります".format(word))
        # STEP3
        eel.view_log_js("『{}』はいます".format(word))
    else:
        print("『{}』はいません".format(word))
        eel.view_log_js("『{}』はいません".format(word))
        # 追加
        #add_flg=input("追加登録しますか？(0:しない 1:する)　＞＞　")
        #if add_flg=="1":
        source.append(word)
    
    # CSV書き込み
    df=pd.DataFrame(source,columns=["name"])
    df.to_csv("./source.csv",encoding="utf_8-sig")
    print(source)
