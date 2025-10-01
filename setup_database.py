"""
Setup script for Supabase database
This script helps you set up the database table
"""
import os
from dotenv import load_dotenv
from database import db_manager

def main():
    """Main setup function"""
    print("RAMBLE Demo - Database Setup")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if Supabase credentials are configured
    if not os.environ.get('SUPABASE_URL') or not os.environ.get('SUPABASE_KEY'):
        print("Supabase credentials not found!")
        print("\nPlease follow these steps:")
        print("1. Make sure your .env file contains:")
        print("   SUPABASE_URL=https://vstdajngvqntisjituoo.supabase.co")
        print("   SUPABASE_KEY=your-supabase-anon-key")
        print("2. Run this script again")
        return
    
    print("Supabase credentials found")
    print(f"URL: {os.environ.get('SUPABASE_URL')}")
    print(f"Key: {os.environ.get('SUPABASE_KEY')[:20]}...")
    
    # Reinitialize database manager with loaded environment
    from database import DatabaseManager
    db_manager = DatabaseManager()
    
    # Test database connection
    if db_manager.is_connected():
        print("Database connection successful")
        
        # Create tables
        print("Creating database tables...")
        db_manager.create_tables_if_not_exist()
        
        print("\nDatabase setup complete!")
        print("\nNext steps:")
        print("1. Go to your Supabase dashboard: https://supabase.com/dashboard/project/vstdajngvqntisjituoo")
        print("2. Navigate to Table Editor")
        print("3. Create the 'users' table with the schema provided above")
        print("4. Run: pip install -r requirement.txt")
        print("5. Run: python app.py")
        
    else:
        print("Database connection failed")
        print("Please check your Supabase credentials and try again")

if __name__ == "__main__":
    main()
