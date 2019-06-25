import requests
import logging
import chardet
import time


logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)


class Downloader(object):
    def __init__(self):
            self.headers = {
                    'user-agent' :'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
            }

    def download(self, url, rule):
        logging.info('Downloading: {}'.format(url))
        try:
            resp = requests.get(url, headers=self.headers)
            # print(resp.text)
            resp.encoding = chardet.detect(resp.content)['encoding']
            if rule.get('delay'):
                time.sleep(rule['delay'])
            if resp.status_code == 200:
                return resp.text
            else:
                raise ConnectionError
        except ConnectionError as e:
            logger.error(e)


