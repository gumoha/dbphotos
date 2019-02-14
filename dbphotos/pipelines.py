# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import codecs,json,time,re
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class DbphotosPipeline(object):

    def open_spider(self,spider):
        filen = "F:\Scrapy\doubanphotos\photos\-test0214-.json"
        self.file = codecs.open(filen, 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        today = time.strftime('%Y%m%d-%H:%M', time.localtime(time.time()))
        line = '获取时间%s—' % today + json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item


class DownloadImgPipeline(ImagesPipeline):

    # 下载图片
    def get_media_requests(self, item, info):
        print('开始下载图片……')
        for imgsrc in item['imgsrcs']:
            #Request里 meta参数：传递信息给下一个函数，只接受dict形式的赋值
            yield scrapy.Request(imgsrc,meta={'pathname':item['imgpath']})

    # 重命名图片
    def file_path(self, request, response=None, info=None):
        # 提取url前面名称作为图片名
        #https://img3.doubanio.com/view/photo/m/public/p2538454221.webp
        image_guid = request.url.split('/')[-1]

        #同一系列图片存储文件夹路径
        pathname = request.meta['pathname']

        #格式化同一系列文件夹路径
        filename = u'{0}/{1}'.format(pathname,image_guid)
        return filename

    #判定是否下载成功
    def item_completed(self, results, item, info):
        #第一个元素是布尔值，表示是否成功
        if not results[0][0]:
            raise DropItem('下载图片失败')
        return item
