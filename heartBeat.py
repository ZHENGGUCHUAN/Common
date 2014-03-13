# -*- coding: UTF-8 -*-
'''
Created on 

@author: Grayson
'''
import threading, datetime, time
import logFile

class HeartBeat(object):
  '''
  classdocs
  '''

  def __init__(self, name, interval = 60 * 60):
    '''
    Heart beat interval time
    '''
    self.name = name
    if interval <= 0:
      raise Exception
    self.interval = interval
    self.thread = threading.Thread(target = self.sendHeartBeat)


  def sendHeartBeat(self):
    logHandle = logFile.LogFile(name = self.name)
    while True:
      currTime = datetime.datetime.now().timetuple()
      logHandle.logInfo(
        'Heart beat at: ' +
        str(currTime.tm_year) + '-' + str(currTime.tm_mon) + '-' + str(currTime.tm_mday) + ' ' +
        str(currTime.tm_hour) + ':' + str(currTime.tm_min) + ':' + str(currTime.tm_sec))
      time.sleep(self.interval)


  def startThread(self):
    self.thread.start()
