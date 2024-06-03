# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 16:34:03 2024

@author: moni
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'Python'

pets = {
    'cats': [
        {'name': 'Whiskers', 'breed': 'Persian', 'age': 3, 'photo': 'cat1.jpg', 'location': 'Mumbai'},
        {'name': 'Mittens', 'breed': 'Siamese', 'age': 2, 'photo': 'cat2.jpg', 'location': 'Delhi'},
        {'name': 'Snowball', 'breed': 'Maine Coon', 'age': 4, 'photo': 'cat3.jpg', 'location': 'Bangalore'},
        {'name': 'Fluffy', 'breed': 'Ragdoll', 'age': 5, 'photo': 'cat4.jpg', 'location': 'Hyderabad'},
        {'name': 'Oreo', 'breed': 'Tuxedo', 'age': 2, 'photo': 'cat5.jpg', 'location': 'Chennai'},
        {'name': 'Simba', 'breed': 'Bengal', 'age': 3, 'photo': 'cat6.jpg', 'location': 'Kolkata'},
        {'name': 'Luna', 'breed': 'Scottish Fold', 'age': 1, 'photo': 'cat7.jpg', 'location': 'Pune'},
        {'name': 'Ginger', 'breed': 'Tabby', 'age': 4, 'photo': 'cat8.jpg', 'location': 'Ahmedabad'},
        {'name': 'Smokey', 'breed': 'British Shorthair', 'age': 2, 'photo': 'cat9.jpg', 'location': 'Surat'},
        {'name': 'Shadow', 'breed': 'Russian Blue', 'age': 3, 'photo': 'cat10.jpg', 'location': 'Jaipur'}
    ],
    'dogs': [
        {'name': 'Buddy', 'breed': 'Golden Retriever', 'age': 4, 'photo': 'dog1.jpg', 'location': 'Mumbai'},
        {'name': 'Max', 'breed': 'Labrador', 'age': 5, 'photo': 'dog2.jpg', 'location': 'Delhi'},
        {'name': 'Rocky', 'breed': 'German Shepherd', 'age': 3, 'photo': 'dog3.jpg', 'location': 'Bangalore'},
        {'name': 'Bailey', 'breed': 'Beagle', 'age': 2, 'photo': 'dog4.jpg', 'location': 'Hyderabad'},
        {'name': 'Charlie', 'breed': 'Poodle', 'age': 3, 'photo': 'dog5.jpg', 'location': 'Chennai'},
        {'name': 'Daisy', 'breed': 'Dachshund', 'age': 4, 'photo': 'dog6.jpg', 'location': 'Kolkata'},
        {'name': 'Bella', 'breed': 'Boxer', 'age': 1, 'photo': 'dog7.jpg', 'location': 'Pune'},
        {'name': 'Cooper', 'breed': 'Siberian Husky', 'age': 2, 'photo': 'dog8.jpg', 'location': 'Ahmedabad'},
        {'name': 'Lucy', 'breed': 'Border Collie', 'age': 5, 'photo': 'dog9.jpg', 'location': 'Surat'},
        {'name': 'Harley', 'breed': 'Shih Tzu', 'age': 6, 'photo': 'dog10.jpg', 'location': 'Jaipur'}
    ],
    'birds': [
        {'name': 'Tweetie', 'breed': 'Parrot', 'age': 1, 'photo': 'bird1.jpg', 'location': 'Mumbai'},
        {'name': 'Chirpy', 'breed': 'Canary', 'age': 2, 'photo': 'bird2.jpg', 'location': 'Delhi'},
        {'name': 'Polly', 'breed': 'Cockatiel', 'age': 3, 'photo': 'bird3.jpg', 'location': 'Bangalore'},
        {'name': 'Kiwi', 'breed': 'Lovebird', 'age': 2, 'photo': 'bird4.jpg', 'location': 'Hyderabad'},
        {'name': 'Sunny', 'breed': 'Finch', 'age': 1, 'photo': 'bird5.jpg', 'location': 'Chennai'},
        {'name': 'Coco', 'breed': 'Cockatoo', 'age': 4, 'photo': 'bird6.jpg', 'location': 'Kolkata'},
        {'name': 'Pepper', 'breed': 'Budgerigar', 'age': 3, 'photo': 'bird7.jpg', 'location': 'Pune'},
        {'name': 'Rio', 'breed': 'Macaw', 'age': 5, 'photo': 'bird8.jpg', 'location': 'Ahmedabad'},
        {'name': 'Blue', 'breed': 'Blue Jay', 'age': 2, 'photo': 'bird9.jpg', 'location': 'Surat'},
        {'name': 'Sky', 'breed': 'Parakeet', 'age': 1, 'photo': 'bird10.jpg', 'location': 'Jaipur'}
    ],
    'hamsters': [
       {'name': 'Chinese hamster', 'breed': 'Chinese', 'age': 1, 'photo': 'hamster1.jpg', 'location': 'Mumbai'},
       {'name': 'Syrian hamster', 'breed': 'Syrian', 'age': 2, 'photo': 'hamster2.jpg', 'location': 'Delhi'},
       {'name': 'Roborovski dwarf hamster', 'breed': 'Roborovski', 'age': 3, 'photo': 'hamster3.jpg', 'location': 'Bangalore'},
       {'name': 'Djungarian hamster', 'breed': 'Djungarian', 'age': 2, 'photo': 'hamster4.jpg', 'location': 'Hyderabad'},
       {'name': 'Campbell\'s dwarf hamster', 'breed': 'Campbell\'s', 'age': 1, 'photo': 'hamster5.jpg', 'location': 'Chennai'},
       {'name': 'Romanian hamster', 'breed': 'Romanian', 'age': 4, 'photo': 'hamster6.jpg', 'location': 'Kolkata'},
       {'name': 'Ciscaucasian hamster', 'breed': 'Ciscaucasian', 'age': 3, 'photo': 'hamster7.jpg', 'location': 'Pune'},
       {'name': 'Desert hamster', 'breed': 'Desert', 'age': 5, 'photo': 'hamster8.jpg', 'location': 'Ahmedabad'},
       {'name': 'Winter white dwarf hamster', 'breed': 'Winter White', 'age': 2, 'photo': 'hamster9.jpg', 'location': 'Surat'},
       {'name': 'Tibetan dwarf hamster', 'breed': 'Tibetan', 'age': 1, 'photo': 'hamster10.jpg', 'location': 'Jaipur'}
   ],
}

