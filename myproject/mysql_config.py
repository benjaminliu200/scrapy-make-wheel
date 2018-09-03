db_config = {
    'local': {
        'host': '193.112.73.110',
        'port': 3306,
        'user': "liudy",
        'passwd': "Huoli123!",
        'db': "scrapy",
        'charset': "utf8",
        'pool': {
            # use = 0 no pool else use pool
            "use": 1,
            # size is >=0,  0 is dynamic pool
            "size": 10,
            # pool name
            "name": "local",
        }
    },
    'poi': {
        'host': '193.112.73.110',
        'port': 3306,
        'user': "liudy",
        'passwd': "Huoli123!",
        'db': "scrapy",
        'charset': "utf8",
        'pool': {
            # use = 0 no pool else use pool
            "use": 0,
            # size is >=0,  0 is dynamic pool
            "size": 0,
            # pool name
            "name": "poi",
        }
    },
}
