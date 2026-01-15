# Pythonの勉強なしで0からコードを書いてみる wan.script555作
#このコードはもともとあったのをマジで少しだけ改変したものです()
#自分のpcでこのモジュールをインストールするのは少しだけ面倒くさいかも？？gitのインストール方法はググってね！！

from paypaypy import PayPay
import os

PHONE_NUMBER = input("電話番号を入力してください")
PASSWORD = input("パスワードを入力してください")

def main():
    paypay = PayPay()

    try:
        paypay.login_start(PHONE_NUMBER, PASSWORD)
    except:
        print("ログインに失敗しました")
        return
    
    url = input("メッセージアプリに送信されたurlを入力してください。※urlには絶対にアクセスしないでください。")

    try:
        paypay.login_confirm(url)
    except:
        print("ログインに失敗しました")
        return

    print("ログインに成功しました")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TOKEN_PATH = os.path.join(BASE_DIR, "token.txt")

    with open("./token.txt", "w", encoding="utf-8") as file:
        file.write("ACCESS_TOKEN = " + paypay.access_token)
        print("トークンをtoken.txtに保存しました")

if __name__ == "__main__":
    main()
