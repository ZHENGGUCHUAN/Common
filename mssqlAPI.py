# -*- coding: UTF-8 -*-
'''
Created on 2013-12-05

@author: Grayson
'''
import adodbapi, traceback
from time import sleep


class MssqlAPI(object):
  '''
  Connect MSSQL database, return SQL instruction result.
  '''


  def __init__(self, server, db, user, pwd):
    '''
    Constructor
    '''
    self.server = server
    self.db = db
    self.user = user
    self.pwd = pwd
    self.retryNum = 20
    self.connectDB(server, db, user, pwd)
    
    
    
  def __del__(self):
    try:
      self.closeDB()
    except:
      print traceback.format_exc()
      
      
  def connectDB(self, server, db, user, pwd):
    '''
    Connect MS-SQL database, 
    Create connection before execute SQL instruct, and close it immediately.
    '''
    try:
      #setup connect string
      connectStr = 'PROVIDER=SQLOLEDB;DATA SOURCE=' + server + ';UID=' + user + ';PWD=' + pwd + ';DATABASE=' + db + ';charset="utf8";autocommit=True'
      #connect database
      print 'Connecting MSSQL: %s' % server
      self.conn = adodbapi.connect(connectStr,timeout=0)
      #get cursor
      self.cursor = self.conn.cursor()
    except:
      self.retryNum -= 1
      if (self.retryNum  > 0):
        print 'Connect to MSSQL database failed, connect again.'
        sleep(1)
        self.connectDB(self.server, self.db, self.user, self.pwd)
      else:
        print 'Connect to MSSQL database failed'
        print traceback.format_exc()
  
  
  def closeDB(self):
    '''
    Close database connection. 
    '''
    self.cursor.close()
    #print 'Connection of MSSQL has be closed.'


  def sqlQuery(self, sqlCmd):
    '''
    SQL query
    '''
    try:
      #execute SQL instruct
      self.sqlInstruct(sqlCmd)
      #get result
      retFetch = self.cursor.fetchall()
    except:
      print 'Query SQL record failed.'
      print traceback.format_exc()
      #sys.exit()
    return retFetch
  
  
  def sqlAppend(self, sqlCmd):
    try:
      self.sqlInstruct(sqlCmd)
      self.sqlCommit()
    except:
      print 'Append SQL record failed.'
      print traceback.format_exc()
  
  
  def sqlDelete(self, table, spec = ''):
    try:
      delCmd = 'DELETE FROM ' + table + spec
      print delCmd
      self.sqlInstruct(delCmd)
    except:
      print 'Delete SQL record failed.'
      print traceback.format_exc()
  
  
  def sqlQueryProc(self, name, para):
    '''
    SQL query
    '''
    try:
      #execute SQL instruct
      self.cursor.callproc(name, para)
      #get result
      retFetch = self.cursor.fetchall()
    except:
      print 'Query SQL record failed.'
      print traceback.format_exc()
      #sys.exit()
    return retFetch
  
  
  def sqlExecuteProc(self, name, para):
    '''
    SQL execute
    '''
    try:
      #execute SQL instruct
      self.cursor.callproc(name, para)
    except:
      print 'Execute SQL record failed.'
      print traceback.format_exc()
      #sys.exit()
  
  
  def sqlCommit(self):
    self.conn.commit()
  
  
  def sqlInstruct(self, sqlCmd):
    try:
      #execute SQL instruct
      self.cursor.execute(sqlCmd.decode('utf-8').encode('gbk'))
    except:
      print 'Execute SQL failed.'
      print traceback.format_exc()
      #sys.exit()
  