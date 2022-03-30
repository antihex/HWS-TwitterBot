#Program to tweet deals on r/hardwareswap
#Zachary Conger
3/30/2022

from EbayScraper import *
from Info import *
import time
import tweepy

#makes only numbers in string
def de_letter(text):
    return "".join(c for c in text if c.lower() in '$1234567890., ')


# authentication of consumer key and secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# authentication of access token and secret
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

bad_items = ["apple", "phone", "mac", "ps5", "xbox", "laptop", "keyboard", "earbuds", "ipad" , "galaxy", "thinkpad", "pixel", "doorbell"]      #unprofitable items

ids = []    #list of ids so double checking doesn't happen.

printFlag = True

count = 3    #How many posts to be check at a time. >=1 
index = 0    #index in ids (used to preserve mem) (keep as 0)

ids = [0 for i in range(count*2)]

custom_ON = False    #look for just broken parts

while(1):                                       #infinate loop
    try:
        subreddit = reddit.subreddit("hardwareswap")
        for submission in subreddit.new(limit=count):        
            id = submission.id
            if not id in ids:                           #checking if already checked
                ids[index] = id
                index = index + 1

                if (index > count * 2 - 1):                 #Resets Index Value
                    index = 0
                bad = False
                title_lower = submission.title.lower()

                if ("paypal" in title_lower and submission.link_flair_text == "SELLING"):       #Find if selling buy shipping and selling

                    for i, j in enumerate(bad_items):       #check if item is bad     
                        if(j in title_lower):
                            bad = True
                            break

                    broken_part = False
                    if custom_ON:
                        if("broken" in title_lower):
                            broken_part = True
                        else:
                            broken_part = False

                    if not bad and (not custom_ON or broken_part):
                        tweet = []                                      # reset tweet every loop
                        list_of_words = title_lower.split()             # split title into list of words

                        for i, w in enumerate(list_of_words):           # find what they have 
                            if "[h]" in w:
                                start = i+1
                                items = [i+1]
                            if "," in w or ";" in w:
                                items.append(i)                             # when new item
                            if " and " in w:
                                items.append(i-1)
                                list_of_words.remove("and ")
                            if " & " in w:
                                items.append(i-1)
                                list_of_words.remove("& ")
                                
                            if "[w]" in w:
                                items.append(i-1)
                                end = i
                                items = list(dict.fromkeys(items))
                                break

                        num_in_list = len(items)
                        list_of_items = []
                        items_ = []
                        

                        for i, j in enumerate(items):  
                            try:
                                if not i == 0:
                                    items_ = []

                                    for x in range (items[i-1]+1, items[i]+1):
                                        items_.append(list_of_words[x])  
                                    list_of_items.append(" ".join(items_))                                                  # create new part of list for each begin to end in the "list of words"
                                    list_of_items[i-1] = list_of_items[i-1].replace(',','',1)                               # remove ,s and ;s
                                    list_of_items[i-1] = list_of_items[i-1].replace(';','',1)
                                else:
                                    items[0] = items[0]-1
                            except:
                                print("error invalid title")
                                printFlag = False       



                        body_lower = submission.selftext.lower()            # splits the body text

                        body_lower = body_lower.replace(',' , '')
                        body_lower = body_lower.replace(';' , ' ')          # makes body easier to parse
                        body_lower = body_lower.replace(':' , ' ')
                        body_lower = body_lower.replace('~' , ' ')
                        body_lower = body_lower.replace('-' , ' ')
                        body_lower = body_lower.replace('|' , ' ')
                        body_lower = body_lower.replace('(' , ' ')
                        body_lower = body_lower.replace('[' , ' ')
                        body_lower = body_lower.replace('{' , ' ')
                        body_lower = body_lower.replace(')' , ' ')
                        body_lower = body_lower.replace(']' , ' ')
                        body_lower = body_lower.replace('}' , ' ')

                        list_body_words = body_lower.split()
                        list_BODY = submission.selftext.split()
                        list_of_prices = []
                        imgur = []                                                                                              #sets imgur to blank if not found

                        for i, j in enumerate(list_body_words):                                                                     # searches for $ 
                            if (i != len(list_body_words)-1):
                                if ("$" in j and not "local" in list_body_words[i+1] and not "local" in list_body_words[i-1]):
                                    list_of_prices.append(list_body_words[i])                                                                               # adds the word to the list of prices


                                if "usd" in j and not "local" in list_body_words[i+1] and not "local" in list_body_words[i-2]:                              # second way of writing price
                                    list_of_prices.append("$"+list_body_words[i-1])


                            #if "imgur" in j:
                            #    imgur.append(list_BODY[i])                          #Finding Timestamp

                        imgur = " ".join(imgur)
                                                                        #formating Text
                        #print(parse(list_of_items))


                        product = " | ".join(list_of_items)
                        list_of_prices = ", ".join(list_of_prices)
                        list_of_prices = de_letter(list_of_prices)

                        tweet.append(product)                                       # creating Tweet
                        
                        for i, j in enumerate(list_of_items):
                            eproxPrice = "~Ebay Price: $" + str(round(parse(j)))      # Eproximate Prices found on Ebay
                            tweet.append(eproxPrice)
                        

                        tweet.append(list_of_prices)
                        tweet.append(submission.url)
                        # tweet.append(imgur)
                        tweet = '\n'.join(tweet)

                        print(tweet)
                        
                        if("a lot of" in product or "cpus" in product):
                            tweet = "BULK: " + submission.url

                        if("combo" in product):
                            tweet = "C-C-C-COMBO: " + submission.url


                        if(len(tweet) > 280): 

                            if(len(submission.url) < 280):      
                                tweet = (submission.url)                         #Test if tweet is too long
                            else:
                                print("\n\nERROR TWEET TOO LARGE\n\n")

            
                                    #Consol GUI Debugging
                        #print("*****************************************")  
                        print('\a') #bell sound
                        #print(product)
                        #print(list_of_prices)    
                        #print(submission.url)
                        #print(imgur)
                        #print('\n')
                        print("------------------------------------------")  
                        #print('\n')
                        #                        ##debuging
                        print(submission.title)
                        print(submission.selftext)
                        print('\n')
                        #print('\n')
                        if printFlag:
                            try:
                                api.update_status(status = tweet)       #TWEET
                                #true = true
                            except:
                                print("Would be a retweet\n")
                        else:
                            printFlag = True
                    else:
                        print("ewwwww")
                        print(submission.title)
                        print('\n')
                else:
                    print("Not selling: " + submission.title + "\n")
            else:
                #print("No new posts \n")
                time.sleep(1)
    except:
        print("error")
        time.sleep(1000)
        print("trying again...")            