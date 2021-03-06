#!/home/grad3/harshal/py_env/my_env/bin/python2.7

class constants:

    # Logger constants. Choose between - 
    # INFO, DEBUG, WARN, ERROR, CRITICAL

    console_log_verbosity = 'INFO'
    file_log_verbosity = 'ERROR'
    log_file = "./log/log"

    # Proxy usage constants
    http_proxy_list = '/research/analytics/proxylist/http_proxylist/proxylist'
    socks_proxy_list = '/research/analytics/proxylist/socks5_proxylist/proxylist'

    proxy_authentication = True
    proxy_credentials = '/research/analytics/proxylist/proxy_credentials'

    if proxy_authentication:
        assert proxy_credentials is not None, "Provide proxy credentials file path"

    proxy_username = None
    proxy_password = None
    http_proxies = []
    socks_proxies = []
   
    if proxy_credentials: 
        f = open(proxy_credentials)
        rows = f.readlines()
        proxy_username = rows[0].strip().split(':')[1]
        proxy_password = rows[1].strip().split(':')[1]
        f.close()

    if http_proxy_list:
        with open(http_proxy_list) as f:
            proxies = f.readlines()
        http_proxies = [proxy.strip() for proxy in proxies]

    if socks_proxy_list:
        with open(socks_proxy_list) as f:
            proxies = f.readlines()
        socks_proxies = [proxy.strip() for proxy in proxies]


    # Database access constants for mysql database
    # To be done : Add support for mongoDB

    database_server = 'ist-www-mysql-prod.bu.edu'
    database_port = 3309
    database_name = 'amazon_appstore'
    database_username = 'amazon_appstore'
    database_password = 'sP7sw8chuchu'

class categories:
    urls = {
    "BOOKS_COMICS" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408444011",
    "BUSINESS" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:10298305011",
    "COMMUNICATION" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408466011",
    "CUSTOMIZATION" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408481011",
    "EDUCATION" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408490011",
    "FINANCE" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408433011",
    "FOOD_DRINK" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408523011", 
    "GAMES" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011",
    "HEALTH_FITNESS" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408749011",
    "KIDS" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408582011",
    "LIFESTYLE" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408710011",
    "LOCAL" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:10298309011",
    "MAGAZINES" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408805011", 
    "MEDICAL" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:10298306011",
    "MOVIES_TV" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408765011",
    "MUSIC_AUDIO" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408771011",
    "NEWS" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408802011",
    "NOVELTY" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408852011",
    "PHOTO_VIDEO" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408874011",
    "PRODUCTIVITY" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408449011",
    "REFERENCE" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408491011",
    "SHOPPING" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408875011",
    "SOCIAL" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408464011",
    "SPORTS" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408876011",
    "TRANSPORTATION" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:10298308011",
    "TRAVEL" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408785011",
    "UTILITIES" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408914011", 
    "WEATHER" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9408850011",
    "ACTION" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408529011",
    "ADVENTURE" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408530011",
    "ARCADE" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408531011",
    "BOARD" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408532011",
    "BRAIN_PUZZLE" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408533011",
    "CARDS" : "http://www.amazon.com/s/=rh=n:2350149011,n:!9209898011,n:9209902011,n:9408534011",
    "CASINO" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408535011",
    "DICE" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408536011",
    "FANTASY_SPORTS" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408877011",
    "MUSIC_RHYTHM" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408537011",
    "RACING" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408538011",
    "ROLE_PLAYING" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408539011",
    "SEEK_FIND" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408541011",
    "SIMULATION" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408542011",
    "SPORTS_GAMES" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408543011",
    "STRATEGY" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408578011",
    "TRIVIA" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408579011",
    "WORDS" : "http://www.amazon.com/s/rh=n:2350149011,n:!9209898011,n:9209902011,n:9408580011"
    }
    
