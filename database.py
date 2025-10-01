"""
Database utilities for Supabase integration
"""
import os
from supabase import create_client, Client
from typing import Optional, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase_url = os.environ.get('SUPABASE_URL')
        self.supabase_key = os.environ.get('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            logger.warning("Supabase credentials not found. Database operations will be disabled.")
            self.supabase: Optional[Client] = None
        else:
            try:
                # Try different initialization methods
                try:
                    self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
                except TypeError:
                    # Fallback for different client versions
                    self.supabase: Client = create_client(
                        supabase_url=self.supabase_url,
                        supabase_key=self.supabase_key
                    )
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                logger.error(f"URL: {self.supabase_url}")
                logger.error(f"Key: {self.supabase_key[:20]}...")
                self.supabase = None

    def is_connected(self) -> bool:
        """Check if database connection is available"""
        return self.supabase is not None

    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new user in the database"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot create user.")
            return None
        
        try:
            # Prepare user data for insertion
            db_user_data = {
                'email': user_data.get('email'),
                'first_name': user_data.get('firstName', ''),
                'middle_name': user_data.get('middleName', ''),
                'surname': user_data.get('surname', ''),
                'birthday': user_data.get('birthday'),
                'gender': user_data.get('gender'),
                'password': user_data.get('password'),
                'points': user_data.get('points', 0),
                'rank': user_data.get('rank', 1),
                'login_method': user_data.get('login_method', 'email'),
                'linkedin_id': user_data.get('linkedin_id')
            }
            
            # Remove None values
            db_user_data = {k: v for k, v in db_user_data.items() if v is not None}
            
            result = self.supabase.table('users').insert(db_user_data).execute()
            
            if result.data:
                logger.info(f"User created successfully: {user_data.get('email')}")
                return result.data[0]
            else:
                logger.error("Failed to create user: No data returned")
                return None
                
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email address"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot get user.")
            return None
        
        try:
            result = self.supabase.table('users').select('*').eq('email', email).execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None

    def get_user_by_linkedin_id(self, linkedin_id: str) -> Optional[Dict[str, Any]]:
        """Get user by LinkedIn ID"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot get user.")
            return None
        
        try:
            result = self.supabase.table('users').select('*').eq('linkedin_id', linkedin_id).execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting user by LinkedIn ID: {e}")
            return None

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot authenticate user.")
            return None
        
        try:
            result = self.supabase.table('users').select('*').eq('email', email).eq('password', password).execute()
            
            if result.data and len(result.data) > 0:
                logger.info(f"User authenticated successfully: {email}")
                return result.data[0]
            else:
                logger.warning(f"Authentication failed for email: {email}")
                return None
                
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None

    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user data"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot update user.")
            return None
        
        try:
            result = self.supabase.table('users').update(update_data).eq('id', user_id).execute()
            
            if result.data:
                logger.info(f"User updated successfully: {user_id}")
                return result.data[0]
            else:
                logger.error("Failed to update user: No data returned")
                return None
                
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return None

    # Chat-related methods
    def get_all_users(self, exclude_user_id: str = None) -> list:
        """Get all users for user discovery"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot get users.")
            return []
        
        try:
            query = self.supabase.table('users').select('id, first_name, surname, email, profile_picture_url, is_online, last_seen, login_method, linkedin_id')
            if exclude_user_id:
                query = query.neq('id', exclude_user_id)
            
            result = query.execute()
            return result.data if result.data else []
                
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            return []

    def create_group(self, group_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new group"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot create group.")
            return None
        
        try:
            result = self.supabase.table('groups').insert(group_data).execute()
            
            if result.data:
                logger.info(f"Group created successfully: {group_data.get('name')}")
                return result.data[0]
            else:
                logger.error("Failed to create group: No data returned")
                return None
                
        except Exception as e:
            logger.error(f"Error creating group: {e}")
            return None

    def add_group_member(self, group_id: str, user_id: str, role: str = 'member') -> bool:
        """Add a user to a group"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot add group member.")
            return False
        
        try:
            member_data = {
                'group_id': group_id,
                'user_id': user_id,
                'role': role
            }
            
            result = self.supabase.table('group_members').insert(member_data).execute()
            
            if result.data:
                logger.info(f"User {user_id} added to group {group_id}")
                return True
            else:
                logger.error("Failed to add group member: No data returned")
                return False
                
        except Exception as e:
            logger.error(f"Error adding group member: {e}")
            return False

    def get_user_groups(self, user_id: str) -> list:
        """Get all groups a user belongs to"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot get user groups.")
            return []
        
        try:
            result = self.supabase.table('group_members').select('''
                group_id,
                groups!inner(id, name, description, created_by, is_private, created_at)
            ''').eq('user_id', user_id).execute()
            
            return result.data if result.data else []
                
        except Exception as e:
            logger.error(f"Error getting user groups: {e}")
            return []

    def get_group_members(self, group_id: str) -> list:
        """Get all members of a group"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot get group members.")
            return []
        
        try:
            result = self.supabase.table('group_members').select('''
                user_id,
                role,
                joined_at,
                users!inner(id, first_name, surname, email, profile_picture_url, is_online, last_seen)
            ''').eq('group_id', group_id).execute()
            
            return result.data if result.data else []
                
        except Exception as e:
            logger.error(f"Error getting group members: {e}")
            return []

    def send_message(self, message_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send a message (private or group)"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot send message.")
            return None
        
        try:
            result = self.supabase.table('messages').insert(message_data).execute()
            
            if result.data:
                logger.info(f"Message sent successfully")
                return result.data[0]
            else:
                logger.error("Failed to send message: No data returned")
                return None
                
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return None

    def get_messages(self, group_id: str = None, recipient_id: str = None, limit: int = 50) -> list:
        """Get messages for a group or private conversation"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot get messages.")
            return []
        
        try:
            query = self.supabase.table('messages').select('''
                id,
                content,
                message_type,
                is_read,
                created_at,
                sender_id,
                users!inner(id, first_name, surname, profile_picture_url)
            ''').order('created_at', desc=True).limit(limit)
            
            if group_id:
                query = query.eq('group_id', group_id)
            elif recipient_id:
                query = query.eq('recipient_id', recipient_id)
            
            result = query.execute()
            return result.data if result.data else []
                
        except Exception as e:
            logger.error(f"Error getting messages: {e}")
            return []

    def create_group_invitation(self, invitation_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a group invitation"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot create invitation.")
            return None
        
        try:
            result = self.supabase.table('group_invitations').insert(invitation_data).execute()
            
            if result.data:
                logger.info(f"Group invitation created successfully")
                return result.data[0]
            else:
                logger.error("Failed to create invitation: No data returned")
                return None
                
        except Exception as e:
            logger.error(f"Error creating invitation: {e}")
            return None

    def get_user_invitations(self, user_id: str) -> list:
        """Get pending invitations for a user"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot get invitations.")
            return []
        
        try:
            result = self.supabase.table('group_invitations').select('''
                id,
                group_id,
                invited_by,
                status,
                created_at,
                groups!inner(id, name, description),
                users!inner(id, first_name, surname)
            ''').eq('invited_user_id', user_id).eq('status', 'pending').execute()
            
            return result.data if result.data else []
                
        except Exception as e:
            logger.error(f"Error getting invitations: {e}")
            return []

    def respond_to_invitation(self, invitation_id: str, status: str) -> bool:
        """Respond to a group invitation"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot respond to invitation.")
            return False
        
        try:
            update_data = {
                'status': status,
                'responded_at': 'now()'
            }
            
            result = self.supabase.table('group_invitations').update(update_data).eq('id', invitation_id).execute()
            
            if result.data:
                logger.info(f"Invitation {invitation_id} {status}")
                return True
            else:
                logger.error("Failed to respond to invitation: No data returned")
                return False
                
        except Exception as e:
            logger.error(f"Error responding to invitation: {e}")
            return False

    def update_user_online_status(self, user_id: str, is_online: bool) -> bool:
        """Update user's online status"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot update online status.")
            return False
        
        try:
            update_data = {
                'is_online': is_online,
                'last_seen': 'now()'
            }
            
            result = self.supabase.table('users').update(update_data).eq('id', user_id).execute()
            
            if result.data:
                logger.info(f"User {user_id} online status updated to {is_online}")
                return True
            else:
                logger.error("Failed to update online status: No data returned")
                return False
                
        except Exception as e:
            logger.error(f"Error updating online status: {e}")
            return False

    def create_tables_if_not_exist(self):
        """Create necessary tables if they don't exist"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot create tables.")
            return False
        
        try:
            # This would typically be done through Supabase dashboard or migrations
            # For now, we'll just log that tables should be created manually
            logger.info("Please create the following tables in your Supabase dashboard:")
            logger.info("""
            -- Users table
            CREATE TABLE users (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                first_name VARCHAR(100),
                middle_name VARCHAR(100),
                surname VARCHAR(100),
                birthday DATE,
                gender VARCHAR(50),
                password VARCHAR(255),
                points INTEGER DEFAULT 0,
                rank INTEGER DEFAULT 1,
                login_method VARCHAR(50) DEFAULT 'email',
                linkedin_id VARCHAR(255) UNIQUE,
                profile_picture_url TEXT,
                is_online BOOLEAN DEFAULT FALSE,
                last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );

            -- Groups table
            CREATE TABLE groups (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                created_by UUID REFERENCES users(id) ON DELETE CASCADE,
                is_private BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );

            -- Group members table
            CREATE TABLE group_members (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                role VARCHAR(50) DEFAULT 'member', -- 'admin', 'member'
                joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(group_id, user_id)
            );

            -- Messages table
            CREATE TABLE messages (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                sender_id UUID REFERENCES users(id) ON DELETE CASCADE,
                group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
                recipient_id UUID REFERENCES users(id) ON DELETE CASCADE, -- For private messages
                content TEXT NOT NULL,
                message_type VARCHAR(50) DEFAULT 'text', -- 'text', 'image', 'file'
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );

            -- Group invitations table
            CREATE TABLE group_invitations (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
                invited_by UUID REFERENCES users(id) ON DELETE CASCADE,
                invited_user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'accepted', 'declined'
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                responded_at TIMESTAMP WITH TIME ZONE
            );

            -- Create indexes for better performance
            CREATE INDEX idx_messages_group_id ON messages(group_id);
            CREATE INDEX idx_messages_sender_id ON messages(sender_id);
            CREATE INDEX idx_messages_recipient_id ON messages(recipient_id);
            CREATE INDEX idx_messages_created_at ON messages(created_at);
            CREATE INDEX idx_group_members_group_id ON group_members(group_id);
            CREATE INDEX idx_group_members_user_id ON group_members(user_id);
            CREATE INDEX idx_group_invitations_group_id ON group_invitations(group_id);
            CREATE INDEX idx_group_invitations_invited_user_id ON group_invitations(invited_user_id);
            """)
            return True
            
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            return False

# Global database manager instance - will be initialized after environment is loaded
db_manager = None

def get_db_manager():
    """Get database manager instance, initializing if needed"""
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager
