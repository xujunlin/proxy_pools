from lxml import etree


class Parser(object):
    def xpath_parse(self, text, rule):
        page = etree.HTML(text)
        proxy_list = []
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