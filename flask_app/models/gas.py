from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash,session
from flask_app.models import user
from geopy.geocoders import Nominatim

DB='gas'
class Gas:
    def __init__(self, data):
        self.id=data['id']
        self.address=data['address']
        self.city=data['city']
        self.state=data['state']
        self.gasprice=data['gasprice']
        self.datetime_seen=data['datetime_seen']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user=None
    @staticmethod
    def is_valid(data):
        valid=True
        flash_string='is required'
        if len(data['address'])<1:
            flash('address '+ flash_string,'gas')
            valid=False
        if len(data['city'])<1:
            flash('city '+flash_string,'gas')
            valid=False
        if len(data['state'])<1:
            flash('state '+flash_string,'gas')
            valid=False
        if len(data['datetime_seen'])<1:
            flash('time and date '+flash_string,'gas')
            valid=False
        if len(data['gasprice'])<=0:
            flash('gas price min 0','gas')
            valid=False
        return valid
    @staticmethod
    def address_latlon(id):
        address=Gas.by_id(id)
        loc=Nominatim(user_agent='mygeo')
      
        myGeo=loc.geocode(f'{address.address},{address.city},{address.state}')
       
        return myGeo

    @classmethod
    def gas_by_city(cls,city,state):
        data={
            'city':city,
            'state':state
        }
        list=[]
        query='SELECT * FROM gasprice join users on users.id=gasprice.user_id WHERE city=%(city)s and state=%(state)s'
        result=connectToMySQL(DB).query_db(query,data)
        if len(result) < 1:
            return False
        for i in result:
            a=cls(i)
            a.user=user.User({
                'id':i['user_id'],
                'first_name':i['first_name'],
                'last_name':i['last_name'],
                'email':i['email'],
                'password':i['password'],
                'created_at':i['users.created_at'],
                'updated_at':i['users.updated_at']
            })
            list.append(a)
        return list
    @classmethod
    def show_all(cls):
        query='SELECT * from gasprice join users on users.id=gasprice.user_id'
        stations=[]
        result= connectToMySQL(DB).query_db(query)
        for i in result:
            a=cls(i)
            a.user=user.User({
                'id':i['user_id'],
                'first_name':i['first_name'],
                'last_name':i['last_name'],
                'email':i['email'],
                'password':i['password'],
                'created_at':i['users.created_at'],
                'updated_at':i['users.updated_at']
            })
            stations.append(a)
        return stations
    @classmethod
    def show_all_city(cls):
        query='SELECT city,state from gasprice'
        return connectToMySQL(DB).query_db(query)

    @classmethod
    def save_gas(cls, data):
        if not Gas.is_valid(data):
            return False
        query='''INSERT INTO gasprice(address,city, state,datetime_seen,gasprice,user_id,updated_at,created_at)
        VALUES(%(address)s,%(city)s,%(state)s,%(datetime_seen)s,%(gasprice)s,%(user_id)s,NOW(),NOW())'''
        return connectToMySQL(DB).query_db(query,data)
    @classmethod
    def by_id(cls, id):
        data={'id':id}
        query='SELECT * FROM gasprice JOIN users ON users.id=gasprice.user_id where gasprice.id=%(id)s'
        result=connectToMySQL(DB).query_db(query,data)
        gas=result[0]
  
        gas_obj=cls(gas)
        gas_obj.user=user.User({
                'id':gas['users.id'],
                'first_name':gas['first_name'],
                'last_name':gas['last_name'],
                'email':gas['email'],
                'password':gas['password'],
                'updated_at':gas['users.updated_at'],
                'created_at':gas['users.created_at']

        })
  
        return gas_obj
    @classmethod
    def destroy(cls,id):
        this_gas=cls.by_id(id)
        if this_gas.user.id!=session['user_id']:
            return False
        data={'id':id}
        query='DELETE FROM gasprice where id=%(id)s'
        return connectToMySQL(DB).query_db(query,data)
    @classmethod
    def update(cls,data):
        this_gas=cls.by_id(data['id'])
        if this_gas.user.id!=session['user_id']:
            return False
        if not Gas.is_valid(data):
            return False
        query='''UPDATE gasprice SET address=%(address)s,city=%(city)s,state=%(state)s,gasprice=%(gasprice)s, datetime_seen=%(datetime_seen)s
        where id=%(id)s'''
        return connectToMySQL(DB).query_db(query,data)

    





