#!/usr/bin/env python3
"""
LSMAC Data Migration Tool
Migrates data from the original SQLite database to Chromebook-compatible JSON format.
"""

import sqlite3
import json
import os
from datetime import datetime

def migrate_database_to_json(db_path, output_path):
    """
    Migrate data from SQLite database to JSON format for Chromebook version.
    
    Args:
        db_path (str): Path to the SQLite database file
        output_path (str): Path to output JSON file
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all members
        cursor.execute("SELECT * FROM members")
        members_data = cursor.fetchall()
        
        # Get column names
        cursor.execute("PRAGMA table_info(members)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Convert to dictionary format
        members = {}
        for row in members_data:
            member_dict = dict(zip(columns, row))
            member_id = member_dict.get('id', member_dict.get('member_id', ''))
            members[member_id] = {
                'id': member_id,
                'name': member_dict.get('name', ''),
                'email': member_dict.get('email', ''),
                'phone': member_dict.get('phone', ''),
                'memberSince': member_dict.get('member_since', member_dict.get('join_date', ''))
            }
        
        # Get check-in history
        cursor.execute("SELECT * FROM checkins")
        checkins_data = cursor.fetchall()
        
        # Get checkins column names
        cursor.execute("PRAGMA table_info(checkins)")
        checkin_columns = [column[1] for column in cursor.fetchall()]
        
        # Convert check-ins to the format expected by the web version
        checkin_history = {}
        for row in checkins_data:
            checkin_dict = dict(zip(checkin_columns, row))
            member_id = checkin_dict.get('member_id', '')
            checkin_date = checkin_dict.get('checkin_date', '')
            
            if member_id and checkin_date:
                if member_id not in checkin_history:
                    checkin_history[member_id] = []
                checkin_history[member_id].append(checkin_date)
        
        # Create the export data structure
        export_data = {
            'members': members,
            'history': checkin_history,
            'migration_date': datetime.now().isoformat(),
            'source_database': db_path
        }
        
        # Write to JSON file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"Migration completed successfully!")
        print(f"Members migrated: {len(members)}")
        print(f"Check-in records migrated: {sum(len(dates) for dates in checkin_history.values())}")
        print(f"Output file: {output_path}")
        
        # Also create a Chromebook-ready import file
        chromebook_data = {
            'members': members,
            'history': checkin_history
        }
        
        chromebook_path = output_path.replace('.json', '_chromebook.json')
        with open(chromebook_path, 'w', encoding='utf-8') as f:
            json.dump(chromebook_data, f, indent=2, ensure_ascii=False)
        
        print(f"Chromebook import file: {chromebook_path}")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error during migration: {e}")
        return False

def create_sample_data(output_path):
    """
    Create sample data for testing the Chromebook version.
    
    Args:
        output_path (str): Path to output JSON file
    """
    sample_data = {
        'members': {
            'M001': {
                'id': 'M001',
                'name': 'John Smith',
                'email': 'john.smith@email.com',
                'phone': '(555) 123-4567',
                'memberSince': '2023-01-15'
            },
            'M002': {
                'id': 'M002',
                'name': 'Jane Doe',
                'email': 'jane.doe@email.com',
                'phone': '(555) 234-5678',
                'memberSince': '2023-02-20'
            },
            'M003': {
                'id': 'M003',
                'name': 'Bob Johnson',
                'email': 'bob.johnson@email.com',
                'phone': '(555) 345-6789',
                'memberSince': '2023-03-10'
            },
            'M004': {
                'id': 'M004',
                'name': 'Alice Brown',
                'email': 'alice.brown@email.com',
                'phone': '(555) 456-7890',
                'memberSince': '2023-04-05'
            },
            'M005': {
                'id': 'M005',
                'name': 'Charlie Wilson',
                'email': 'charlie.wilson@email.com',
                'phone': '(555) 567-8901',
                'memberSince': '2023-05-12'
            }
        },
        'history': {
            'M001': ['2024-01-15', '2024-01-16'],
            'M002': ['2024-01-15'],
            'M003': ['2024-01-16']
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    print(f"Sample data created: {output_path}")

def main():
    """Main function to handle migration."""
    print("LSMAC Data Migration Tool")
    print("=" * 40)
    print()
    
    # Check for existing database files
    db_files = ['checkin_system.db', 'test_checkin_system.db']
    found_db = None
    
    for db_file in db_files:
        if os.path.exists(db_file):
            found_db = db_file
            break
    
    if found_db:
        print(f"Found database: {found_db}")
        choice = input("Do you want to migrate this database to JSON format? (y/n): ").lower()
        
        if choice == 'y':
            output_file = f"migrated_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            if migrate_database_to_json(found_db, output_file):
                print("\nMigration successful! You can now:")
                print("1. Copy the JSON file to your Chromebook")
                print("2. Open chromebook_checkin.html in Chrome")
                print("3. Import the data manually if needed")
            else:
                print("Migration failed. Please check the error messages above.")
        else:
            print("Migration cancelled.")
    else:
        print("No existing database found.")
        choice = input("Do you want to create sample data for testing? (y/n): ").lower()
        
        if choice == 'y':
            sample_file = "sample_data.json"
            create_sample_data(sample_file)
            print(f"\nSample data created: {sample_file}")
            print("You can use this to test the Chromebook version.")
        else:
            print("No action taken.")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main() 