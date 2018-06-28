from modules import TwitterModule, ClockModule, WeatherModule
from utils import Container

container = Container()
container.add_module(ClockModule, "left")
container.add_module(TwitterModule, "bottom")
container.add_module(WeatherModule, "right")

container.start()
