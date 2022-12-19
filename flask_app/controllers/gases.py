from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user,gas
import os
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    cities=gas.Gas.show_all_city()
    list1=[]
    [list1.append(city) for city in cities if city not in list1]
        

    
    return render_template('dashboard.html',gas=gas.Gas.show_all(),user=user.User.get_by_id(session['user_id']),list=list1)
@app.route('/create_gas')
def create_gas():
    return render_template('create_gas.html')

@app.route('/delete/<int:id>')
def delete(id):
    gas.Gas.destroy(id)
    return redirect('/dashboard')
@app.route('/edit/<int:id>')
def edit(id):
    return render_template ('edit_gas.html',gas=gas.Gas.by_id(id),user=user.User.get_by_id(session['user_id']))    
@app.route('/view/<int:id>')
def view(id):
    location=gas.Gas.address_latlon(id)
    lat=location.latitude
    long=location.longitude
    api_key=os.environ.get('API_KEY')
    if lat:
        return render_template ('view_gas.html',lat=lat,long=long,api_key=api_key)  
    else:
        flash ('invalid address')
        return redirect ('/dashboard')
@app.route('/dashboard/<city>/<state>')
def view_bycity(city,state):
    return render_template ('dashboard_city.html',gases=gas.Gas.gas_by_city(city,state),user=user.User.get_by_id(session['user_id']),city=city,state=state)  
 

@app.route('/create',methods=['POST'])
def create():
    valid=gas.Gas.save_gas(request.form)
    if not valid:
        return redirect('/create_gas')
    return redirect('/dashboard')
@app.route('/update/<int:id>',methods=['POST'])
def update_gas(id):
    valid=gas.Gas.update(request.form)
    print(valid)
    if valid==False:
        return redirect(f'/edit/{id}')
    return redirect('/dashboard')
@app.route('/update_city',methods=['POST'])
def update_city():
    gas.Gas.gas_by_city(request.form['city'],request.form['state'])
    return redirect('/dashboard')