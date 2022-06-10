from dataclasses import dataclass
import typing

@dataclass
class Test:
    hello: int
    bye: float


c = Test()

c.bye = 5
c.hello = 6