# Database setup (only if it's not already set up)
def setup_database():
    try:
        conn = sqlite3.connect('pets.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS cats
                     (id INTEGER PRIMARY KEY, name TEXT, breed TEXT, age INTEGER, photo TEXT, location TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS dogs
                     (id INTEGER PRIMARY KEY, name TEXT, breed TEXT, age INTEGER, photo TEXT, location TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS birds
                     (id INTEGER PRIMARY KEY, name TEXT, breed TEXT, age INTEGER, photo TEXT, location TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS hamsters
                     (id INTEGER PRIMARY KEY, name TEXT, breed TEXT, age INTEGER, photo TEXT, location TEXT)''')

        for category, category_pets in pets.items():
            for pet in category_pets:
                c.execute(f"INSERT INTO {category} (name, breed, age, photo, location) VALUES (?, ?, ?, ?, ?)",
                          (pet['name'], pet['breed'], pet['age'], pet['photo'], pet['location']))

        # Commit changes and close connection
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Error while setting up database:", e)

setup_database()

@app.route('/')
def home1():
    return render_template('hom.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/adopt', methods=['POST'])
def adopt():
    pet_type = request.form['pet_type']

    if pet_type in pets:
        return render_template('pet_table.html', pets=pets[pet_type], pet_type=pet_type)
    else:
        flash('Error: Pet type not found.')
        return redirect(url_for('home'))

@app.route('/adopt_pet', methods=['POST'])
def adopt_pet():
    pet_name = request.form['pet_name']
    pet_breed = request.form['pet_breed']
    pet_age = request.form['pet_age']

    print(f"Adoption request received for {pet_name} ({pet_breed}), {pet_age} years old.")
    return {'message': f'Adoption request received for {pet_name} ({pet_breed}), {pet_age} years old.'}

@app.route('/signup_submit', methods=['POST'])
def signup_submit():
    email = request.form['email']
    password = request.form['password']

    print(f"New user signed up with email: {email} and password: {password}")

    flash('Signup successful! Please login.')
    return redirect(url_for('login'))

@app.route('/login_submit', methods=['POST'])
def login_submit():
    email = request.form['email']
    password1 = request.form['password']

    if email == 'example@example.com' and password1 == 'password':
        session['email'] = email
        flash('Login successful!')
        return redirect(url_for('home'))
    else:
        if password1 != 'password':
            flash('Incorrect password. Please try again.')
        return redirect(url_for('login'))

@app.route('/seller')
def seller():
    return render_template('home-seller.html')

@app.route('/submit_pet', methods=['POST'])
def submit_pet():
    data = request.get_json()
    pet_type = data['pet_type']
    pet_name = data['pet_name']
    pet_age = data['pet_age']
    pet_location = data['pet_location']
    pet_license = data['pet_license']

    print(f"New pet listed: {pet_name}, a {pet_age}-year-old {pet_type} located in {pet_location}, {pet_license}")

    return jsonify({'message': f'Pet {pet_name} has been listed for adoption!'})

if __name__ == '__main__':
    app.run(debug=True)
