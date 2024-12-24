from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash
from datetime import date
from flask_mail import Mail,Message
import re
import joblib
import sklearn
import pyodbc as odbc


def is_valid_mobile(mobile):
    # This regex checks for a 10-digit mobile number starting with valid numbers (e.g., in India)
    pattern = r"^[6-9]\d{9}$"
    return re.match(pattern, mobile) is not None

def is_valid_email(email):
    # Define a regex for validating email format
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='vardaancontact1@gmail.com'
app.config['MAIL_PASSWORD']='qznk nluu xejv ebss'
app.config['MAIL_DEFAULT_SENDER']='vardaancontact1@gmail.com'
connection_string ='Driver={ODBC Driver 18 for SQL Server};Server=tcp:2203051050471.database.windows.net,1433;Database=vardaan;Uid=Rishabh;Pwd=Rishpu96;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
try:
    conn = odbc.connect(connection_string)
    print("Connection successful!")
except odbc.Error as e:
    print("Error:", e)
mail=Mail
Today=date.today()
date=Today

@app.route('/')
def first():
    if 'username' in session:
        username = session['username']
    else:
        username='nouser'     
    return redirect(url_for('home'))    



@app.route('/images/<filename>')
def images(filename):
    return send_from_directory('images', filename)

@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
    else:
        username='nouser' 
    return render_template('index.html',username=username)


@app.route('/donate')
def donate():
    if 'username' in session:
        username = session['username']
        contact="allowed"
    else:
        username='nouser'  
        contact="notallowed"
    #this is for wellwiher posts
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM wellwisher_posts WHERE status='active' ORDER BY post_id DESC ''')
    post_details=cursor.fetchall()
    cursor.close()
    return render_template('donate.html',username=username,contact=contact,post_details=post_details)


 
@app.route('/organizations')
def organizations():
 #this is for organization posts
    if 'username' in session:
        username = session['username']
        contact="allowed"
    else:
        username='nouser'  
        contact="notallowed"
    cursor=conn.cursor()
    cursor.execute(''' SELECT * FROM organization_posts WHERE status='active' ORDER BY post_id DESC ''')
    post_details=cursor.fetchall()
    cursor.close()
    return render_template('organizations.html',username=username,contact=contact,post_details=post_details)  

@app.route('/food')
def food():
    if 'username' in session:
        username = session['username']
        contact="allowed"
    else:
        username='nouser'
        contact="notallowed"
    cursor=conn.cursor()
    cursor.execute(''' SELECT * FROM food_post WHERE status='active' ORDER BY post_id DESC''')
    data=cursor.fetchall()
    cursor.close()
    return render_template('food.html',username=username,data=data,contact=contact)

@app.route('/login')
def login():
    username='nouser'
    return render_template('login.html',username=username)

@app.route('/register')
def register():
    username='nouser'
    return render_template('register.html',username=username)

@app.route('/forgotpassword')
def forgotpassword():
    username='nouser'
    return render_template('forgot.html',username=username)



@app.route('/orgregister', methods=['GET', 'POST'])
def orgregister():
    if request.method == "POST":
        try:
            # Fetching form data
            orgname = request.form['orgname']
            orgid = request.form['orgid']
            orgemail = request.form['orgemail']
            orgmobile = request.form['orgmobile']
            orgaddress = request.form['orgaddress']
            orgcountry = request.form['orgcountry']
            orgstate = request.form['orgstate']
            orgdesc = request.form['orgdesc']
            orgpswd = request.form['orgpswd']

            # Check if any mandatory field is missing
            if not all([orgname, orgid, orgemail, orgmobile, orgaddress, orgcountry, orgstate, orgdesc, orgpswd]):
                flash('All fields are required!', 'error')  # Flash error message if fields are missing
                return redirect('/orgregister')

            # Inserting the new organization into the database
            cursor = conn.cursor()

            # Check if the organization ID already exists to avoid duplicate entries
            cursor.execute('SELECT * FROM organization WHERE org_id = ?', (orgid,))
            existing_org = cursor.fetchone()
            if existing_org:
                flash('Organization ID already exists. Please choose a different ID.', 'error')
                return redirect('/orgregister')
            
            cursor.execute('SELECT * FROM organization WHERE org_name = ?', (orgname,))
            existing_orgname = cursor.fetchone()
            if existing_orgname:
                flash('Organization name already exists', 'error')
                return redirect('/orgregister')
            
            cursor.execute('SELECT * FROM organization WHERE org_email = ?', (orgemail,))
            existing_orgemail = cursor.fetchone()
            if existing_orgemail:
                flash('Organization email already exists.', 'error')
                return redirect('/orgregister')
            if not is_valid_email(orgemail):
                flash('please enter a valid email address','error')
                return redirect('/orgregister')
            
            cursor.execute('SELECT * FROM organization WHERE org_mobile= ?', (orgmobile,))
            existing_orgmobile = cursor.fetchone()
            if existing_orgmobile:
                flash('This mobile number already exists', 'error')
                return redirect('/orgregister')
            if not is_valid_mobile(orgmobile):
                flash('Please enter a valid mobile number')
                return redirect('/orgregister')
                

            # Insert data into the organization table
            cursor.execute('''INSERT INTO organization (org_name, org_id, org_email, org_mobile, org_address, org_country, org_state, description, org_pswd) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
               (orgname, orgid, orgemail, orgmobile, orgaddress, orgcountry, orgstate, orgdesc, orgpswd))

            
            
            # Commit the changes to the database
            cursor.commit()
            

            # Flash success message and redirect to login page
            flash('Organization registered successfully! Please log in.', 'success')
            return redirect('/orglogin')

        except Exception as e:
            # Handling any exceptions that occur during the registration process
            flash(f"An error occurred: {e}", 'error')
            return redirect('/orgregister')

    # Rendering the registration form for GET requests
    return render_template('register.html',username='nouser')

