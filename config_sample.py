class Config:
    program_name = 'wa2'
    request_prefix = 'http://www.onsen.ag/data/api/getMovieInfo/'
    #sleep time bewteem two request
    sleep_time = 10
    request_url = request_prefix + program_name

    #email config
    from_addr = 'wikizhu@outlook.com'
    password = '?????????'
    to_addrs = ['a@a.com', 'kazusa@wa.com']
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587

    debug = False