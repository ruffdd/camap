import mysql.connector
from os import getenv
import os
from flask import Flask
flask_app: Flask
development:bool=False
db_host=getenv("DB_HOST")
db_host=("localhost" if db_host=='' else db_host)
mydb = mysql.connector.connect(
  host=db_host,
  database="camap",
  user="camap",
  password="camaper"
)

cursor = mydb.cursor()

def tables():
  cursor.execute("show tables;")
  return cursor.fetchall()

def get_building(id:int):
  result={}
  result['id']=id
  cursor.execute("SELECT OSMBuildings.id,Descript.title,Descript.shortname,Descript.fileurl  FROM OSMBuildings LEFT JOIN Descript on OSMBuildings.descript=Descript.shortname WHERE OSMBuildings.id="+str(id)+";")
  response = cursor.fetchall()
  if response== []:
    return result
  response=response[0]
  result['id']=response[0]
  result['name']=response[1]
  result['short_name']=response[2]
  result['description_content']=get_description(response[3])
  return result

def get_description_url(shortname:str):
  cursor.execute("SELECT fileurl FROM Descript WHERE shortname='"+shortname+"';")
  res= cursor.fetchall()
  return '' if res.__len__()==0 else res[0]

def set_description(path:str,text:str):
  assert path!=""
  if not os.path.exists('data'):
    os.mkdir('data')
  file = open('data/'+path,'w+')
  file.write(text)
  file.close()

def get_description(url:str):
  file = open('data/'+url,'r')
  output = file.read()
  file.close()
  return output

def update_building(input:dict):
  flask_app.logger.debug("add building data:"+ str(input))
  assert input['short_name']!=''
  desc_path = get_description_url(input['short_name'])
  if desc_path=="":
    desc_path='description-'+input['short_name']+'.html'
    insert(cursor,'Descript',['shortname','title','fileurl'],[input['short_name'],input['name'],desc_path],True)
  set_description(desc_path[0],input['description_content'])
  insert(cursor,'Adresses', ['shortname','street','campus','nr'],[input['short_name'],'','',0],True)
  insert(cursor, 'OSMBuildings',['id','adress','descript'], [input['id'],input['short_name'],input['short_name']],True)
  mydb.commit()

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


def insert(cursor,table:str,columns:[],values:[],update:bool=False):
  assert len(columns) == len(values)
  command = "INSERT INTO "+table +' '
  command += str(columns).replace('[','(').replace(']',')').replace("'",'')
  command += " VALUES "
  command += str(values).replace('[','(').replace(']',')')
  if update:
    command += " ON DUPLICATE KEY UPDATE "
    for i in range(len(values)):
      command+=columns[i]+"='"+str(values[i])+"',"
    command=command[:-1]
  
  command += ';'
  cursor.execute(command)