# -*- coding: utf-8 -*-
#

from cached_property import cached_property

from .backend import DataBackend
from ..utils import lru_cache, get_str_date_from_int, get_int_date
from pandas import Series
import numpy as np

class TushareDataBackend(DataBackend):

    @cached_property
    def ts(self):
        try:
            import tushare as ts
            return ts
        except ImportError:
            print("-" * 50)
            print(">>> Missing tushare. Please run `pip install tushare`")
            print("-" * 50)
            raise

    @cached_property
    def stock_basics(self):
        return self.ts.get_stock_basics()

    @cached_property
    def code_name_map(self):
        code_name_map = self.stock_basics[["name"]].to_dict()["name"]
        return code_name_map

    def convert_code(self, order_book_id):
        return order_book_id.split(".")[0]

    @lru_cache(maxsize=4096)
    def get_price(self, order_book_id, start, end, freq, **kwargs):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        code = self.convert_code(order_book_id)
        is_index = False
        if ((order_book_id.startswith("0") and order_book_id.endswith(".XSHG")) or
            (order_book_id.startswith("3") and order_book_id.endswith(".XSHE"))
            ):
            is_index = True
        ktype = freq
        if freq[-1] == "m":
            ktype = freq[:-1]
        elif freq == "1d":
            ktype = "D"
        # else W M

        df = self.ts.get_k_data(code, start=start, end=end, index=is_index, ktype=ktype)

        if freq[-1] == "m":
            df["datetime"] = df.apply(
                lambda row: int(row["date"].split(" ")[0].replace("-", "")) * 1000000 + int(row["date"].split(" ")[1].replace(":", "")) * 100, axis=1)
        elif freq in ("1d", "W", "M"):
            df["datetime"] = df["date"].apply(lambda x: int(x.replace("-", "")) * 1000000)

        del df["code"]
        arr = df.to_records()

        return arr

    @lru_cache()
    def get_order_book_id_list(self):
        """获取所有的股票代码列表
        """
        info = self.ts.get_stock_basics()
        code_list = info.index.sort_values().tolist()
        order_book_id_list = [
            (code + ".XSHG" if code.startswith("6") else code + ".XSHE")
            for code in code_list
        ]
        return order_book_id_list

    @lru_cache()
    def get_trading_dates(self, start, end):
        """获取所有的交易日

        :param start: 20160101
        :param end: 20160201
        """
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        df = self.ts.get_k_data("000001", index=True, start=start, end=end)
        trading_dates = [get_int_date(date) for date in df.date.tolist()]
        return trading_dates

    @cached_property
    def trading_dates(self):
        return np.array(self.get_trading_dates('1990-01-01', '2099-12-28'))

    @lru_cache(maxsize=4096)
    def symbol(self, order_book_id):
        """获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """
        code = self.convert_code(order_book_id)
        return "{}[{}]".format(order_book_id, self.code_name_map.get(code))

    @lru_cache(maxsize=4096)
    def get_index_component(self, order_book_id):
        """
        获取指数组成成分
        :param order_book_id: 股票代码
        :return: list of str
        """
        if order_book_id == '000300.XSHG':
            code_list = list(self.ts.get_hs300s()['code'])
        elif order_book_id == '000016.XSHG':
            code_list = list(self.ts.get_sz50s()['code'])
        elif order_book_id == '000905.XSHG':
            code_list = list(self.ts.get_zz500s()['code'])
        order_book_id_list = [code + ".XSHG" if code.startswith("6") else code + ".XSHE" for code in code_list]
        return order_book_id_list

    @lru_cache(maxsize=4096)
    def get_previous_trading_date(self, date, n=1):
        """

        :param date: 需要查询的日期 str '20180601'或者20180601
        :param n: 提前的天数
        :return: 查询日期之前的第n个交易日 20180531
        """
        all_previous_trading_dates = self.trading_dates[self.trading_dates < int(date)]
        return all_previous_trading_dates[-n]

    @lru_cache(maxsize=4096)
    def get_shares(self, order_book_id, start_date, end_date, fields=None):
        """
        获取某只股票在一段时间内的流通情况
        :param order_book_id: 需要查询的资产代码
        :param start_date: 查询的起始日期 20180504
        :param end_date: 查询的截止日期 20180601
        :param fields: total 总股本；circulation_a 流通A股；management_circulation 已流通高管持股；
        non_circulation_a 非流通A股合计；total_a A股总股本
        :return: pd.Series
        """
        dates = self.trading_dates[self.trading_dates >= start_date]
        dates = dates[dates <= end_date]
        dates = map(lambda x: str(x)[:4] + '-' + str(x)[4:6] + '-' + str(x)[6:], dates)
        if fields == 'total_a':
            col_name = 'totals'
        else:
            col_name = 'outstanding'
        code = self.convert_code(order_book_id)
        result_series = Series()
        for date in dates:
            try:
                temp = self.ts.get_stock_basics(date)[col_name][code]
            except:
                temp = np.nan
            result_series[date] = temp
        return result_series
