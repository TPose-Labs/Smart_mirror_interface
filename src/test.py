from modules import TwitterModule, ClockModule
from utils import Container

container = Container()
container.add_module(ClockModule, "left")
container.add_module(TwitterModule, "bottom")

container.start()
