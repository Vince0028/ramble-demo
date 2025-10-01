from flask import Flask, render_template, send_from_directory, request, redirect, session, jsonify, url_for
import requests
import os
from dotenv import load_dotenv
import json
import secrets
from database import get_db_manager

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

# Fallback route for missing images
@app.route('/public/placeholder-logo.png')
def placeholder_logo():
    return send_from_directory('public', 'placeholder-logo.png')


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


@app.route('/chat')
def chat():
    return render_template('chat.html')


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
        profile_url = 'https://api.linkedin.com/v2/people/~:(id,firstName,lastName,profilePicture(displayImage~:playableStreams))'
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
        
        # Get profile picture URL
        profile_picture_url = ''
        if 'profilePicture' in profile_data and 'displayImage~' in profile_data['profilePicture']:
            elements = profile_data['profilePicture']['displayImage~'].get('elements', [])
            if elements and len(elements) > 0:
                profile_picture_url = elements[0].get('identifiers', [{}])[0].get('identifier', '')
        
        # Check if user exists in database
        db_manager = get_db_manager()
        existing_user = db_manager.get_user_by_linkedin_id(profile_data.get('id'))
        
        if existing_user:
            # Update existing user
            user_data = {
                'name': full_name,
                'email': email,
                'linkedin_id': profile_data.get('id'),
                'profile_picture_url': profile_picture_url,
                'points': existing_user.get('points', 2690),
                'rank': existing_user.get('rank', 4),
                'login_method': 'linkedin',
                'db_user': existing_user
            }
        else:
            # Create new user in database
            new_user_data = {
                'email': email,
                'firstName': first_name,
                'surname': last_name,
                'profile_picture_url': profile_picture_url,
                'points': 2690,
                'rank': 4,
                'login_method': 'linkedin',
                'linkedin_id': profile_data.get('id')
            }
            
            db_user = db_manager.create_user(new_user_data)
            
            user_data = {
                'name': full_name,
                'email': email,
                'linkedin_id': profile_data.get('id'),
                'profile_picture_url': profile_picture_url,
                'points': 2690,
                'rank': 4,
                'login_method': 'linkedin',
                'db_user': db_user
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


@app.route('/api/login', methods=['POST'])
def login():
    """Handle user login"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Authenticate user
        db_manager = get_db_manager()
        user = db_manager.authenticate_user(data['email'], data['password'])
        
        if user:
            # Store in session
            session['user'] = {
                'name': f"{user.get('first_name', '')} {user.get('surname', '')}".strip(),
                'email': user.get('email'),
                'points': user.get('points', 2690),
                'rank': user.get('rank', 4),
                'login_method': 'email',
                'db_user': user
            }
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': session['user']
            })
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
            
    except Exception as e:
        return jsonify({'error': f'Login error: {str(e)}'}), 500

@app.route('/api/signup', methods=['POST'])
def signup():
    """Handle user signup"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstName', 'surname', 'email', 'password', 'birthday', 'gender']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        db_manager = get_db_manager()
        existing_user = db_manager.get_user_by_email(data['email'])
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409
        
        # Create new user
        user_data = {
            'email': data['email'],
            'firstName': data['firstName'],
            'middleName': data.get('middleName', ''),
            'surname': data['surname'],
            'birthday': data['birthday'],
            'gender': data['gender'],
            'password': data['password'],
            'points': 2690,
            'rank': 4,
            'login_method': 'email'
        }
        
        db_user = db_manager.create_user(user_data)
        
        if db_user:
            # Store in session
            session['user'] = {
                'name': f"{data['firstName']} {data['surname']}",
                'email': data['email'],
                'points': 2690,
                'rank': 4,
                'login_method': 'email',
                'db_user': db_user
            }
            
            return jsonify({
                'success': True,
                'message': 'User created successfully',
                'user': session['user']
            })
        else:
            return jsonify({'error': 'Failed to create user'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Signup error: {str(e)}'}), 500

@app.route('/api/user')
def get_user():
    """Get current user data"""
    user = session.get('user')
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'Not authenticated'}), 401

# Chat API endpoints
@app.route('/api/chat/users')
def get_chat_users():
    """Get all users for chat/discovery"""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        db_manager = get_db_manager()
        users = db_manager.get_all_users(exclude_user_id=user['db_user']['id'])
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': f'Failed to get users: {str(e)}'}), 500

@app.route('/api/chat/groups', methods=['GET'])
def get_user_groups():
    """Get user's groups"""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        db_manager = get_db_manager()
        groups = db_manager.get_user_groups(user['db_user']['id'])
        return jsonify(groups)
    except Exception as e:
        return jsonify({'error': f'Failed to get groups: {str(e)}'}), 500

@app.route('/api/chat/groups', methods=['POST'])
def create_group():
    """Create a new group"""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Group name is required'}), 400
        
        group_data = {
            'name': data['name'],
            'description': data.get('description', ''),
            'created_by': user['db_user']['id'],
            'is_private': data.get('is_private', False)
        }
        
        db_manager = get_db_manager()
        group = db_manager.create_group(group_data)
        
        if group:
            # Add creator as admin
            db_manager.add_group_member(group['id'], user['db_user']['id'], 'admin')
            return jsonify(group)
        else:
            return jsonify({'error': 'Failed to create group'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Failed to create group: {str(e)}'}), 500

@app.route('/api/chat/groups/<group_id>/members')
def get_group_members(group_id):
    """Get group members"""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        db_manager = get_db_manager()
        members = db_manager.get_group_members(group_id)
        return jsonify(members)
    except Exception as e:
        return jsonify({'error': f'Failed to get group members: {str(e)}'}), 500

@app.route('/api/chat/groups/<group_id>/invite', methods=['POST'])
def invite_to_group(group_id):
    """Invite user to group"""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        invited_user_id = data.get('user_id')
        
        if not invited_user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        invitation_data = {
            'group_id': group_id,
            'invited_by': user['db_user']['id'],
            'invited_user_id': invited_user_id
        }
        
        db_manager = get_db_manager()
        invitation = db_manager.create_group_invitation(invitation_data)
        
        if invitation:
            return jsonify(invitation)
        else:
            return jsonify({'error': 'Failed to create invitation'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Failed to invite user: {str(e)}'}), 500

@app.route('/api/chat/invitations')
def get_user_invitations():
    """Get user's pending invitations"""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        db_manager = get_db_manager()
        invitations = db_manager.get_user_invitations(user['db_user']['id'])
        return jsonify(invitations)
    except Exception as e:
        return jsonify({'error': f'Failed to get invitations: {str(e)}'}), 500

@app.route('/api/chat/invitations/<invitation_id>/respond', methods=['POST'])
def respond_to_invitation(invitation_id):
    """Respond to group invitation"""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        status = data.get('status')  # 'accepted' or 'declined'
        
        if status not in ['accepted', 'declined']:
            return jsonify({'error': 'Status must be accepted or declined'}), 400
        
        db_manager = get_db_manager()
        success = db_manager.respond_to_invitation(invitation_id, status)
        
        if success and status == 'accepted':
            # Add user to group
            # First get the invitation to find group_id
            invitations = db_manager.get_user_invitations(user['db_user']['id'])
            invitation = next((inv for inv in invitations if inv['id'] == invitation_id), None)
            
            if invitation:
                db_manager.add_group_member(invitation['group_id'], user['db_user']['id'])
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to respond to invitation'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Failed to respond to invitation: {str(e)}'}), 500

@app.route('/api/chat/messages', methods=['POST'])
def send_message():
    """Send a message"""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        
        if not data.get('content'):
            return jsonify({'error': 'Message content is required'}), 400
        
        message_data = {
            'sender_id': user['db_user']['id'],
            'content': data['content'],
            'message_type': data.get('message_type', 'text')
        }
        
        # Add group_id or recipient_id based on message type
        if data.get('group_id'):
            message_data['group_id'] = data['group_id']
        elif data.get('recipient_id'):
            message_data['recipient_id'] = data['recipient_id']
        else:
            return jsonify({'error': 'Either group_id or recipient_id is required'}), 400
        
        db_manager = get_db_manager()
        message = db_manager.send_message(message_data)
        
        if message:
            return jsonify(message)
        else:
            return jsonify({'error': 'Failed to send message'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Failed to send message: {str(e)}'}), 500

@app.route('/api/chat/messages')
def get_messages():
    """Get messages for a conversation"""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        group_id = request.args.get('group_id')
        recipient_id = request.args.get('recipient_id')
        limit = int(request.args.get('limit', 50))
        
        if not group_id and not recipient_id:
            return jsonify({'error': 'Either group_id or recipient_id is required'}), 400
        
        db_manager = get_db_manager()
        messages = db_manager.get_messages(group_id=group_id, recipient_id=recipient_id, limit=limit)
        return jsonify(messages)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get messages: {str(e)}'}), 500

@app.route('/api/chat/online-status', methods=['POST'])
def update_online_status():
    """Update user's online status"""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        is_online = data.get('is_online', True)
        
        db_manager = get_db_manager()
        success = db_manager.update_user_online_status(user['db_user']['id'], is_online)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to update online status'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Failed to update online status: {str(e)}'}), 500


if __name__ == '__main__':
    # Get port from environment variable (for Render) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run with: py app.py
    app.run(host='0.0.0.0', port=port, debug=True)
else:
    # This is for production deployment with Gunicorn
    pass
