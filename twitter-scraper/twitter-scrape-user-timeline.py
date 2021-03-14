import tweepy

# Twitter developer account application tokens
consumer_key = '<consumer_key>'
consumer_secret = '<consumer_secret_key>'
access_token = '<access_token>'
access_token_secret = '<access_token_secret>'

# Twitter API authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweets = []

# Asking user for input / CLI
print('Enter twitter username:')
username = input()
print('How many tweets do you want to get?:')
# Validating input
try:
    items_count = int(input())
except:
    print('Invalid value. It has to be a number. Exiting the programme...')
    exit(0)
print('Name of the file for saving ' + username + "'s tweets")
file_name = input()

tweet_count = 1

# Going through every status of that user until enough tweets are found
for status in tweepy.Cursor(api.user_timeline, screen_name = username, tweet_mode = 'extended').items(50000):
    # Processing every status
    # Ignoring retweets and replies
    if status.full_text[:2] == 'RT' or status.full_text[:1] == '@':
        continue
    # If the status is not a retweet then we append it to the tweets list
    else:
        print('Saving tweet no ' + str(tweet_count))
        tweets.append(status.full_text.strip())
        tweet_count += 1

    # Break the loop when enough tweets are found
    if tweet_count == items_count + 1:
        break

# Saving the text content of found tweets to a .txt file
f = open(file_name + '.txt', 'w', encoding = 'utf-8')
line = ''
for i, tweet in enumerate(tweets):
    f.write(('Tweet no ' + str(i+1) + '\n'))
    f.write(tweet.strip())
    f.write('\n')
    f.write('\n')
f.close()