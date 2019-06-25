parse_rule = [
    {
        'name': 'xici',
        'url': ['https://www.xicidaili.com/nn/{}'.format(i) for i in range(1, 4)],
        'parse_type': 'xpath',
        'ip': '//*[@id="ip_list"]/tr/td[2]/text()',
        'port': '//*[@id="ip_list"]/tr/td[3]/text()'
    },
    {
        'name': 'kuaidaili',
        'url': ['https://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1, 8)],
        'parse_type': 'xpath',
        'ip': '//tbody/tr/td[1]/text()',
        'port': '//tbody/tr/td[2]/text()',
        'delay': 1
    }
]