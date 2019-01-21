# -*- coding: utf-8 -*-
import numpy as np

from .time_series import MarketDataSeries, MarketSeries, FinancialDataSeries, IndexDataSeries
from .func import (
    SumSeries,
    AbsSeries,
    StdSeries,
    SMASeries,
    MovingAverageSeries,
    WeightedMovingAverageSeries,
    ExponentialMovingAverageSeries,
    CrossOver,
    minimum,
    maximum,
    every,
    count,
    hhv,
    llv,
    Ref,
    iif,
    AveDevSeries,
    DmaSeries,
)
from .context import (
    symbol,
    set_current_security,
    set_current_date,
    set_start_date,
    set_data_backend,
    set_current_freq,
)
from .helper import select
from numpy import sqrt

# create open high low close volume datetime total_turnover
for name in ["open", "high", "low", "close", "volume", "datetime", "total_turnover"]:
    dtype = np.float64 if name != "datetime" else np.uint64
    cls = type("{}Series".format(name.capitalize()), (MarketDataSeries, ), {"name": name, "dtype": dtype})
    obj = cls(dynamic_update=True)
    for var in [name[0], name[0].upper(), name.upper()]:
        globals()[var] = obj

# define classes to reflect market condition
for name in ["advance", "decline"]:
    dtype = np.float64
    cls = type("{}Series".format(name.capitalize()), (MarketSeries, ), {"name": name, "dtype": dtype})
    obj = cls(dynamic_update=True)
    for var in [name[0], name[0].upper(), name.upper()]:
        globals()[var] = obj

# define classes to get financial data
for name in ["capital"]:
    dtype = np.float64
    cls = type("{}Series".format(name.capitalize()), (FinancialDataSeries, ), {"name": name, "dtype": dtype})
    obj = cls(dynamic_update=True)
    for var in [name[0], name[0].upper(), name.upper()]:
        globals()[var] = obj

# define classes to get index data
for name in ["indexo", "indexh", "indexl", "indexc", "indexv", "indexa"]:
    dtype = np.float64
    cls = type("{}Series".format(name.capitalize()), (IndexDataSeries, ), {"name": name, "dtype": dtype})
    obj = cls(dynamic_update=True)
    for var in [name[0], name[0].upper(), name.upper()]:
        globals()[var] = obj

VOL = VOLUME
AMOUNT = TOTAL_TURNOVER
SQRT = sqrt

MA = MovingAverageSeries
WMA = WeightedMovingAverageSeries
EMA = ExponentialMovingAverageSeries
SMA = SMASeries

SUM = SumSeries
ABS = AbsSeries
STD = StdSeries

CROSS = CrossOver
REF = Ref
MIN = minimum
MAX = maximum
EVERY = every
COUNT = count
HHV = hhv
LLV = llv
IF = IIF = iif

S = set_current_security
T = set_current_date
AVEDEV = AveDevSeries
DMA = DmaSeries

__all__ = [
    "OPEN", "O",
    "HIGH", "H",
    "LOW", "L",
    "CLOSE", "C",
    "VOLUME", "V", "VOL",
    "DATETIME",
    "ADVANCE",
    "DECLINE",
    "CAPITAL",
    "INDEXO",
    "INDEXH",
    "INDEXL",
    "INDEXC",
    "INDEXA",

    "SMA",
    "MA",
    "EMA",
    "WMA",

    "SUM",
    "ABS",
    "STD",

    "CROSS",
    "REF",
    "MAX",
    "MIN",
    "EVERY",
    "COUNT",
    "HHV",
    "LLV",
    "IF", "IIF",

    "S",
    "T",

    "select",
    "symbol",
    "set_current_security",
    "set_current_date",
    "set_start_date",
    "set_data_backend",
    "set_current_freq",
    "AVEDEV",
    "AMOUNT",
    "SQRT",
    "DMA"
]
