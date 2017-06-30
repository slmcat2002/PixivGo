# -*- coding: utf-8 -*-
import re
import sys
import json
import time
import datetime
import logging
import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import Spider
from PixivGo.util.BaseUtil import BaseUtil

GENERAL_CODE = "utf-8"


class PixivSearch(scrapy.Spider):
  name = "pixiv_search"
  source = "acfun"
  custom_settings = {
    'ITEM_PIPELINES': {
      #'PixivGo.pipelines.DefaultPipeline': 200,
    },
    'DOWNLOADER_MIDDLEWARES': {
    },

    'DOWNLOAD_DELAY': 0.1,
    'CONCURRENT_REQUESTS': 16,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
    'CONCURRENT_REQUESTS_PER_IP': 16,
  }


  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')
    self.keyword = ""

  start_urls = []
  base_url = "https://www.pixiv.net"
  base_search_api = "https://www.pixiv.net/search.php?s_mode=s_tag&word=%s&p=%s"

  url_filter = "http://www.acfun.cn/"

  def start_requests(self):
    self.keyword = self.settings["keyword"]
    if self.keyword is None:
      logging.warning("cant find keyword")
      yield
    else:
      yield Request(url=self.generate_search_url(keyword=self.keyword, page=1),
                    callback=self.parse_search_result)

  def parse_search_result(self, response):
    table = response.xpath('.//ul[@class="_image-items autopagerize_page_element"]')
    artwork_list = table.xpath('./li[@class="image-item"]')
    for artwork in artwork_list:
      a_url = artwork.xpath('.//a[@class="work  _work "]/@href').extract_first()
      if a_url is None:
        a_url = artwork.xpath('.//a[@class="work  _work multiple "]/@href').extract_first()
      a_url = self.generate_full_url(a_url)
      # title = artwork.xpath('.//h1[@class="title"]').xpath('string(.)').extract_first()
      # author_info = artwork.xpath('.//a[@class="user ui-profile-popup"]')
      # author_link = self.generate_full_url(author_info.xpath('@href').extract_first())
      # author_name = author_info.xpath('@data-user_name').extract_first()

      #yield Request(url=a_url, callback=self.parse_artwork)

  def parse_artwork(self, response):
    userdata = response.xpath('.//div[@class="userdata"]')
    title = userdata.xpath('./h1[@class="title"]').xpath('string(.)').extract_first()
    title = BaseUtil.text_clean(title)
    author_name = userdata.xpath('./h2[@class="name"]/a').xpath('string(.)').extract_first()
    author_name = BaseUtil.text_clean(author_name)
    author_link = userdata.xpath('./h2[@class="name"]/a/@href').extract_first()
    author_link = self.generate_full_url("/" + author_link)
    score = response.xpath('.//span[@class="views"]')
    view = like = 0
    if len(score) == 2:
      view = score[0].xpath('string(.)').extract_first()
      like = score[1].xpath('string(.)').extract_first()
    print response.url, view, like, title, author_link, author_name

  def generate_search_url(self, keyword, page):
    return self.base_search_api % (keyword, page)

  def generate_full_url(self, href):
    return self.base_url + href

