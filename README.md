

# 利用シーン
- 結婚式/披露宴の出し物（クイズ大会を想定）

# 開発環境での実行方法
1. 環境変数設定
```
export LINE_CHANNEL_ACCESS_TOKEN=XXXX
export LINE_CHANNEL_SECRET=XXXX
export TEST_USER_LINE_ID=XXXX(自分のLINE USER ID)を使う
```
2. `python ./manage.py runserver`でlocalhost:8000のurlで起動される
3. ngrokを起動して`ngrok http 8000`を実行し、8000ポートに穴を開ける
4. `python manage.py push_question \d{1}`で登録済みユーザにPUSH通知する（ngrok）



# 利用方法
1. 参加者が対象botをフォローする
2. 司会者がクイズを読む・裏方が問題をPUSH通知
3. 対象botから問題が届く
4. 問題を解き、選択肢のボタンを押下する
5. 回答のタイミングで裏方が解答をPUSH通知
6. 2-5を問題数分繰り返す

# おまけ
- 内輪ネタ関数を用意し、特定の発話に対して個別のネタ発言をするように仕込む
