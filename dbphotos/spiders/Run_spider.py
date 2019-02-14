from scrapy import cmdline

name = 'doubanphotos'

cmd = 'scrapy crawl %s'%name

cmdline.execute(cmd.split())