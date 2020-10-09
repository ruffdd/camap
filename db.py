import mysql.connector
import os
from flask import Flask
flask_app: Flask
development:bool=False
mydb = mysql.connector.connect(
  host="localhost",
  database="camap",
  user="camap",
  password="camaper"
)

cursor = mydb.cursor()

def tables():
  cursor.execute("show tables;")
  return cursor.fetchall()

def get_building(osm_id:int):
  result={}
  result['id']=osm_id
  result['name']=""
  result['description_url']=""
  result['adress_name']=""
  return result

def get_description_url(shortname:str):
  cursor.execute('SELECT fileurl FROM Descript WHERE shortname='+shortname+';')
  res= cursor.fetchall()
  return '' if res.__len__()==0 else res[0]

def set_description(path:str,text:str):
  assert path!=""

def update_building(input:dict):
  flask_app.logger.debug("add building data:"+ str(input))
  assert input['short_name']!=''

  desc_path = get_description_url(input['id'])
  if desc_path=="":
    desc_path='description-'+input['short_name']+'.html'
    cursor.execute("INSERT INTO Descript (shortname,title,fileurl) VALUES ('"+input['short_name']+"','"+input['name']+"','"+desc_path+"');")
  set_description(desc_path,input['description_content'])
  cursor.execute("INSERT INTO Adresses (shortname,street,campus,nr) VALUES ('"+input['short_name']+"','','',0);")
  cursor.execute("INSERT INTO OSMBuildings (id,adress,descript) VALUES ('"+input['id']+"','"+input['short_name']+"','"+input['short_name']+"');")

  if development:
    response=cursor.fetchall()
    flask_app.logger.debug(str(response))

def load_sql_file(name):
  path="./sql/"+ name +("" if name.endswith(".sql") else ".sql")
  file = open(path)
  commands=[]
  for line in file.read().split(";"):
    commands.append(line+";")
  #text = text.replace("\n","").strip().replace(";",";\n")
  return commands

def setup(app:Flask):
  global flask_app
  flask_app=app
  sql_file_name=""
  if len(tables()) == 0 :
      sql_file_name="setup"
  if(sql_file_name!=""):
    try:
      sql_file = load_sql_file(sql_file_name)
      for command in sql_file:
        flask_app.logger.debug("executing: "+command)
        cursor.execute(command)
      response = cursor.fetchall()
      flask_app.logger.info(str(response))

      flask_app.logger.info("created oder updated database")
    except FileNotFoundError:
      flask_app.logger.error('could no load sql file "' + sql_file_name+'" to initialize database')


