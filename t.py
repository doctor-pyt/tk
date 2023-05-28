import time
import secret
import tweepy
import re
import random

auth = tweepy.OAuthHandler(secret.word["CK"], secret.word["CS"])
auth.set_access_token(secret.word["AT"], secret.word["AS"])

api = tweepy.API(
    auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, timeout=1800
)

users = ["potitto_tousen"]

pattern = re.compile(
    r"サイン色紙|サイン入り|サイン入りポラ|サイン本|フリップ|チェキ|直筆|描き下ろし|入園券|サインボール|色紙|原画|試写|来店|ポスター|書店用|ムビチケ|鑑賞券|制作舞台|初回放送配信|プロップ|台本プレゼント"
)
pattern2 = re.compile(r"giftee.biz|dgift|petitgift")

while True:
    for user in users:
        for status in tweepy.Cursor(
            api.user_timeline, id=user, exclude_replies=True, tweet_mode="extended"
        ).items(60):
            # print(user)
            # リツイートか
            if hasattr(status, "retweeted_status") == False:
                print("リツイートではない\n----------")
                continue

            # リツイート済みか
            if status.retweeted_status.retweeted == True:
                print("リツイート済\n----------")
                continue

            # 除外キーワードがふくまれているか
            if pattern.search(status.retweeted_status.full_text) != None:
                print("除外キーワード対象\n----------")
                continue

            tweet_id = status.retweeted_status.id_str
            user_id = status.entities["user_mentions"][0]["id"]

            time.sleep(random.uniform(3.1, 10))

            try:
                # フォロー処理
                user = api.get_user(user_id)
                if user.following == False:
                    api.create_friendship(user_id)
                    time.sleep(random.uniform(3.1, 10))
                else:
                    time.sleep(random.uniform(3.1, 10))
                # print(user.name, user.following)

                # RT処理
                api.retweet(tweet_id)

                # Fav処理
                if len(status.retweeted_status.entities["urls"]) != 0:
                    for urlitem in status.retweeted_status.entities["urls"]:
                        if pattern2.search(urlitem["expanded_url"]) != None:
                            api.create_favorite(tweet_id)
                            break

                print(status.retweeted_status.full_text + "\n----------")

                time.sleep(random.uniform(3.1, 10))

            except Exception as e:
                print(e.args)

    time.sleep(random.uniform(10.1, 20))
