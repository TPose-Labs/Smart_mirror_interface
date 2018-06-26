from tkinter import Label
from tkinter.font import Font
import datetime
import calendar
import twitter
import html
import re
import utils
import time

class Module:

    def __init__(self, root):
        self.root = root

    def pack(self, side=None):
        self.root.pack(side=side)

class ClockModule(Module):

    def __init__(self, root):
        super(ClockModule, self).__init__(root)

        font_big = Font(family="Helvetica", size=72)
        font_small = Font(family="Helvetica", size=48)

        self.day = Label(root, font=font_big, fg="white", bg="black",
                         padx=5)
        self.day.grid(row=0, sticky="w")
        self.fulldate = Label(root, font=font_small, fg="white",
                              bg="black", padx=5)
        self.fulldate.grid(row=1, column=0, sticky="w")
        self.clock = Label(root, font=font_small, fg="white", bg="black",
                           padx=5)
        self.clock.grid(row=2, column=0, sticky="w")

        self.time = ""
        self.dotw = ""
        self.date = ""
        self.loop()

    def loop(self):
        currday = datetime.datetime.today()
        dotw = calendar.day_name[currday.weekday()] + ","
        date = currday.strftime("%B %d, %Y")
        time = currday.strftime("%I:%M %p")
        if self.time != time:
            self.time = time
            self.clock.config(text=time)
        if self.dotw != dotw:
            self.dotw = dotw
            self.day.config(text=dotw)
        if self.date != date:
            self.date = date
            self.fulldate.config(text=date)
        self.day.after(1000, self.loop)

class TwitterModule(Module):

    def __init__(self, root):
        super(TwitterModule, self).__init__(root)

        font_big = Font(family="Helvetica", size=36)
        font_small = Font(family="Helvetica", size=24)

        self.api = twitter.Api(consumer_key="E7YJ1iuJRp5HETovcuc9d4h39",
                          consumer_secret="45OupqmRLbNLxYY4o40nXmE29CfKYXAowohUSIL30cn4TUopR1",
                          access_token_key="4100343689-6o2O0WKj3V8ZEuPfJOm86TOVi0Ri5pHfVBR52d6",
                          access_token_secret="dqVbh5ARQbxDgjKdo6yLAaGy8jhOVzQbpByuwAG38DlNP")
        self.text_top = Label(root, font=font_big, fg="white", bg="black",
                         padx=5)
        self.text_top.grid(row=0)
        self.text_bot = Label(root, font=font_big, fg="white", bg="black",
                         padx=5)
        self.text_bot.grid(row=1)
        self.counter = 0
        self.loop()

    def loop(self):
        timeline = self.api.GetHomeTimeline()
        self.timeline = [TwitterModule.process(tweet) for tweet in timeline]
        self.loop_helper()
        self.text_top.after(1000*60*60, self.loop)

    def loop_helper(self):
        if self.counter >= len(self.timeline):
            self.counter = 0
        tweet = self.timeline[self.counter]
        print(tweet)
        self.text_top.config(text=tweet[0])
        self.text_bot.config(text=tweet[1])
        self.counter += 1
        self.text_top.after(20000, self.loop_helper)

    @staticmethod
    def process(tweet):
        removed_url = re.sub(r'http\S+', '', tweet.text)
        processed_text = html.unescape(removed_url)
        text = TwitterModule.remove_unicode(processed_text)
        tweet_user = tweet.user.screen_name
        tweet_time = TwitterModule.process_tweet_time(tweet.created_at)
        return "Posted by @{} on {}:".format(tweet_user, tweet_time), text

    @staticmethod
    def process_tweet_time(tweet_time):
        time_split = tweet_time.split(" ")
        day = utils.DAYS[time_split[0]]
        month = utils.MONTHS[time_split[1]]
        raw_time = time_split[3][:5]
        if int(raw_time[:2]) < 12:
            time = raw_time[:5] + " am"
        else:
            time = raw_time[:5] + " pm"
        if time[0] == "0":
            time = time[1:]
        return "{}, {} {} at {}".format(day, month, time_split[2],
                                        time)

    @staticmethod
    def remove_unicode(tweet):
        char_list = [tweet[j] for j in range(len(tweet)) if ord(tweet[j]) in range(65536)]
        tweet=''
        for j in char_list:
            tweet=tweet+j
        return tweet
