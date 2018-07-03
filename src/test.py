from modules import TwitterModule, ClockModule, WeatherModule, StockModule
from utils import Container

container = Container()
container.add_module(ClockModule, "left")
container.add_module(TwitterModule, "bottom")
container.add_module(WeatherModule, "right")
container.add_module(StockModule, "rbot")

container.start()
