from tkinter import Label, CENTER
from tkinter.font import Font
from weather import Weather, Unit
from dotenv import load_dotenv
from os.path import join, dirname
import datetime
import calendar
import twitter
import html
import re
import utils
import os


class Module:

    def __init__(self, root):
        self.root = root

    def pack(self, side=None):
        self.root.pack(side=side)

    def grid(self, row=0, column=0):
        self.root.grid(row=row, column=column)


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


class WeatherModule(Module):

    def __init__(self, root):
        super(WeatherModule, self).__init__(root)

        font_big = Font(family="Helvetica", size=72)
        font_small = Font(family="Helvetica", size=48)

        self.temp_label = Label(root, font=font_big, fg="white", bg="black",
                                padx=5)
        self.temp_label.grid(row=0, sticky="w")
        self.cond_label = Label(root, font=font_big, fg="white",
                                bg="black", padx=5)
        self.cond_label.grid(row=1, column=0, sticky="w")
        self.forecasts_label = Label(root, font=font_small, fg="white", bg="black",
                                     padx=5)
        self.forecasts_label.grid(row=2, column=0, sticky="w")

        self.temp = ""
        self.cond = ""
        self.forecasts = []
        self.loop()

    def list_forecasts(self):
        forecast_list = ""
        for forecast in self.forecasts:
            forecast_list = forecast_list + forecast.date + ": " + forecast.text + ", "
        return forecast_list

    def loop(self):
        weather = Weather(unit=Unit.FAHRENHEIT)
        location = weather.lookup(12784268)
        currweather = location.condition
        temp = currweather.temp
        cond = currweather.text
        forecasts = location.forecast
        if self.temp != temp:
            self.temp = temp
            self.temp_label.config(text=temp)
        if self.cond != cond:
            self.cond = cond
            self.cond_label.config(text=cond)
        if self.forecasts != forecasts:
            self.forecasts = forecasts
            self.forecasts_label.config(text=self.list_forecasts())
        self.temp_label.after(1000, self.loop)


class TwitterModule(Module):

    def __init__(self, root):
        super(TwitterModule, self).__init__(root)

        font_big = Font(family="Helvetica", size=36)

        self.load_api_credentials()

        self.api = twitter.Api(consumer_key=self.ckey,
                               consumer_secret=self.csec,
                               access_token_key=self.atkey,
                               access_token_secret=self.atsec)

        self.text_top = Label(root, font=font_big, fg="white", bg="black",
                              padx=5)
        self.text_top.grid(row=0)
        self.text_bot = Label(root, font=font_big, fg="white", bg="black",
                              padx=5)
        self.text_bot.grid(row=1)
        self.counter = 0
        self.loop()


    def load_api_credentials(self):
        load_dotenv(join(dirname(__file__), '.env'))
        self.ckey = os.environ.get("CKEY")
        self.csec = os.environ.get("CSEC")
        self.atkey = os.environ.get("ATKEY")
        self.atsec = os.environ.get("ATSEC")


    def loop(self):
        timeline = self.api.GetHomeTimeline()
        self.timeline = [self.process(tweet) for tweet in timeline]
        self.loop_helper()
        self.text_top.after(1000 * 60 * 60, self.loop)

    def loop_helper(self):
        if self.counter >= len(self.timeline):
            self.counter = 0
        tweet = self.timeline[self.counter]
        self.text_top.config(text=tweet[0], justify=CENTER)
        # TODO: crack this grid geometry thing.
        # The 50 char max length is only a temporary fix
        if len(tweet[1]) > 50:
            self.text_bot.config(text=tweet[1][:50] + "...", justify=CENTER)
        else:
            self.text_bot.config(text=tweet[1], justify=CENTER)
        self.counter += 1
        self.text_top.after(20000, self.loop_helper)

    def process(self, tweet):
        removed_url = re.sub(r'http\S+', '', tweet.text)
        processed_text = html.unescape(removed_url)
        text = utils.remove_unicode(processed_text)
        tweet_user = tweet.user.screen_name
        tweet_time = self.process_tweet_time(tweet.created_at)
        return "Posted by @{} on {}:".format(tweet_user, tweet_time), text

    def process_tweet_time(self, tweet_time):
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
