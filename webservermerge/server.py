#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
import random
from datetime import datetime,date
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


# configuration
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111db.eastus.cloudapp.azure.com/username
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db.eastus.cloudapp.azure.com/ewu2493"
#
#DATABASEURI = "sqlite:///test.db"

DATABASEURI = "postgresql://cx2178:RDATHT@w4111db.eastus.cloudapp.azure.com/cx2178"



#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
# 
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
# 
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
# 
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#
#engine.execute("""DROP TABLE IF EXISTS test;""")
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
#
# END SQLITE SETUP CODE
#

uid = '111111'

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  #print request.args


  #
  # example of a database query
  #


  #cursor = g.conn.execute("SELECT * FROM users")
  #names = []
  #for result in cursor:
    #names.append(result['username'])  # can also be accessed using result[0]
  #cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html",uid=uid)

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
@app.route('/another',methods=['GET', 'POST'])
def another():
    error=None
    shopid=request.args.get('shopid')
    print shopid
    shopnames = g.conn.execute("SELECT shopname from shops WHERE shopid = '%s'"%shopid)
    shopname = ' '
    for result in shopnames:
	    shopname = result[0]
    shopnames.close()


    if request.method=='POST':
        #place order:
        if request.form['submit'] == 'Place Order' :
            if uid == '111111':
		        print 'yea'
		        error = 'Please log in before place Order'
		        return render_template("anotherfile.html", uid = uid, error=error, shopid = shopid)
            ordertime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ordernum = random.randrange(10000000,99999999)
            cur2=g.conn.execute("SELECT ordernum from orders")
            existnum=[]
            for result in cur2:
                existnum.append(result[0])
            cur2.close()
