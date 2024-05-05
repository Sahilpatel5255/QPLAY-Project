from flask import Flask, render_template, request, redirect, session,jsonify
from flask_cors import CORS
import  random
 
import psycopg2

app = Flask(__name__)

# Function to establish a database connection
def get_db_connection():
    conn = psycopg2.connect(database="postgres", user="postgres", password="13552089", host="localhost", port="5432")
    return conn


################################################################################################
# Render index page
@app.route('/')
def index():
    return render_template('index.html')


# Render login page
@app.route('/login')
def lg():
    return render_template('login.html')



# Render signup page
@app.route('/signup')
def sg():
    return render_template('signup.html')


#login handler for login 
@app.route('/login', methods=['POST'])
def login_handler():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        
        # Use parameterized queries to prevent SQL injection
        query = "SELECT * FROM logindb WHERE loguser = %s AND logpass = %s"
        cursor.execute(query, (username, password))
        user_data = cursor.fetchone()  # Fetch the first matching row
        
        cursor.close()
        db_connection.close()

        if user_data:
            # User with provided credentials found in the database
            return render_template('dashboard.html', user_data=user_data)
        else:
            # User not found in the database
            return render_template('login.html', message='Invalid credentials')
    else:
        return render_template('login.html')

        



@app.route('/signup', methods=['POST'])
def signup_handler():
    if request.method == 'POST':
        try:
            username = request.form.get('signup-username')
            name = request.form.get('email')
            password = request.form.get('signup-password')
            confirm_password = request.form.get('confirm-password')

            # Check if passwords match
            if password != confirm_password:
                return render_template('signup.html', message='Passwords do not match')

            # Establish a database connection
            db_connection = get_db_connection()
            cursor = db_connection.cursor()

            # Insert data into the database
            query = "INSERT INTO logindb (loguser, logpass, name) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, name))
            db_connection.commit()

            cursor.close()
            db_connection.close()

            return render_template('login.html', message='Signup successful. Please login.')

        except Exception as e:
            # Print the exception for debugging purposes
            print(e)
            return render_template('signup.html', message='Error during signup')

    else:
        return render_template('signup.html')
    


    # Route to render the dashboard page
@app.route('/dashboard')
def dashboard():


    return render_template('dashboard.html')
    
   

#test planner    

@app.route('/plantest')

def pt():
    return render_template('planttest.html')

@app.route('/plantest', methods=['POST'])
def plan_handler():
    if request.method == 'POST':
        qno = request.json['numQuestions']
        subject = request.json['Subject']
        chapter = request.json['Chapter']
        # print(request.json)
        data=[]
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        query = "SELECT * FROM questionset where subject='"+subject+"' and chapter='"+chapter+"';"
        # print(query)
        cursor.execute(query)
        for i in cursor.fetchall():
            data.append({"question":i[1 ],"op1":i[2],"op2":i[3],"op3":i[4],"op4":i[5],"correct":i[6],"qid":i[8]})
        # print(data)
        random.shuffle(data)

        cursor.execute("DELETE FROM tempques;")
        db_connection.commit()

        for i in range(int(qno)):
            print(data[i])
            q="INSERT INTO public.tempques(question, option_a, option_b, option_c, option_d, correctans, qid) VALUES ('"+data[i]['question']+"', '"+data[i]['op1']+"', '"+data[i]['op2']+"', '"+data[i]['op3']+"', '"+data[i]['op4']+"', '"+data[i]['correct']+"', '"+data[i]['qid']+"');"
            print(q)
            cursor.execute(q)
            db_connection.commit()

        if data:
            return jsonify("ok"), 200 
        else:
            return jsonify("error"), 400 
    
#data transfer from databese tempques to frontend 

@app.route('/ques')
def getques():
   
    data=[]
    db_connection = get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM tempques")
    for i in  cursor.fetchall():
        data.append({"question":i[0],"op1":i[1],"op2":i[2],"op3":i[3],"op4":i[4]})
    return jsonify(data)
        



@app.route('/welcome')
def wel():
    return render_template('welcome.html')

# Route to render the result page
@app.route('/result')
def result():
    # Logic for handling results goes here if needed
    return render_template('result.html')


# Route to render the resource page  
@app.route('/resource')
def res():
    return render_template('resource.html')


#handle resources in the backend 
@app.route('/resource', methods=['POST'])
def add_resource():
 if request.method == 'POST':  
    try:
        description = request.form['description']
        link = request.form['link']

        print(f"Received description: {description}")
        print(f"Received link: {link}")

       

        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        query = "INSERT INTO res (label, refer) VALUES (%s, %s)"
        cursor.execute(query, (description, link))
        db_connection.commit()
        cursor.close()
        db_connection.close()

        return jsonify({'message': 'Data inserted successfully'})
       

    except Exception as e:
        # Handle any potential exceptions or errors
        error_message = f"Error: {e}"
        return jsonify({'error': error_message})
 else:
      return render_template ('dashboard.html')
 
 #live poll code for insertion in database
@app.route('/livepoll')
def poll():
    # Logic for handling results goes here if needed
    return render_template('livepoll.html') 
@app.route('/tkypoll')
def tkypoll():
    # Logic for handling results goes here if needed
    return render_template('tkypoll.html') 



@app.route('/livepoll', methods=['POST'])
def poll_data():
            data = request.get_json()  # Get the JSON data sent from the frontend
    # Process the received data as needed (e.g., store it in a database)
            question_id = data.get('questionId')
            selected_option = data.get('selectedOption')

            # Print the received data for debugging purposes
            print(f"Received question ID: {question_id}")
            print(f"Received selected option: {selected_option}")

            # Establish a database connection
            db_connection = get_db_connection()
            cursor = db_connection.cursor()

            # Insert the received data into the 'poll' table
            query = "INSERT INTO poll (qid, optionsel) VALUES (%s, %s)"
            cursor.execute(query, (question_id, selected_option))

            # Commit changes and close the database connection
            db_connection.commit()
            cursor.close()
            db_connection.close()

            return jsonify({'message': 'Data inserted successfully'})

@app.route('/resultpoll')
def rpoll():
    # Logic for handling results goes here if needed
    return render_template('resultpoll.html') 
 
@app.route('/resultpoll', methods=['POST'])
def result_poll():
    try:
        data = request.json
        question_id = data.get('questionId')
        
        # Assuming the optionsel and count are the names of your columns in your poll table
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch data based on question ID from poll table
        cursor.execute("SELECT COUNT(optionsel) , optionsel FROM poll WHERE qid=%s GROUP BY optionsel ;", (question_id,))
        result = cursor.fetchall()
        print(result)

        # Ensure result is a list of tuples for JSON serializing
        result_json = [{'count': row[0], 'optionsel': row[1]} for row in result]

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return result as JSON
        return jsonify(result_json)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
       
       



    
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)