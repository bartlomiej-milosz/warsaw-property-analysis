from enum import Enum


class District(Enum):
    MOKOTOW = "mazowieckie/warszawa/warszawa/warszawa/mokotow"
    WILANOW = "mazowieckie/warszawa/warszawa/warszawa/wilanow"
    SRODMIESCIE = "mazowieckie/warszawa/warszawa/warszawa/srodmiescie"
    WOLA = "mazowieckie/warszawa/warszawa/warszawa/wola"
    PRAGA_POLNOC = "mazowieckie/warszawa/warszawa/warszawa/praga-polnoc"


class ResultLimit(Enum):
    SMALL = 24
    MEDIUM = 36
    LARGE = 48
    XLARGE = 72