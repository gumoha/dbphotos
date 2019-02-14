import scrapy
import time,random,os
from dbphotos.items import DbphotosItem


class DbphotosSpider(scrapy.Spider):
    name = 'doubanphotos'
    allowed_domains = ['douban.com']

    base_path = r'F:\Scrapy\doubanphotos\photos\\'

    # https://www.douban.com/people/staymiao/photos
    dburl = 'https://www.douban.com/people/'

    print('请输入需要获取相册的域名段（仅限字母或数字）\n在输入 exit 后停止输入\n')
    IDname = input('输入：')
    if IDname != 'exit':
        ID_folderpath = os.path.join(base_path,IDname)

        if not os.path.exists(ID_folderpath):
            print('正在创建%s文件夹……'%IDname)
            os.makedirs(ID_folderpath)
            print('创建%s文件夹成功！' % IDname)

        plurl = dburl + str(IDname) + '/photos'
        print('ID为 %s 的相册链接：%s,进行相册获取……' % (IDname,plurl))
    else:
        print('exit 退出程序')


    def start_requests(self):
        yield scrapy.Request(self.plurl, callback=self.parse_url)


    def parse_url(self,response):
        print('获取相册信息%s……'%response.url)

        href_list = response.xpath('//div[contains(@class,"wr")]/div[contains(@class,"albumlst")]/a/@href').extract()

        for hr in href_list:
            print('获取到的相册链接 ——> %s'%hr)
            time.sleep(random.choice(range(5)))
            yield scrapy.Request(url=hr,callback=self.parse_info)

        try:
            nextpg = response.xpath('//div[contains(@class,"paginator")]/span[contains(@class,"next")]/a/@href').extract_first()
            if nextpg:
                time.sleep(random.choice(range(5)))
                yield scrapy.Request(url=nextpg, callback=self.parse_url)
        except:
            print('没有下一页更多相册了')


    def parse_info(self,response):

        item_photos = DbphotosItem()

        item_photos['link'] = response.url

        #相册标题
        try:
            item_photos['title'] = response.xpath('//div[contains(@class,"info")]/h1/text()').extract_first()
        except:
            item_photos['title'] = None

        #相册介绍
        try:
            item_photos['intro'] = response.xpath('//div[contains(@class,"article")]/p[contains(@class,"description")]/text()').extract_first()
        except:
            item_photos['intro'] = None
        #相册张数
        try:
            item_photos['nums'] = response.xpath('//div[contains(@class,"article")]/div[contains(@class,"pl photitle")]/span/text()').re_first(r'\d+\u5f20')
        except:
            item_photos['nums'] = None

        #创建相册文件夹
        item_photos['imgpath'] = os.path.join(self.ID_folderpath,item_photos['title'])
        folderpath = item_photos['imgpath']

        if not os.path.exists(folderpath):
            os.makedirs(folderpath)
            print('创建%s文件夹成功！' % item_photos['title'])

        item_photos['imgsrcs'] = response.xpath('//div[contains(@class,"article")]/div[contains(@class,"photolst clearfix")]/div[contains(@class,"photo_wrap")]/a/img/@src').extract()

        yield item_photos

        try:
            nextpg = response.xpath('//div[contains(@class,"article")]/div[contains(@class,"paginator")]/span[contains(@class,"next")]/a/@href').extract_first()
            if nextpg:
                time.sleep(random.choice(range(5)))
                yield response.follow(url=nextpg,callback=self.parse_info)
        except:
            print('没有下一页更多相片了')

