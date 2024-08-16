import pytest
import os
import hashlib
from flask import Flask
from app import app, generate_checksum, verify_checksum, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page."""
    client.post('/login', data=dict(
        username='admin',
        password='password'
    ), follow_redirects=True)
    response = client.get('/')
    assert response.status_code == 200
    assert b"Upload and Predict" in response.data

def test_login_page(client):
    """Test the login page."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_login(client):
    """Test the login functionality."""
    response = client.post('/login', data=dict(
        username='admin',
        password='password'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"Upload and Predict" in response.data

def test_invalid_login(client):
    """Test invalid login."""
    response = client.post('/login', data=dict(
        username='wrong',
        password='wrong'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid credentials" in response.data

def test_logout(client):
    """Test the logout functionality."""
    client.post('/login', data=dict(
        username='admin',
        password='password'
    ), follow_redirects=True)
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data

def test_generate_checksum():
    """Test the generate_checksum function."""
    file_path = 'test_file.txt'
    with open(file_path, 'w') as f:
        f.write('test content')
    checksum = generate_checksum(file_path)
    assert checksum == hashlib.sha256(b'test content').hexdigest()
    os.remove(file_path)

def test_verify_checksum():
    """Test the verify_checksum function."""
    file_path = 'test_file.txt'
    checksum_path = 'test_checksum.txt'
    with open(file_path, 'w') as f:
        f.write('test content')
    with open(checksum_path, 'w') as f:
        f.write(hashlib.sha256(b'test content').hexdigest())
    verify_checksum(file_path, checksum_path)
    os.remove(file_path)
    os.remove(checksum_path)