#          print existnum
            while ordernum in existnum:
		        ordernum = random.randrange(10000000,99999999)
            order_content = request.form['order_content']
            type = request.form['Take_out_Delivery']
            if request.form['Take_out_Delivery'] == 'none':
		        error = 'Please fill in the required fields'
  	                return render_template("anotherfile.html", uid = uid, error=error, shopid = shopid)
	    elif request.form['Take_out_Delivery'] == 'delivery':
			delivery_options = g.conn.execute("SELECT s_delivery FROM shops WHERE shopid = %s",(shopid))
			for option in delivery_options:
				delivery_option = option[0]
			print delivery_option
			if str(delivery_option) == 'False' or delivery_option == 'f':
				error = 'This shop cannot deliver.'
				return render_template("anotherfile.html", error=error, uid = uid, shopid = shopid)
		        delivery_address_aptnum = request.form['aptnum']
		        delivery_address_street = request.form['street']
		        delivery_address_city = request.form['city']
		        delivery_address_state = request.form['state']
		        delivery_address_postcode = request.form['postcode']
		        if not delivery_address_postcode.isdigit():
			        return render_template("anotherfile.html",  uid = uid, error = 'Please fill in valid postcode', shopid = shopid)
		        address = delivery_address_aptnum + ', ' + delivery_address_street + ', ' + delivery_address_city + ', ' + delivery_address_state + ', ' + delivery_address_postcode
		        print order_content
		        if not order_content.strip() or not delivery_address_aptnum.strip() or not delivery_address_city.strip() or not delivery_address_street.strip() or not delivery_address_state.strip():
			        print 'place order'
			        error = 'Please fill in the required fields'
                                return render_template("anotherfile.html", error=error, uid = uid, shopid = shopid)
	  	        else:
			        q = (ordernum, uid, shopid, 'f', 't', ordertime, order_content)
			        i ="INSERT INTO orders(ordernum, userid, shopid, istakeout, isdelivery, ordertime, context) VALUES(%s, %s, %s, %s, %s, %s, %s);"
			        print i
			        g.conn.execute(i, q)
			        print 'finish inserting order'
			        q = (delivery_address_aptnum, delivery_address_street, 'None', delivery_address_city, delivery_address_state, delivery_address_postcode)
                    		i ="INSERT INTO address(aptnum, street, district, city, state, postcode) VALUES(%s, %s, %s, %s, %s, %s);"
                    		print i
                    		g.conn.execute(i, q)
                    		print 'finish inserting address'
			        q = (ordernum, delivery_address_aptnum, delivery_address_street, delivery_address_city, delivery_address_state, delivery_address_postcode, ordertime)
			        i ="INSERT INTO deliver(ordernum, aptnum, street, city, state, postcode, deliverytime) VALUES(%s, %s, %s, %s, %s, %s, %s);"
                    		print i
                    		g.conn.execute(i, q)
                    		print 'finish inserting deliver'
			        return render_template("PlaceOrderSuccess.html", type = type, shopid = shopid, ordernum = ordernum, order_content = order_content, ordertime = ordertime, shopname = shopname, address = address)
	    else:
			takeout_options = g.conn.execute("SELECT s_takeout FROM shops WHERE shopid = %s",(shopid))
                        for option in takeout_options:
				takeout_option = option[0]
			print takeout_option
                        if str(takeout_option) == 'False' or takeout_option == 'f':
                                error = 'This shop cannot takeout.'
                                return render_template("anotherfile.html", error=error, uid = uid, shopid = shopid)
                	order_content = request.form['order_content']
                	if not order_content.strip():
                    		error = 'Please fill in the required fields'
                    		return render_template("anotherfile.html", error=error, uid = uid, shopid = shopid)
                	else:
			        q = (ordernum, uid, shopid, 'f', 't', ordertime, order_content)
                    		i ="INSERT INTO orders(ordernum, userid, shopid, istakeout, isdelivery, ordertime, context) VALUES(%s, %s, %s, %s, %s, %s, %s);"
                    		print i
                    		g.conn.execute(i, q)
                    		print 'finish inserting order'
			        return render_template("PlaceOrderSuccess.html", type = type, shopid = shopid, ordernum = ordernum, order_content = order_content, ordertime = ordertime, shopname = shopname)


        #write comments
        if request.form["submit"]=="Write a comment":
            cmtwrt=request.form['comments']
            print cmtwrt

            if uid=='111111':
                print "ye"
                error='Please login first'
                return render_template('anotherfile.html', error=error, uid = uid, shopid = shopid)
            else:
                cmttime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print cmttime
                v_funnynum=0
                v_coolnum=0
                v_useful=0
                q="SELECT MAX(labelnum) FROM comments WHERE shopid='%s'"%shopid
                #print q
                lastlabel=g.conn.execute(q)
                #label=[]
                for result in lastlabel:
                #    print result
                    if result[0]== None:
                        label=1
                    else:
                        label=result[0]+1
                lastlabel.close()

                args=(label,shopid,uid,cmttime,cmtwrt,v_funnynum,v_coolnum,v_useful)
                qi="INSERT INTO comments VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                g.conn.execute(qi, args)
                #return redirect('/')

        if request.form["submit"]=="Like it":
            if uid=='111111':
                print "ye"
                error='Please login first'
                return render_template('anotherfile.html', uid = uid, error=error)
            else:
                # check if the record has already existed
                cur1=g.conn.execute("SELECT userid from likes")
                existuser=[]
                for result in cur1:
                    existuser.append(result[0])
                cur1.close()
                print existuser

                if uid in existuser:
                    cur2=g.conn.execute("SELECT shopid from likes WHERE userid='%s'"%uid)
                    existshop=[]
                    for result in cur2:
                        existshop.append(result[0])
                    cur2.close()
                    print existshop
                    if shopid in existshop:
                        error='You have liked this shop!'
                        return render_template('anotherfile.html', uid = uid, shopid=shopid,error=error)

                # insert new record
                ltime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print ltime
                args=(uid,shopid,ltime)
                qi="INSERT INTO likes VALUES(%s,%s,%s)"
                g.conn.execute(qi, args)

                q="SELECT DISTINCT u.username FROM likes l, users u WHERE u.userid<>'%s'"%uid +" AND u.userid=l.userid AND l.shopid='%s'"%shopid
                print q
                lpeople=g.conn.execute(q)
                people=[]
                flag=0
                for result in lpeople:
                    flag=1
                    people.append(result[0]+"  ")
                if flag==0:
                    people.append("No other people liked this shop yet... You are the first!")
                lpeople.close()
                #print people
                q2="SELECT DISTINCT s.shopname FROM likes l, shops s WHERE s.shopid<>'%s'"%shopid +" AND s.shopid=l.shopid AND l.userid='%s'"%uid
                print q2
                lh=g.conn.execute(q2)
                hist=[]
                for result in lh:
                        hist.append(result[0]+"  ")
                lh.close()
                return render_template("like.html", data=people,lhist=hist)


        if request.form["submit"]=="Reserve it":
            if uid=='111111':
                print "ye"
                error='Please login first'
                return render_template('anotherfile.html', uid = uid, error=error)
            else:

                #deal with input error
                num=str(request.form['pnum'])

                try:
                    num=int(num)
                except:
                    error='Please input people number as a number'
                    return render_template('anotherfile.html', uid = uid,shopid=shopid,error=error)

                rtime=datetime.now()
                d=request.form['rdate']
                t=request.form['rtime']
                if d=='' or t=='' or num=='':
                    error='Please input your reservation time and people number'
                    return render_template('anotherfile.html', uid = uid,shopid=shopid,error=error)
                dtime=str(d+' '+t)
                djudge=datetime.strptime(d, "%Y-%m-%d")

                if (djudge-rtime).seconds<1800 or (djudge-rtime).days<0:
                    error="reservation time is invalid. Please input again"
                    return render_template('anotherfile.html', uid = uid,shopid=shopid,error=error)

                sh=g.conn.execute("SELECT starthour from shops WHERE shopid='%s'"%shopid)
                for result in sh:
                    starthour=str(result[0])
                sh.close()
                eh=g.conn.execute("SELECT closehour from shops WHERE shopid='%s'"%shopid)
                for result in eh:
                    endhour=str(result[0])
                eh.close()
                print "query business hour complete"

                starthour=datetime.strptime(starthour, "%H:%M:%S")
                endhour=datetime.strptime(endhour, "%H:%M:%S")
                t=datetime.strptime(t, "%H:%M:%S")
                print starthour,endhour,t
                if starthour<endhour:
                    if t<starthour or t>endhour:
                        error="The time you reserve is not the shop's business hour!"
                        return render_template('anotherfile.html', uid = uid,shopid=shopid,error=error)
                else:
                    if t<starthour and t>endhour:
                        error="The time you reserve is not the shop's business hour!"
                        return render_template('anotherfile.html',shopid=shopid, uid = uid,error=error)


                #print rtime
                #deal with existed record in database
                cur1=g.conn.execute("SELECT userid from reserve")
                existuser=[]
                for result in cur1:
                    existuser.append(result[0])
                cur1.close()
                print existuser
                if uid in existuser:
                    cur2=g.conn.execute("SELECT DISTINCT shopid from reserve WHERE userid='%s'"%uid+" AND rdate='%s'"%dtime)
                    existshop=[]
                    for result in cur2:
                        existshop.append(result[0])
                    cur2.close()
                    print existshop
                    if shopid in existshop:
                        error='You have reserved this shop for that time!'
                        return render_template('anotherfile.html', shopid=shopid, uid = uid,error=error)

                # insert new record
                args=(uid,shopid,dtime,num)
                qi="INSERT INTO reserve VALUES(%s,%s,%s,%s)"
                g.conn.execute(qi, args)

                #show relevant info
                q="SELECT DISTINCT u.username FROM reserve r, users u WHERE u.userid<>'%s'"%uid +" AND u.userid=r.userid AND r.shopid='%s'"%shopid
                print q
                rpeople=g.conn.execute(q)
                people=[]
                flag=0
                for result in rpeople:
                    flag=1
                    people.append(result[0]+"  ")
                if flag==0:
                    people.append("No other people reserved this shop yet...")
                rpeople.close()
                #print people
                q2="SELECT DISTINCT s.shopname FROM reserve r, shops s WHERE s.shopid<>'%s'"%shopid +" AND s.shopid=r.shopid AND r.userid='%s'"%uid
                print q2
                rh=g.conn.execute(q2)
                hist=[]
                for result in rh:
                        hist.append(result[0]+"  ")
                rh.close()
                return render_template("reserve.html", data=people,rhist=hist)

        if request.form["submit"]=="Rate it":
            if uid=='111111':
                print "ye"
                error='Please login first'
                return render_template('anotherfile.html', error=error, uid = uid)
            else:

                #deal with input error
                rscore=str(request.form["score"])
                try:
                    rscore=float(rscore)
                    if rscore>5:
                        error='Your rating score should be smaller than 5'
                        return render_template('anotherfile.html',shopid=shopid,  uid = uid,error=error)
                except:
                    error='Please input your rating score as a number smaller than 5'
                    return render_template('anotherfile.html',shopid=shopid, uid = uid,error=error)

                print rscore

                # deal with existed record in database
                cur1=g.conn.execute("SELECT userid from rate")
                existuser=[]
                for result in cur1:
                    existuser.append(result[0])
                cur1.close()
                print existuser
                if uid in existuser:
                    cur2=g.conn.execute("SELECT shopid from rate WHERE userid='%s'"%uid)
                    existshop=[]
                    for result in cur2:
                        existshop.append(result[0])
                    cur2.close()
                    print existshop
                    if shopid in existshop:
                        error='You have rated this shop before!'
                        return render_template('anotherfile.html', shopid=shopid, uid = uid,error=error)

                #insert new record
                ratetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                args=(uid,shopid,ratetime,rscore)
                qi="INSERT INTO rate VALUES(%s,%s,%s,%s)"
                g.conn.execute(qi, args)

                #show relevant info
                q="SELECT u.username,r.score FROM rate r, users u WHERE u.userid<>'%s'"%uid +" AND u.userid=r.userid AND r.shopid='%s'"%shopid
                print q
                rpeople=g.conn.execute(q)
                people=[]
                flag=0
                for result in rpeople:
                    flag=1
                    people.append(result[0]+"  "+str(result[1]))
                if flag==0:
                    people.append("No other people rated this shop yet...")
                rpeople.close()
                return render_template("rate.html", data=people,score=rscore)


            #g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
            #return redirect('/')

    # query and display
    q="SELECT s.shopname,s.rating_score,to_char(s.starthour,'HH24:MI:SS'),to_char(s.closehour,'HH24:MI:SS'),s.contactinfo,s.avg_cost,s.cusine_type,s.shoptype,s.s_takeout,s.s_delivery FROM shops s WHERE s.shopid='%s'"%shopid
    print q
    cur = g.conn.execute(q)
    shopinfo=[]
    for result in cur:
        shopinfo.append(result[0]+"   "+str(result[1])+"   "+result[2]+"   "+result[3]+"   "+result[4]+"   "+str(result[5])+"   "+result[6]+"   "+result[7]+"   "+str(result[8])+"   "+str(result[9]))   # can also be accessed using result[0]
    print shopinfo  
    cur.close()

    cur2=g.conn.execute("SELECT context FROM comments WHERE shopid='%s' LIMIT 3"%shopid)
    comments=[]
    for result in cur2:
        comments.append(result[0])   # can also be accessed using result[0]

    cur2.close()

    cur3=g.conn.execute("SELECT l.aptnum,l.street,l.city,l.state,l.postcode FROM locate_in l WHERE l.shopid='%s'"%shopid)
    adds=[]
    aflag=0	
    for result in cur3:
	aflag=1
        adds.append(result[0]+"   "+str(result[1])+"   "+result[2]+"   "+result[3]+"   "+result[4])   # can also be accessed using result[0]

    cur3.close()
    if aflag==0:
	adds.append("Information not provided")	
    print adds



    return render_template("anotherfile.html",data=shopinfo,cmts=comments,address=adds, uid = uid,shopid=shopid)

