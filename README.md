https://checkrelationshipoftwitteruser.herokuapp.com/

# 使い方

- 2つのtwitterアカウントを入力すると、アカウント同士のフォロー関係を確認します
- 鍵垢さん同士の場合は動きません

# git clone時にやること

$ virtualenv .

$ pip install -r requirements.txt

direnvなどで環境変数にTwitterAPIkeyを配置
```
export CONSUMER_KEY="**************"
export CONSUMER_SECRET="**************"
export ACCESS_TOKEN="**************"
export ACCESS_TOKEN_SECRET="**************"
```