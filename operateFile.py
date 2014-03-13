# -*- coding: UTF-8 -*-
'''
Created on 2014-02-25

@author: Grayson
'''
import traceback, re

class OperateFile(object):
  '''
  classdocs
  '''

  def __init__(self, file):
    try:
      self.fileHandle = open(file)
    except:
      print traceback.format_exc()


  def __del__(self):
    self.fileHandle.close()


  def readLine2List(self):
    self.fileHandle.seek(0)
    linesList = self.fileHandle.readlines()
    return linesList


  def readItem2List(self):
    '''
    将配置文件读取信息分字典项存入返回字典conditionDict中
    '''
    itemDict = dict()
    try:
      #匹配正则表达式
      pattern = re.compile('</?\w+>')
      linesList = self.readLine2List()
      dictValue = list()
      for line in linesList:
        strLine = str(line)
        #跳过白空行
        if (len(strLine.split()) == 0):
          continue
        #以'#'起始行认为是注释
        if (strLine.split()[0][0:1] == '#'):
          continue
        if (pattern.match(strLine)):
          if (strLine[1:2] == '/'):
            #关键字结束符
            if (strLine[2:-2] != dictKey):
              #起始关键字与结束关键字不匹配
              raise Exception('Invalid format.')
            #条件信息写入
            itemDict[dictKey] = dictValue
          else:
            #关键字起始符
            dictKey = strLine[1:-2]
            dictValue = list()
        else:
          #条件信息以空格符分割存入列表
          if (strLine.split() != []):
            dictValue.append(strLine.split())
    except:
      print traceback.format_exc()

    return itemDict



