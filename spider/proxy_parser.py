#!/usr/bin/env python
# encoding: utf-8
from lxml import etree


class Parser(object):
    """
    处理爬取的代理列表，格式化生成代理列表
    """

    def xpath_parse(self, text, rule):
        """
        :param text: 爬取页面
        :param rule: 爬取规则
        :return: 格式化代理列表
        """
        proxy_list = []

        page = etree.HTML(text)
        ip_list = page.xpath(rule['ip'])
        # print(ip_list)
        port_list = page.xpath(rule['port'])
        # print(port_list)
        for ip, port in zip(ip_list, port_list):
            proxy = {
                'proxy': ip + ':' + port
            }
            proxy_list.append(proxy)
        return proxy_list