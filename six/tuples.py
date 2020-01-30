from collections import namedtuple

Color3 = namedtuple('Color3', 'red green blue')
Color4 = namedtuple('Color4', 'red green blue alpha')
ChannelConfig = namedtuple('ChannelConfig', 'color intensity desaturate')
