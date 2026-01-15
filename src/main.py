# Pythonの勉強なしで0からコードを書いてみる wan.script555作
#今回のコードかなり簡易的なので適当なのは許してね、応用すれば自販機botとかもできます！！動かないとこあったらごめんなさい

from PayPaython_mobile import PayPay
import os

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TOKEN_PATH = os.path.join(BASE_DIR, "token.txt")

    with open("./token.txt", "r", encoding="utf-8") as file:
        line = file.read().strip()
        ACCESS_TOKEN = line.split("=", 1)[1].strip()
        #↑これはtoken.txtにACCESS_TOKEN=自分のアクセストークンと書いておくことで自動で読み込むコードです、ACCESS_TOKEN=の部分が必要ない人は上二つを削除してACCESS_TOKEN = file.read().strip()とかくと動きます

        # print(ACCESS_TOKEN)
        # ↑これはデバック用なので基本的にはコメントアウトしておいてください by wan.script555

except FileNotFoundError:
    ACCESS_TOKEN = input("自分のアクセストークンを入力してください: ")

try:
    login = PayPay(access_token=ACCESS_TOKEN)
    login.get_profile()
except Exception as e:
    print("トークンでのログインに失敗しました")
    print(e)
    exit()
else:
    print("ログイン成功")

    choice = input(
        "\n操作を選択してください\n"
        "1: 終了\n"
        "2: 送金リンク作成\n"
        "3: 請求リンク作成\n"
        "4: プロフィール表示\n"
        "5: 送金リンク受け取り\n"
        "6: 請求リンクの中身を確認する\n"
        "> "
    )

    if choice == "1":
        print("正常に終了します")
        exit()

    elif choice == "2":
        soukin = int(input("送金したい額を入力してください: "))
        password = input("パスワードが必要ですか？(はい/いいえ): ")

        if password == "はい":
            pwd = input("パスワードを入力してください: ")
            result = login.create_link(amount=soukin, passcode=pwd)
        else:
            result = login.create_link(amount=soukin)

        print("送金リンクを作成しました")
        print(result.link)

    elif choice == "3":
        seikyu = int(input("請求額を入力してください: "))
        result = login.create_p2pcode(amount=seikyu)
        print("請求リンクを作成しました")
        print(result.p2pcode)

    elif choice == "4":
        profile = login.get_profile()
        balance = login.get_balance()

        print("ユーザー名:" + profile.name)
        print("アイコンURL:" + profile.icon)
        print("合計残高:" + str(balance.all_balance))
        print("使用可能残高:" + str(balance.useable_balance))
        print("PayPayマネーライト:" + str(balance.money_light))
        print("PayPayマネー:" + str(balance.money))
        print("PayPayポイント:" + str(balance.points))

    elif choice == "5":
        input_link = input("送金リンクのURLまたはIDを入力してください: ")
        link_info=login.link_check(input_link)
        print("合計金額" + str(link_info.amount))
        print("金額のマネーライト分" + str(link_info.money_light))
        print("金額のマネー分" + str(link_info.money))
        link_pass = (link_info.has_password)
        link_status = (link_info.status)

        if link_status != "PENDING":
            print("このリンクは受け取れません。ステータス:" + link_status)
            exit()

        input_choice = input("このリンクを受け取りますか？(はい/いいえ): ")

        if input_choice == "はい":
            if link_pass:
                pwd_input = input("パスワードを入力してください: ")
                login.link_receive(input_link, pwd_input, link_info=link_info)
            else:
                login.link_receive(input_link, link_info=link_info)

        elif input_choice == "いいえ":
            print("リンクの受け取りをキャンセルしました")
            exit()

        else:
            print("無効な選択です")
            exit()

    elif choice == "6":
        link_check = input("請求リンクのURLまたはIDを入力してください: ")
        get_barcode_info=login.get_barcode_info(link_check)
        print("請求金額(Noneだった場合値段の指定なし):" + str(get_barcode_info.amount))

    else:
        print("無効な選択です")
        exit()
