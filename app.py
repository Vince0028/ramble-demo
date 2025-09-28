from flask import Flask, render_template, send_from_directory, request, redirect, session, jsonify, url_for
import requests
import os
from dotenv import load_dotenv
import json
import secrets

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))

# LinkedIn OAuth configuration
LINKEDIN_CLIENT_ID = os.environ.get('LINKEDIN_CLIENT_ID', '862mvp7e208g5z')
LINKEDIN_CLIENT_SECRET = os.environ.get('LINKEDIN_CLIENT_SECRET', 'WPL_AP1.DLvWnuIO53i8K8Gk.r22wZQ==')
LINKEDIN_REDIRECT_URI = os.environ.get('LINKEDIN_REDIRECT_URI', 'http://localhost:5000/auth/linkedin/callback')

# Serve files from existing Next.js public/ folder for convenience (images, placeholders)
@app.route('/public/<path:filename>')
def public_files(filename):
    return send_from_directory('public', filename)

# Maintain Next.js-style image path: /images/... maps to public/images
@app.route('/images/<path:filename>')
def public_images(filename):
    return send_from_directory('public/images', filename)


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/groups')
def groups():
    return render_template('groups.html')


@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


# LinkedIn OAuth routes
@app.route('/auth/linkedin')
def linkedin_login():
    """Initiate LinkedIn OAuth flow"""
    print(f"DEBUG: LINKEDIN_CLIENT_ID = {LINKEDIN_CLIENT_ID}")
    print(f"DEBUG: LINKEDIN_CLIENT_SECRET = {LINKEDIN_CLIENT_SECRET}")
    print(f"DEBUG: LINKEDIN_REDIRECT_URI = {LINKEDIN_REDIRECT_URI}")
    
    if not LINKEDIN_CLIENT_ID:
        return jsonify({'error': 'LinkedIn OAuth not configured'}), 500
    
    # Generate state parameter for security
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    # LinkedIn OAuth URL
    linkedin_auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&"
        f"client_id={LINKEDIN_CLIENT_ID}&"
        f"redirect_uri={LINKEDIN_REDIRECT_URI}&"
        f"state={state}&"
        f"scope=r_liteprofile%20r_emailaddress"
    )
    
    return redirect(linkedin_auth_url)


@app.route('/auth/linkedin/callback')
def linkedin_callback():
    """Handle LinkedIn OAuth callback"""
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    
    if error:
        return jsonify({'error': f'LinkedIn OAuth error: {error}'}), 400
    
    if not code:
        return jsonify({'error': 'No authorization code received'}), 400
    
    # Verify state parameter
    if state != session.get('oauth_state'):
        return jsonify({'error': 'Invalid state parameter'}), 400
    
    try:
        # Exchange code for access token
        token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': LINKEDIN_REDIRECT_URI,
            'client_id': LINKEDIN_CLIENT_ID,
            'client_secret': LINKEDIN_CLIENT_SECRET
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        token_info = token_response.json()
        access_token = token_info['access_token']
        
        # Get user profile information
        profile_url = 'https://api.linkedin.com/v2/people/~'
        headers = {'Authorization': f'Bearer {access_token}'}
        profile_response = requests.get(profile_url, headers=headers)
        profile_response.raise_for_status()
        profile_data = profile_response.json()
        
        # Get email address
        email_url = 'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))'
        email_response = requests.get(email_url, headers=headers)
        email_response.raise_for_status()
        email_data = email_response.json()
        
        # Extract user information
        first_name = profile_data.get('firstName', {}).get('localized', {}).get('en_US', '')
        last_name = profile_data.get('lastName', {}).get('localized', {}).get('en_US', '')
        full_name = f"{first_name} {last_name}".strip()
        
        email = ''
        if email_data.get('elements') and len(email_data['elements']) > 0:
            email = email_data['elements'][0]['handle~']['emailAddress']
        
        # Store user data in session
        user_data = {
            'name': full_name,
            'email': email,
            'linkedin_id': profile_data.get('id'),
            'points': 2690,  # Default points for new users
            'rank': 4,       # Default rank for new users
            'login_method': 'linkedin'
        }
        
        session['user'] = user_data
        
        # Redirect to dashboard
        return redirect('/dashboard')
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'LinkedIn API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@app.route('/auth/logout')
def logout():
    """Logout user"""
    session.pop('user', None)
    session.pop('oauth_state', None)
    return redirect('/')


@app.route('/api/user')
def get_user():
    """Get current user data"""
    user = session.get('user')
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'Not authenticated'}), 401


if __name__ == '__main__':
    # Get port from environment variable (for Render) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run with: py app.py
    app.run(host='0.0.0.0', port=port, debug=False)