# @app.route('/login')
# def login():
#     return render_template("login.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
       username = request.form['username']
       passwords = g.conn.execute("SELECT password FROM users WHERE username=%s",(username))
       error = 'No Such User'
       uids = g.conn.execute("SELECT userid FROM users WHERE username=%s",(username))
       for id in uids:
           global uid
           uid = id[0]
#	   print uid
       for password in passwords:
	   getpassword = password[0]
           if request.form['password'] != getpassword:
                error = 'Login Error, Try Again'
           else:
#               session['logged_in'] = True
             	print 'You were logged in'
               	return render_template("index.html", uid = uid)
       passwords.close();
       uids.close();
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    global uid
    uid = "111111"
    print('You were logged out')
    return render_template("index.html", uid = uid)

@app.route('/createaccount', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        print 'here'
        username = request.form['username']
        usernames = g.conn.execute("SELECT username from users")
        users = []
        for result in usernames:
            users.append(result[0])
        if username in users:
            return render_template("createaccount.html", error = 'User Already Exist')
        usernames.close()
        useridcreate = list(username)
	if "'" in useridcreate or ")" in useridcreate or ";" in useridcreate or "(" in useridcreate:
		return render_template("createaccount.html", error = "User name contains illegal characters.") 
        if(len(useridcreate)<3):
            return render_template("createaccount.html", error = 'Username must be longer than 3 characters')
        userid = str(useridcreate[0]) + str(useridcreate[1]) + str(useridcreate[1]) + str(useridcreate[0]) + str(useridcreate[1]) + str(useridcreate[1])
        useridlist = g.conn.execute("SELECT userid from users")
        userids = []
        for result in useridlist:
            userids.append(result[0])
        i=0
        while userid in userids:
            userid = str(useridcreate[0]) + str(useridcreate[1]) + str(useridcreate[1]) + str(useridcreate[0]) + str(useridcreate[1]) + str(useridcreate[1]) + str(i)
            i = i+1
        print 'username success'
        password1 = request.form['password1']
        password2 = request.form['password2']
        if password1 != password2:
            return render_template("createaccount.html", error = 'The passwords you entered must be the same.')
        g.conn.execute("INSERT INTO users(userid, password, username) VALUES (%s, %s, %s)", (userid, password1, username))
        print 'create user successfully'
        global uid
        uid = userid
        return render_template("index.html", uid = uid)
    return render_template("createaccount.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')


#show restuarants according to filter

reslist=[]
@app.route('/restlist', methods=['POST'])
def restlist():
  shops = []
  names = []
  if request.form["submit"] == "Search nearby!" :
      neararea=request.form['Near']
      if neararea=="none":
          q="SELECT shopname,rating_score,shopid FROM shops ORDER BY rating_score DESC"
          print q
          cur = g.conn.execute(q)
      else:
          q="SELECT s.shopname,s.rating_score,s.shopid FROM shops s,locate_in l WHERE l.shopid=s.shopid AND l.postcode='%s' ORDER BY rating_score DESC"%neararea
          print q
          cur = g.conn.execute(q)

      names = []
      #rating=[]
      print cur
      for result in cur:
          names.append(result[0]+"   "+str(result[1])+"   "+result[2])   # can also be accessed using result[0]
          #rating.append(result[1])
      cur.close()
      data = names

  if request.form["submit"] == "Apply!" :
      type = request.form['Type']
      area = request.form['Area']
      take_out = request.form['Take_out']
      delivery = request.form['Delivery']
      sort=request.form['Sort']
      if sort=="none":
          ratingsort=""
      if sort=="DESC":
          ratingsort=" DESC"

      if type=="none" and area=="none" and take_out=="none" and delivery=="none":
          q="SELECT shopname,rating_score,shopid FROM shops ORDER BY rating_score"+ratingsort
          print q
          cur = g.conn.execute(q)
      else:
          w=" WHERE"
          if type=="none":
              stp=""
          else:
              stp=" s.shoptype='%s'"%type

          if area=="none":
              sa=""
              l=""
              alian=""
          else:
              alian=""
              sa=" l.shopid=s.shopid AND l.postcode='%s'"%area
              l=",locate_in l"
              if type!="none":
                  alian=" AND"

          if take_out=="none":
              stake=""
              tlian=""
          else:
              tlian=""
              stake=" s.s_takeout='%s'"%take_out
              if type!="none" or area!="none":
                  tlian=" AND"

          if delivery=="none":
              sd=""
              slian=""
          else:
              slian=""
              sd=" s.s_delivery='%s'"%delivery
              if type!="none" or area!="none" or take_out!="none":
                  slian=" AND"

          #cur = g.conn.execute('SELECT s.shopname FROM shops s,locate_in l WHERE s.shopid=l.shopid AND s.shoptype=type AND l.postcode=area AND s.s_takeout=take_out AND s.s_delivery=delievery')
          #q = 'SELECT s.shopname FROM shops s WHERE s.shoptype=%s AND s.s_takeout=%s'
          q="SELECT s.shopname,s.rating_score,s.shopid FROM shops s"+l+w+stp+alian+sa+tlian+stake+slian+sd+" ORDER BY s.rating_score"+ratingsort
          #q="SELECT s.shopname FROM shops s"+l+w+stp+alian+sa
          #q="SELECT s.shopname FROM shops s"+l+w+stp+tlian+stake

          print q
          cur = g.conn.execute(q)
          #cur = g.conn.execute(q,type,take_out)

      names=[]
      #rating=[]
      print cur
      for result in cur:
          names.append(result[0]+"   "+str(result[1])+"   "+result[2])   # can also be accessed using result[0]
          #rating.append(result[1])
      cur.close()
      global reslist
      reslist=names
      data = names

  if request.form["submit"] == "Order History" :
      if uid == '111111':
          return render_template("index.html", uid = uid, error = 'Please Login First')
      shopnames = g.conn.execute("SELECT DISTINCT s.shopname, s.rating_score, s.shopid FROM shops s, orders o WHERE s.shopid = o.shopid AND o.userid='%s'"%uid)
      for shopname in shopnames:
          shops.append(shopname[0]+"   "+str(shopname[1])+"   "+shopname[2])
#      print shops
      shopnames.close()
      print shops
      data = shops
      print data
#  elif  ( $_REQUEST['orderhistory'] )
  #g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return render_template("index.html", data=data, uid = uid)


#for n in reslist:








if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    #print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()



