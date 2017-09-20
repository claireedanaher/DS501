
import json
import collections
import re
from tabulate import tabulate

# Case Study 1, Problem 2, Part 1: Word Count
# "Use the tweets you collected in Problem 1, and compute the frequencies of the words being used in these tweets."
# "Plot a table of the top 30 words with their counts."
def top30words(json_tweet_data):
    # gathers the text from each tweet into a list, all converted to lowercase
    all_tweets = []
    for tweet in json_tweet_data:
        all_tweets.append(tweet['text'].lower())
    
    # counts the number of words in each tweet's text
    bag_of_words = [collections.Counter(re.findall(r'\w+', text)) for text in all_tweets]
    # collects all words and word counts together
    bags_sum = sum(bag_of_words, collections.Counter())
    
    # loads English stopwords and removes them from bag of words
    with open("stopwords/english") as file:
        stopword_list = file.readlines()
    stopword_list = [newline.strip() for newline in stopword_list] 
    for stopword in stopword_list:
        if stopword in bags_sum:
            del bags_sum[stopword]
            
    # prints table of top 30 words and their counts
    print(tabulate(bags_sum.most_common(30), headers=['Top Words', 'Count']))
    print("\n")

# Case Study 1, Problem 2, Part 2: Find the most popular tweets in your collection of tweets
# "Please plot a table of the top 10 tweets that are the most popular among your collection, i.e., 
# the tweets with the largest number of retweet counts."
def top10retweeted(json_tweet_data):
    # gathers number of retweet counts for each tweet into a list
    retweet_counts = []
    for tweet in json_tweet_data:
        retweet_counts.append(tweet['retweet_count'])

    # finds indices of top 10 retweet counts, ordered from most to least
    top10indices = sorted(range(len(retweet_counts)), key = lambda i: retweet_counts[i])[:-11:-1]
    
    # prints table of top 10 tweets and their retweet counts
    print("\033[4mCount\tTop Tweets\033[0m\n")
    for index in top10indices:
        print(str(json_tweet_data[index]['retweet_count']) + "\t\"" + json_tweet_data[index]['text'] + "\"")
    print("\n")

# Case Study 1, Problem 2, Part 3: Find the most popular Tweet Entities in your collection of tweets
# "Please plot a table of the top 10 hashtags, top 10 user mentions that are the most popular in your 
# collection of tweets."
def top10hashtags_user_mentions(json_tweet_data):
    user_list = []
    hashtag_list = []
    
    for tweet in json_tweet_data:
        # gathers the hashtags from each tweet into a list
        hashtags = tweet['entities']['hashtags']
        if len(hashtags):
            for hashtag in hashtags:
                hashtag_list.append("#" + hashtag['text'])
        
        # gathers the users mentioned in each tweet into a list
        user_mentions = tweet['entities']['user_mentions']
        if len(user_mentions):
            for user in user_mentions:
                user_list.append("@" + user['screen_name'])

    # counts number of each hashtag
    hashtag_count = collections.Counter(hashtag_list)
    # prints table of top 10 hashtags with their counts
    print(tabulate(hashtag_count.most_common(10), headers=['Top Hashtags', 'Count']))
    print("\n")
    
    # counts number of times each user is mentioned
    user_count = collections.Counter(user_list)
    # prints table of top 10 users mentioned and their counts
    print(tabulate(user_count.most_common(10), headers=['Top Users Mentioned', 'Count']))
    
def main():
    # converts .txt file into json structure
    file = "allresults.txt"
    with open(file) as raw_data:
        parsed_data = json.load(raw_data)

    # finds indices of repeated tweets
    texts = []
    repeated_indices = []
    for index in range(len(parsed_data)):
        text = parsed_data[index]['text']
        if text in texts:
            repeated_indices.append(index)
        else:
            texts.append(text)
    
    # deletes repeated tweets
    for index in sorted(repeated_indices, reverse = True): 
        del parsed_data[index]
    
    # Case Study 1, Problem 2, all parts
    top30words(parsed_data)
    top10retweeted(parsed_data)
    top10hashtags_user_mentions(parsed_data)

if __name__ == '__main__':
    main()