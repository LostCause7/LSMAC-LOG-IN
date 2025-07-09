import sqlite3
import datetime
from typing import List, Tuple, Optional

class CheckInDatabase:
    def __init__(self, db_path: str = "checkin_system.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create members table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create check_ins table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS check_ins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id TEXT NOT NULL,
                    check_in_date DATE NOT NULL,
                    check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (member_id) REFERENCES members (member_id)
                )
            ''')
            
            conn.commit()
    
    def add_member(self, member_id: str, name: str, email: str = None, phone: str = None) -> bool:
        """Add a new member to the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO members (member_id, name, email, phone)
                    VALUES (?, ?, ?, ?)
                ''', (member_id, name, email, phone))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False  # Member ID already exists
    
    def get_member(self, member_id: str) -> Optional[Tuple]:
        """Get member information by member ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT member_id, name, email, phone, created_date
                FROM members WHERE member_id = ?
            ''', (member_id,))
            return cursor.fetchone()
    
    def record_check_in(self, member_id: str, check_in_date: str = None) -> bool:
        """Record a check-in for a member"""
        if check_in_date is None:
            check_in_date = datetime.date.today().isoformat()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO check_ins (member_id, check_in_date)
                    VALUES (?, ?)
                ''', (member_id, check_in_date))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_check_ins_for_date(self, date: str) -> List[Tuple]:
        """Get all check-ins for a specific date"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.name, m.member_id, ci.check_in_time
                FROM check_ins ci
                JOIN members m ON ci.member_id = m.member_id
                WHERE ci.check_in_date = ?
                ORDER BY ci.check_in_time DESC
            ''', (date,))
            return cursor.fetchall()
    
    def get_member_check_in_history(self, member_id: str) -> List[Tuple]:
        """Get check-in history for a specific member"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT check_in_date, check_in_time
                FROM check_ins
                WHERE member_id = ?
                ORDER BY check_in_time DESC
            ''', (member_id,))
            return cursor.fetchall()
    
    def has_checked_in_today(self, member_id: str) -> bool:
        """Check if a member has already checked in today"""
        today = datetime.date.today().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM check_ins
                WHERE member_id = ? AND check_in_date = ?
            ''', (member_id, today))
            return cursor.fetchone()[0] > 0 