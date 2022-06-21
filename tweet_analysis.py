import re
from re import X
import tweepy
from tweepy import errors
from textblob import TextBlob
import config


class TwitterClient(object):
    def __init__(self):


        try:
            self.client = tweepy.Client(bearer_token=config.bearer_token, consumer_key=config.consumer_key, 
                                        access_token=config.access_token,
                                        access_token_secret=config.access_token_secret)
        except:
            print("Authentication Failed")

    def sentiment(self, tweet):
            clean = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
            analysis = TextBlob(clean)
            if analysis.sentiment.polarity > 0:
                return 1
            elif analysis.sentiment.polarity == 0:
                return 0
            else:
                return -1
    
    def get_tweets(self, count = 10):
        query = input("Enter a query:\n")
        positive_tweets = []
        negative_tweets = []
        neutral_tweets = []

        try:
            fetched_tweets = self.client.search_recent_tweets(query=query)
            for tweet in fetched_tweets.data:
                sentiment = self.sentiment(tweet.text)
                if sentiment == 1:
                    positive_tweets.append(tweet)
                elif sentiment == 0:
                    neutral_tweets.append(tweet)
                else:
                    negative_tweets.append(tweet)

            return positive_tweets, negative_tweets, neutral_tweets
        except errors.TweepyException as e:
            print("Error: " + str(e))


def main():
    client = TwitterClient()
    pos, neg, net = client.get_tweets(count=10)
    num_tweets = len(pos) + len(neg) + len(net)

    print("Positive tweets percentage: {} %".format(100*len(pos)/num_tweets))

    print("Negative tweets percentage: {} %".format(100*len(neg)/num_tweets))

    print("Neutral tweets percentage: {} %".format(100*len(net)/num_tweets))
  
    print("\n\nPositive tweets:")
    for tweet in pos[:10]:
        print(tweet)
  
    print("\n\nNegative tweets:")
    for tweet in neg[:10]:
        print(tweet)

    print("\n\nNeutral tweets:")
    for tweet in net[:10]:
        print(tweet)
  
  
if __name__ == "__main__":
    # calling main function
    main()

                
