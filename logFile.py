# -*- coding: UTF-8 -*-
'''
Created on 2014-01-15

@author: Grayson
'''
import logging.handlers
from os import getpid


class LogFile(object):
  '''
  classdocs
  '''


  def __init__(self, title = 'QIANNIU.SNMP', name = 'Default', level = logging.DEBUG, address = 'syslog.1600.com'):
    '''
    address = syslog.5211game.com
    '''
    self.logger = logging.getLogger(name)
    self.logger.setLevel(level)
    self.title = title
    self.setModuleName(name)

    handler = logging.handlers.SysLogHandler(address = (address, logging.handlers.SYSLOG_UDP_PORT) )
    self.logger.addHandler(handler)
    
  
  def __del__(self):
    del self.logger
  
  
  #def log(self):
  #  return self.logger
  def setModuleName(self, moduleName):
    self.moduleName = moduleName


  def logInfo(self, logString):
    self.logger.info(self.moduleName + '[' + str(getpid()) + ']: ' + 'module[' + self.moduleName + ']' + logString)
    print self.moduleName + '[' + str(getpid()) + ']: ' + 'module[' + self.moduleName + ']' + logString

if __name__ == '__main__':
  log = LogFile()
  log.logInfo("TEST", "123")