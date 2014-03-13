# -*- coding: UTF-8 -*-
'''
Created on 2013-12-06

@author: Grayson
'''
import pymongo, traceback
from time import sleep


class MongoAPI(object):
  '''
  Connect Mongo database
  '''


  def __init__(self, server, port):
    '''
    Constructor
    '''
    self.retryNum = 20
    self.server = server
    self.port = port
    
    self.connectDB(server, port)
    

  def __del__(self):
    self.closeDB()


  def connectDB(self, server, port):
    '''
    Connect MongoDB database, 
    '''
    try:
      print 'Connecting mongoDB: %s,%d' % (server, port)
      self.conn = pymongo.MongoClient(server, port)
    except:
      self.retryNum -= 1
      if (self.retryNum  > 0):
        print 'Connect to mongoDB failed, connect again.'
        sleep(1)
        self.connectDB(self.server, self.port)
      else:
        print 'Connect to mongoDB failed.'
        print traceback.format_exc()
    
  
  def closeDB(self):
    self.conn.close()
    #print('Connection of mongoDB has be closed.')

  
  def isExist(self, database, collection, spec):
    '''
    Query database, return is it exist in spec.
    '''
    try:
      db = self.conn[database]
      col = db[collection]
      exist = True if col.count(spec) > 0 else False
    except:
      print 'Get count result failed.'
      print traceback.format_exc()
      #sys.exit()
      
    return exist
  
  
  def find(self, database, collection, spec = None, sort = None):
    '''
    Query database, return all record in spec.
    '''
    try:
      db = self.conn[database]
      col = db[collection]
      if (spec is None):
        if (sort is None):
          records = col.find()
        else:
          records = col.find().sort(sort)
      else:
        if (sort is None):
          records = col.find(spec)
        else:
          records = col.find(spec).sort(sort)
    except:
      print 'Get find result failed.',database, collection, spec, sort
      print traceback.format_exc()
      
    return records
    
  
  def update(self, database, collection, spec, document, upsert = True):
    '''
    Update date
    '''
    try:
      db = self.conn[database]
      col = db[collection]
      col.update(spec, document, upsert)
    except:
      print 'Update data failed.'
      print traceback.format_exc()
      
      
  def insert(self, database, collection, document, catchException = True):
    '''
    Insert date
    '''
    try:
      db = self.conn[database]
      col = db[collection]
      col.insert(document, save = True)
    except:
      if catchException:
        print 'Insert data failed.'
        print traceback.format_exc()
      else:
        pass
  
  
  def drop(self, database, collection = None):
    '''
    Drop database/collection
    '''
    if (collection is None):
      #drop database
      try:
        self.conn.drop_database(database)
      except:
        print 'Drop database failed.'
        print traceback.format_exc()
    else:
      #drop collection
      try:
        db = self.conn[database]
        col = db[collection]
        col.drop()
      except:
        print 'Drop collection failed.'
        print traceback.format_exc()
  
  
  def remove(self, database, collection, spec):
    '''
    Remove date
    '''
    try:
      db = self.conn[database]
      col = db[collection]
      col.remove(spec)
    except:
      print 'Remove data failed.'
      print traceback.format_exc()
  
  
  def createIndex(self, database, collection, index):
    '''
    Create index from database
    '''
    try:
      db = self.conn[database]
      col = db[collection]
      col.create_index(key_or_list=index)
    except:
      print 'Create index failed.'
      print traceback.format_exc()
