import tweepy
import time
import secret
import random

auth = tweepy.OAuthHandler(secret.word["CK"], secret.word["CS"])
auth.set_access_token(secret.word["AT"], secret.word["AS"])

api = tweepy.API(auth)

friends = api.friends_ids()
unfollow_cnt = 0

# 古い順から
for f in friends[::-1]:
    # 100人削除
    if unfollow_cnt <= 100:
        print("{0}".format(api.get_user(f).screen_name))
        api.destroy_friendship(f)
        waitsec1 = random.uniform(3.1, 10)
        print(str(waitsec1) + "秒後に処理を開始します")
        time.sleep(waitsec1)
        unfollow_cnt += 1
        print(unfollow_cnt)
    else:
        print("終了")
        break
