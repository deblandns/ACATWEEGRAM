import requests

url = "https://twitter154.p.rapidapi.com/user/tweets"

querystring = {"username": "@ACATWEEGRAM", "limit": "1", "user_id": "1806779267663138816", "include_replies": "false", "include_pinned": "false"}

headers = {
	"x-rapidapi-key": "b2ca57fd49mshcceaec273d8e2a0p143921jsn9a2a5cf40ef4",
	"x-rapidapi-host": "twitter154.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data = response.json()
tweet_id = data['results'][0]['tweet_id']
tweet_title = data['results'][0]['text']
channel_name = data['results'][0]['user']['username']
follower_count = data['results'][0]['user']['follower_count']
media_url = data['results'][0]['media_url']
print(f"tweet_id:{tweet_id}")
print(f"tweet_title:{tweet_title}")
print(f"channel_name:{channel_name}")
print(f"follower_count:{follower_count}")
print(f"media_url:{media_url}")
