#!/usr/bin/env python
# encoding: utf-8
import requests
import time
import logging
from .save_to_db import Mongo_save
from multiprocessing.pool import ThreadPool
from requests.exceptions import ConnectTimeout, ProxyError

# 日志
logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)

class VerifyIp(object):
    """
    验证代理列表，筛选有效代理
    """
    def __init__(self):
        # 模拟报头
        self.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    def verify_ip(self, proxy, method, url='https://www.baidu.com'):
        """
        代理验证函数
        :param proxy: 代理 类型：集合
        :param method: 代理类型 （新代理/重复更新）
        :param url: 测试网站
        :return: None
        """
        # 生成代理
        proxies = {
            'http': 'http://' + proxy['proxy'],
            'https': 'https://' + proxy['proxy']
        }
        try:
            start = time.time()
            resp = requests.get(url, headers=self.headers, proxies=proxies, timeout=3)
            delay = round(time.time() - start, 2)

            if resp.status_code == 200:
                proxy['delay'] = delay
                logger.info('代理IP可用:{}'.format(proxy))
                if method == 'upload':
                    Mongo_save().insert_proxy(proxy)
                elif method == 'update':
                    Mongo_save().update_proxy({'proxy': proxy['proxy']}, {'delay': proxy['delay']})
            else:
                if method == 'update':
                    logger.info('代理IP失效，已删除:{}'.format(proxy))
                    Mongo_save().delete_proxy(proxy)
        except (ConnectTimeout, ProxyError):
            Mongo_save().delete_proxy(proxy)

    def verify_many(self, proxy_list, method):
        '''
        设置线程池，处理代理验证
        :param proxy_list: 代理池 类型：列表
        :param method: 代理类型 （新代理/重复更新）
        :return: None
        '''
        pool = ThreadPool(len(proxy_list))
        for proxy in proxy_list:
            pool.apply_async(self.verify_ip, args=(proxy, method))
        pool.close()
        pool.join()




