https://checkrelationshipoftwitteruser.herokuapp.com/

# 使い方

- 2つのtwitterアカウントを入力すると、アカウント同士のフォロー関係を確認します
- 鍵垢さん同士の場合は動きません

# git clone時にやること

$ virtualenv .

$ pip install -r requirements.txt

`config.py` を作成してTwitterAPIkeyを配置
```
CONSUMER_KEY = "**************"
CONSUMER_SECRET = "**************"
ACCESS_TOKEN = "**************"
ACCESS_TOKEN_SECRET = "**************"
```