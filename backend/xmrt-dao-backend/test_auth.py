import sys
import os
import json
from src.main import app, db

# Removed pytest dependency for standalone execution

if __name__ == "__main__":
    # fast and dirty manual run
    try:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        client = app.test_client()
        with app.app_context():
            db.create_all()
            
        print("Testing Register...")
        resp = client.post('/api/users/register', json={
            'username': 'manualtest', 
            'email': 'manual@test.com', 
            'password': 'pass'
        })
        print(f"Register status: {resp.status_code}")
        if resp.status_code != 201:
            print(resp.get_json())
            
        print("Testing Login...")
        resp = client.post('/api/users/login', json={
            'email': 'manual@test.com', 
            'password': 'pass'
        })
        print(f"Login status: {resp.status_code}")
        
        login_data = resp.get_json()
        if login_data.get('success'):
             print("Login successful!")
        else:
             print("Login failed!")

        print("Done.")
    except Exception as e:
        print(e)
