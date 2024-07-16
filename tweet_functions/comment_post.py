# URL for the CreateTweet endpoint
import requests

# this is the function that we call when we want to send comment
url = 'https://x.com/i/api/graphql/oB-5XsHNAbjvARJEc8CZFw/CreateTweet'


def send_comment(text: str, post_id: str, channel_name: str) -> str:
    """
    add text you want to send as comment and post id you want to send image to
    the channel name that we are going to send message to :param channel_name:
    the text that we are going to send to tweet :param text:
    the post id that we are going to reply comment under it:param post_id:
    this will return link of webpage else it will return false :return:
    """
    # this is cookies when you want to run it on the web and save data on client you can use cookies
    cookies = {
        'auth_token': 'ac02ad63410fdcb83f8b3993f9d2f9582018f120',
        'ct0': 'cb0580831790827912a0cf7ad1ae2a6c8a1135aebc340ca60eca18f06f7a28fd654f70585aa3675f8890de9eae0565b7f287243fab23937370979db26007bf14ebe118ca83e2ef86d9fa1e22e12fb304	',
        'd_prefs': 'MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw',
        'des_opt_in': 'Y',
        'dnt': '1',
        'g_state': '{"i_l":0}',
        "guest_id": 'v1%3A172091662864390487',
        'kdt': 'gJHUeGHPIok2rwBLt0h6aTuzJjWN8BpSatvvSqPQ',
        'lang': 'en',
        'night_mode': '2',
        'twid': 'u%3D1806779267663138816'
    }

    # this is header our configs and setting go there
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.5',
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'Content-Length': '1432',
        'Content-Type': 'application/json',
        'Cookie': 'guest_id=v1%3A172091662864390487; night_mode=2; kdt=gJHUeGHPIok2rwBLt0h6aTuzJjWN8BpSatvvSqPQ; auth_token=ac02ad63410fdcb83f8b3993f9d2f9582018f120; ct0=cb0580831790827912a0cf7ad1ae2a6c8a1135aebc340ca60eca18f06f7a28fd654f70585aa3675f8890de9eae0565b7f287243fab23937370979db26007bf14ebe118ca83e2ef86d9fa1e22e12fb304; twid=u%3D1806779267663138816; lang=en; d_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw',
        'Origin': 'https://x.com',
        'Priority': 'u=1, i',
        'Referer': f'https://x.com/{channel_name}/status/{post_id}',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': "Windows",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Gpc': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'X-Client-Transaction-Id': 'nqXk2313OQNAJsobgR8ri5nPRCIQ4uXKojirRIz5k9NuD6H/qRXdmnYqoeVxSoU0DX672ZxlZmXuifi6Pr91yhi8ps5znQ',
        'X-Client-Uuid': 'b53135cd-091a-41b3-8226-c3d481b926a4',
        'X-Csrf-Token': 'cb0580831790827912a0cf7ad1ae2a6c8a1135aebc340ca60eca18f06f7a28fd654f70585aa3675f8890de9eae0565b7f287243fab23937370979db26007bf14ebe118ca83e2ef86d9fa1e22e12fb304',
        'X-Twitter-Active-User': 'yes',
        'X-Twitter-Auth-Type': 'OAuth2Session',
        'X-Twitter-Client-Language': 'en',
    }

    # this is payload all inputs go there
    payload = {
        "variables": {
            "tweet_text": f"{text}",
            "reply": {
                "in_reply_to_tweet_id": f"{post_id}",
                "exclude_reply_user_ids": []
            },
            "dark_request": False,
            "media": {
                "media_entities": [],
                "possibly_sensitive": False
            },
            "semantic_annotation_ids": []
        },
        "features": {
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "tweetypie_unmention_optimization_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "articles_preview_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        },
        "queryId": "oB-5XsHNAbjvARJEc8CZFw"
    }

    # run request and post data to server
    data = requests.post(url, json=payload, headers=headers, cookies=cookies)

    # print data to visualize everything we get
    print(data.status_code)
    print(data.json())
    # this will return post link
    if data.status_code == 200:
        return f"https://x.com/{channel_name}/status/{post_id}"
    else:
        return "not working may you written comment twice"



