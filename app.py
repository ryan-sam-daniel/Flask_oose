from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    
    # Check if the login database exists
    if os.path.exists('login_database.xlsx'):
        df = pd.read_excel('login_database.xlsx')
    else:
        return render_template('login.html', error="Login database not found.")
    
    # Check if the user exists in the database
    if 'Email' in df.columns and 'Password' in df.columns:
        user = df[(df['Email'] == username) & (df['Password'] == password)]
        if not user.empty:
            return redirect(url_for('form'))
        else:
            return render_template('login.html', error="Invalid email or password.")
    else:
        return render_template('login.html', error="Login database structure is incorrect.")

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    
    # Check if the form database exists
    if os.path.exists('form_database.xlsx'):
        df = pd.read_excel('form_database.xlsx')
    else:
        df = pd.DataFrame(columns=['Name', 'Email', 'Password'])
    
    # Create a DataFrame for the new data
    new_data = pd.DataFrame({'Name': [name], 'Email': [email], 'Password': [password]})
    
    # Append the new data to the existing DataFrame
    df = pd.concat([df, new_data], ignore_index=True)
    
    # Save back to Excel
    df.to_excel('form_database.xlsx', index=False)
    
    return "Data saved successfully!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the login database exists
        if os.path.exists('login_database.xlsx'):
            df = pd.read_excel('login_database.xlsx')
        else:
            df = pd.DataFrame(columns=['Email', 'Password'])
        
        # Check if the email already exists in the database
        if email in df['Email'].values:
            return render_template('register.html', error="Email already registered.")
        
        # Create a DataFrame for the new user
        new_user = pd.DataFrame({'Email': [email], 'Password': [password]})
        
        # Append the new user to the existing DataFrame
        df = pd.concat([df, new_user], ignore_index=True)
        
        # Save back to Excel
        df.to_excel('login_database.xlsx', index=False)
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
