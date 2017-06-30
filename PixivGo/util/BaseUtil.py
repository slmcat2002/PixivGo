# -*- coding: utf-8 -*-

import re
import time


class BaseUtil(object):
  def enum(**enums):
    return type('Enum', (), enums)

  def __init__(self):
    pass

  @staticmethod
  def text_clean(text):
    t = text.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').replace(',', ' ').strip()
    t = re.sub('\s+', ' ', t)
    return t

  @staticmethod
  def json_clean(text):
    t = text.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').strip()
    return t

  @staticmethod
  def date_time_now():
    return int(time.time())

  @staticmethod
  def date2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d')))

  @staticmethod
  def datetime2ts(datetime):
    return int(time.mktime(time.strptime(datetime, '%Y-%m-%d %H:%M:%S')))


