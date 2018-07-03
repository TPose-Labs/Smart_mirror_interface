from tkinter import Label, CENTER
from tkinter.font import Font
from weather import Weather, Unit
from dotenv import load_dotenv
from os.path import join, dirname
from requests import get
import datetime
import calendar
import twitter
import html
import re
import utils
import os


class Module:
    '''
        This here is the skeleton for a "module."
        Modules are the building blocks of the
        smart mirror -- each feature will have its own
        module.
        From a development standpoint, I'm treating this
        class as one would an interface, but I'm also
        implementing most of the functions in here,
        except for "loop," since that differs from module
        to module.
    ''' 

    def __init__(self, root):
        self.root = root
        self.inside = []

    def pack(self, side=None):
        self.root.pack(side=side)

    def grid(self, row=0, column=0):
        self.root.grid(row=row, column=column)

    def destroy_all_inside(self):
        for frame in self.inside:
            frame.grid_forget()
            frame.destroy()

    def loop(self):
        pass


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

    @utils.overrides(Module)
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

        self.font_big = Font(family="Helvetica", size=72)
        self.font_small = Font(family="Helvetica", size=48)

        self.temp_label = Label(root, font=self.font_big, fg="white", bg="black",
                                padx=5)
        self.temp_label.grid(row=0, sticky="w")
        self.cond_label = Label(root, font=self.font_big, fg="white",
                                bg="black", padx=5)
        self.cond_label.grid(row=1, column=0, sticky="w")
        self.temp = ""
        self.cond = ""
        self.forecasts = []
        self.row_counter = 2
        self.loop()

    def list_forecasts(self):
        forecast_list = ""
        for i in range(3):
            forecast = self.forecasts[i]
            self.inside.append(Label(self.root, font=self.font_small,
                                              fg="white", bg="black",
                                              padx=5))
            self.inside[-1].grid(row=self.row_counter, column=0, sticky="w")
            rearranged = self.rearrange_date(forecast.date)
            if i == 2:
                self.inside[-1].config(text=rearranged + ": " + forecast.text)
            else:
                self.inside[-1].config(text=rearranged + ": " + \
                                                forecast.text + ",")
            self.row_counter += 1

    def rearrange_date(self, date):
        date_split = date.split(" ")
        day = date_split[0]
        month = utils.MONTHS[date_split[1]]
        year = date_split[2]
        return "{} {}, {}".format(month, day, year)

    @utils.overrides(Module)
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
        if len(self.forecasts) != 0:
            if self.forecasts[0].date != forecasts[0].date:
                self.row_counter = 2
                self.forecasts = forecasts
                self.destroy_all_inside()
                self.list_forecasts()
        else:
            self.forecasts = forecasts
            self.destroy_all_inside()
            self.list_forecasts()
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

    @utils.overrides(Module)
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


class StockModule(Module):

    def __init__(self, root, symbols):
        super(StockModule, self).__init__(root)
        
        font_big = Font(family="Helvetica", size=36)
        self.inside = {}

        self.symbols = symbols
        row_counter = 1
        for symbol in self.symbols:
            self.inside[symbol] = Label(root, font=font_big, fg="white",
                                        bg="black", padx=5)
            self.inside[symbol].grid(row=row_counter, sticky="w")
            row_counter += 1
        self.loop()
    
    @utils.overrides(Module)
    def loop(self):
        quotes = self.get_quotes()
        for symbol in self.symbols:
            quote = quotes[symbol]
            self.inside[symbol].config(text=quote)
        self.inside[list(self.inside.keys())[0]].after(1000 * 60 * 10, self.loop)

    def get_quotes(self):
        quotes = {}
        for symbol in self.symbols:
            url_before = "https://api.iextrading.com/1.0/stock/"
            url_after = "/batch?types=quote"
            r = get(url_before + symbol + url_after)
            quote = r.json()["quote"]
            formatted = symbol + ": " + str(quote["latestPrice"]) + "\t" + \
                        str(quote["change"])
            quotes[symbol] = formatted
        return quotes
