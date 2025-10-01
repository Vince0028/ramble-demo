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

    def create_tables_if_not_exist(self):
        """Create necessary tables if they don't exist"""
        if not self.is_connected():
            logger.warning("Database not connected. Cannot create tables.")
            return False
        
        try:
            # This would typically be done through Supabase dashboard or migrations
            # For now, we'll just log that tables should be created manually
            logger.info("Please create the 'users' table in your Supabase dashboard with the following schema:")
            logger.info("""
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
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
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
