# -*- coding: utf-8 -*-
#


class DataBackend(object):
    skip_suspended = True

    def get_price(self, order_book_id, start, end, freq, **kwargs):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :param freq: 1m 1d 5m 15m ...
        :returns:
        :rtype: numpy.rec.array
        """
        raise NotImplementedError

    def get_order_book_id_list(self):
        """获取所有的
        """
        raise NotImplementedError

    def get_trading_dates(self, start, end):
        """获取所有的交易日

        :param start: 20160101
        :param end: 20160201
        """
        raise NotImplementedError

    def symbol(self, order_book_id):
        """获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """
        raise NotImplementedError

    def get_index_component(self, order_book_id):
        """
        获取指数组成成分
        :param order_book_id: 股票代码
        :return: list of str
        """
        raise NotImplementedError

    def get_previous_trading_date(self, date, n=1):
        """

        :param date: 需要查询的日期
        :param n: 提前的天数
        :return: 查询日期之前的第n个交易日
        """
        raise NotImplementedError

    def get_shares(self, order_book_id, start_date, end_date, fields=None):
        """
        获取某只股票在一段时间内的流通情况
        :param order_book_id: 需要查询的资产代码
        :param start_date: 查询的起始日期
        :param end_date: 查询的截止日期
        :param fields: total 总股本；circulation_a 流通A股；management_circulation 已流通高管持股；
        non_circulation_a 非流通A股合计；total_a A股总股本
        :return:
        """
        raise NotImplementedError

