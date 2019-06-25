from .config import parse_rule
from .downloader import Downloader
from .url_parser import Parser
from .verify_ip import verify_many
from .db import Mongo_save
import logging
import time

logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)


def scheduling():
    while True:
        logger.info('开始抓取IP...')
        for rule in parse_rule:
            for url in rule['url']:
                logger.info('开始抓取网站:{}'.format(url))
                text = Downloader().download(url, rule)
                proxy_list = Parser().xpath_parse(text, rule)
                verify_many(proxy_list, 'upload')
        time.sleep(24 * 60 * 60)

def check():
    while True:
        m = Mongo_save()
        proxies = m.get_proxy(10000)
        if not len(proxies) == 0:
            logger.info('开始检测代理IP...')
            verify_many(proxies, 'update')

        time.sleep(30 * 60)