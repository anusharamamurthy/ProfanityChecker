from profanitychecker import ProfanityChecker
import json
import sys

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print("Missing Argument")
        print("usage: python init.py <bad_words_file_name> <data_file_name> <Show_flagged_words_True/False>")
        exit()

    bad_words = sys.argv[1]
    file_name = sys.argv[2]
    show_flag = sys.argv[3] == "True"

    # bad_words = "profanity_en.txt"
    # file_name = "data/tweets.json"
    # show_flag = True

    prof_check = ProfanityChecker(bad_words) #profanity_en.txt

    tweets = []

    with open(file_name, 'r') as file:
            for line in file:
                tweet = json.loads(line)
                tweets.append(tweet["text"])

    cntr = 0
    for tweet in tweets:
        flagged_words = prof_check.test_membership(tweet)
        if len(flagged_words) == 0:
            cntr += 1
        else:
            if show_flag:
                print(flagged_words)

    print("Total tweets: %d\nTweets not flagged for profanity: %d" % (len(tweets), cntr))
