import requests
import time
import logging
from .db import Mongo_save
from multiprocessing.pool import ThreadPool
from requests.exceptions import ConnectTimeout, ProxyError

logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)


def verify_many(proxy_list, method):
    pool = ThreadPool(len(proxy_list))
    for proxy in proxy_list:
        pool.apply_async(verify_ip, args=(proxy, method))
    pool.close()
    pool.join()


def verify_ip(proxy, method, url='https://www.baidu.com'):
    headers = {
                    'user-agent' :'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
            }
    proxies = {
        'http': 'http://' + proxy['proxy'],
        'https': 'https://' + proxy['proxy']
    }
    try:
        start = time.time()
        resp = requests.get(url, headers=headers, proxies=proxies, timeout=3)
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
    except (ConnectTimeout,ProxyError):
        Mongo_save().delete_proxy(proxy)