@app.route('/userregister', methods=['GET', 'POST'])
def userregister():
    if request.method == "POST":
        try:
            # Get form data
            username = request.form['username']
            name = request.form['name']
            mobile = request.form['mobile']
            email = request.form['email']
            address = request.form['address']
            password = request.form['password']

            # Check if any field is empty
            if not all([username, name, mobile, email, address, password]):
                flash('All fields are required!', 'error')
                return redirect('/userregister')

            # Database interaction
            cursor = conn.cursor()
            
            # Check if username already exists
            cursor.execute('SELECT username FROM wellwisher WHERE username = ?', (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Username already exists. Please choose another.', 'error')
                return redirect('/userregister')
            
            cursor.execute('SELECT email FROM wellwisher WHERE email = ?', (email,))
            existing_email=cursor.fetchone()

            if existing_email:
                flash('email already exists. Please choose another.', 'error')
                return redirect('/userregister')
            
            if not is_valid_email(email):
                flash('please enter a valid email address','error')
                return redirect('/orgregister')
            

            cursor.execute('SELECT mobileno FROM wellwisher WHERE mobileno = ?', (mobile,))
            existing_mobile=cursor.fetchone()

            if existing_mobile:
                flash('This phone number already exist. Please choose another.','error')
                return redirect('/userregister')
            
            if not is_valid_mobile(mobile):
                flash('Please enter a valid mobile number')
                return redirect('/userregister')
                
            # Insert new user into the database
            cursor.execute('''INSERT INTO wellwisher (username, name, mobileno, email, address, password) 
                              VALUES (?, ?, ?, ?, ?, ?)''', 
                           (username, name, mobile, email, address, password))
            cursor.commit()
            cursor.close()

            # Success message
            flash('Registration successful! Please log in.', 'success')
            return redirect('/login')
        except Exception as e:
            # Handle any other exceptions
            flash(f"An unexpected error occurred: {str(e)}", 'error')
            return redirect('/userregister')
    return render_template('register.html',username='nouser')




@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method == "POST":
        username=request.form['username']
        userpswd=request.form['userpswd']
        cursor=conn.cursor()
        cursor.execute(''' SELECT * FROM wellwisher WHERE username = ? and password = ? ''',(username,userpswd))
        login=cursor.fetchone()
        if login: 
            session['who']='wellwisher'
            session['username']=request.form['username']
            cursor.execute(''' SELECT email FROM wellwisher WHERE username= ? ''',(username,))
            email=cursor.fetchone()
            session['email'] = email[0] if email else None
            return redirect('/home')
        else:
           flash('Invalid username or password', 'error')
        return redirect('/login')

@app.route('/orglogin', methods=['GET', 'POST'])
def orglogin():
    if request.method == "POST":
        orgid=request.form['orgid']
        password=request.form['orgpswd']
        cursor=conn.cursor()
        cursor.execute(''' SELECT * FROM organization WHERE org_id = ? and org_pswd =? ''',(orgid,password))
        login=cursor.fetchone()
        cursor.close()
        if login:
            session['who']='organization'
            cursor=conn.cursor()
            cursor.execute(''' SELECT org_name FROM organization WHERE org_id =? ''',(orgid,))
            org_name=cursor.fetchone()[0]
            cursor.execute(''' SELECT org_email FROM organization WHERE org_id =? ''',(orgid,))
            email=cursor.fetchone()[0]
            cursor.close()
            session['username']=org_name
            session['email']=email
            return redirect('/home')
        else:
           flash('Invalid username or password', 'error')
        return redirect('/login')   
        
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username','nouser')
    return redirect(url_for('home'))

@app.route('/post')
def post():
    if 'username' in session:
        username = session['username']
    else:
        username='nouser'
    if session['who']=='organization':
        user='organization'
    else:
        user='wellwisher'    
    return render_template('post.html',user=user,username=username)

@app.route('/posting',methods=['GET','POST'])
def posting():
    global date
    if request.method=='POST':
        postdesc = request.form['postdesc']
        cursor = conn.cursor()

        v=joblib.load('vardaanpost.pkl')
        model=joblib.load('postingspam')
    
  
        test=v.transform([postdesc])
        prediction= model.predict(test)

        if(prediction==0):
            flash("This Post is not a appropriate post for this website")
            return redirect('/post')
        else:
            if session['who']=='organization':
                user='organization'
                username=session['username']
            else:
                user='wellwisher' 
                username=session['username']

            if user=='organization': 
                cursor.execute(''' SELECT org_address FROM organization WHERE org_name=?''',(username,))
                useraddress = cursor.fetchone()[0]
                cursor.execute(''' SELECT org_id FROM organization WHERE org_name=?''',(username,))
                org_id = cursor.fetchone()[0]
                cursor.execute('INSERT INTO organization_posts (org_id,org_name,postdesc,org_address,date) VALUES(?,?,?,?,?)',(org_id,username,postdesc,useraddress,date))
                cursor.commit()
                cursor.close()
                return redirect('/organizations')
            else:
                #selecting name instead of username and address
                cursor.execute('SELECT userid from wellwisher WHERE username=?',(username,))
                userid=cursor.fetchone()[0]
                cursor.execute('SELECT name from wellwisher WHERE username=?',(username,))
                name = cursor.fetchone()[0]
                cursor.execute('SELECT address from wellwisher WHERE username=?',(username,))
                address = cursor.fetchone()[0]
                cursor.execute('INSERT INTO wellwisher_posts (userid,username,name,postdesc,date,address) VALUES(?,?,?,?,?,?)',(userid,username,name,postdesc,date,address))
                cursor.commit()
                cursor.close()
                return redirect('/donate')        
    return redirect('/post')
    
@app.route('/foodposting',methods=['POST','GET'])
def foodposting():
    global date
    if request.method=='POST':
        postdesc=request.form['postdesc']

        v=joblib.load('vardaanpost.pkl')
        model=joblib.load('postingspam')
  
        test=v.transform([postdesc])
        prediction= model.predict(test)

        if(prediction==0):
            return"You cannot post this post as this post may contain asking for money"

        qtyalv=request.form['avlqty']
        pickloc=request.form['pickup']
        picktime=request.form['picktime']

        cursor=conn.cursor()

        username=session['username']
        cursor.execute('SELECT userid from wellwisher WHERE username=?',(username,))
        userid=cursor.fetchone()[0]
        cursor.execute('SELECT name from wellwisher WHERE username=?',(username,))
        name = cursor.fetchone()[0]
        cursor.execute('SELECT address from wellwisher WHERE username=?',(username,))
        address = cursor.fetchone()[0]
        cursor.execute(''' INSERT INTO food_post (username,userid,name,postdesc,qtyavl,pickuplocation,pickuptime,address,date) VALUES (?,?,?,?,?,?,?,?,?)''',(username,userid,name,postdesc,qtyalv,pickloc,picktime,address,date))
        cursor.commit()
        cursor.close()
    return redirect('/food')
        

@app.route('/orgcontact',methods=['POST','GET'])
def orgcontact():
    if request.method=="POST":
        orgname=request.form['orgname']
        cursor=conn.cursor()
        cursor.execute(''' SELECT org_mobile FROM organization WHERE org_name=? ''',(orgname,))
        mobile=cursor.fetchone()[0]
        cursor.execute(''' SELECT org_email FROM organization WHERE org_name=? ''',(orgname,))
        email=cursor.fetchone()[0]
        recipient=session['email'][0]
        cursor.close()
        msg=Message('Vardaan',recipients=[recipient])
        msg.body = f"""As you requested for the details of {orgname} for donations, here are the details:
        \nEmail: {email}
        \nMobile number: {mobile}
        \nThank you for helping society by taking the initiative!
        \nVardaan"""
        mail.send(msg)
        return redirect('/organizations')

@app.route('/usercontact',methods=['POST','GET'])  
def usercontact():
    if request.method=='POST':
        username=request.form['username']
        postid=request.form['postid']
        cursor=conn.cursor()
        cursor.execute('SELECT name FROM wellwisher_posts WHERE username = ?',(username,))
        name=cursor.fetchone()[0]
        cursor.execute(''' SELECT email FROM wellwisher WHERE username=?''',(username,))
        email=cursor.fetchone()[0]
        cursor.execute('SELECT mobileno FROM wellwisher WHERE username = ?',(username,))
        mobile=cursor.fetchone()[0]
        recipient=session['email'][0]
        cursor.execute('SELECT postdesc FROM wellwisher_posts WHERE post_id = ?',(postid,))
        post_desc=cursor.fetchone()[0]
        cursor.close()
        msg=Message('Vardaan',recipients=[recipient])
        msg.body=f"""As you requested for the details of {name} for :
        \n{post_desc}, here are the details:
        \nEmail: {email}
        \nMobile number: {mobile}
        \nThank you for helping society by taking the initiative!
        \nVardaan"""
        mail.send(msg)
        return redirect('/donate')

@app.route('/foodcontact',methods=['POST','GET'])
def foodcontact():
    if request.method=='POST':
        username=request.form['username']
        postid=request.form['postid']
        cursor= conn.cursor()
        cursor.execute('SELECT name FROM food_post WHERE username = ?',(username,))
        name=cursor.fetchone()[0]
        cursor.execute(''' SELECT email FROM wellwisher WHERE username=?''',(username,))
        email=cursor.fetchone()[0]
        cursor.execute('SELECT mobileno FROM wellwisher WHERE username = ?',(username,))
        mobile=cursor.fetchone()[0]
        recipient=session['email'][0]
        cursor.execute('SELECT postdesc FROM food_post WHERE post_id = ?',(postid,))
        post_desc=cursor.fetchone()[0]
        cursor.close()
        msg=Message('Vardaan',recipients=[recipient])
        msg.body=f"""As you requested for the details of {name} for :
        \n{post_desc}, here are the details:
        \nEmail: {email}
        \nMobile number: {mobile}
        \nThank you for helping society by taking the initiative!
        \nVardaan"""
        mail.send(msg)
        return redirect('/food')

@app.route('/myposts')
def myposts():
    if 'username' in session:
        username = session['username']    
    else:
        username='nouser'
    cursor=conn.cursor()
    if session['who']=='wellwisher':
        user='wellwisher'
        cursor.execute('SELECT  * FROM wellwisher_posts WHERE username=? and status=?',(username,'active'))
        table1=cursor.fetchall()   
        cursor.execute('SELECT * FROM food_post WHERE username =? and status=?',(username,'active'))
        table2=cursor.fetchall()
        return render_template('myposts.html',username=username,table1=table1,table2=table2,user=user)
    else:
        user='organization'
        cursor.execute('SELECT * FROM organization_posts WHERE org_name=? and status=?',(username,'active'))  
        data=cursor.fetchall()  
        return render_template('myposts.html',username=username,data=data,user=user)

@app.route('/userdeletepost',methods=['POST','GET']) 
def deletepost():
    if request.method=='POST':
        postid=request.form['postid']
        posttype=request.form['posttype']
        cursor=conn.cursor()
        if posttype=='foodpost':
            cursor.execute(''' UPDATE food_post SET status=? WHERE post_id=? ''',('Closed',postid))
            cursor.commit()
        else:    
         cursor.execute(''' UPDATE wellwisher_posts SET status=? WHERE post_id=? ''',('Closed',postid))
         cursor.commit()
        cursor.close()
        return redirect('/myposts')

@app.route('/orgdeletepost',methods=['POST','GET'])
def orgdeletepost():
    if request.method=='POST':
        postid=request.form['postid']
        cursor=conn.cursor()
        cursor.execute('''UPDATE organization_posts SET status=? WHERE post_id=? ''',('Closed',postid))
        cursor.commit()
        cursor.close()
        return redirect('/myposts')

if __name__ == '__main__':
    app.run(debug=True)