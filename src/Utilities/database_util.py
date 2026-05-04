import sqlite3
import os
import json
import warnings
from datetime import datetime

# GEN 2: We have like 2 days left :(
class DatabaseManager:
    def __init__(self, db_name="app_database.db", db_directory=None):
        """
        Sets up the path for the database. Defaults to the same folder as the script.
        """
        if db_directory is None:
            self.db_path = os.path.join(os.getcwd(), db_name)
        else:
            self.db_path = os.path.join(db_directory, db_name)
        print("Initialized @ ", self.db_path)
        self.connection = None
        self.cursor = None

    # ---------------------------------------------------------
    # INITIALIZATION & CONNECTION
    # ---------------------------------------------------------
    def connect(self):
        """Connects to the database and handles connection errors."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            
            # Enforce foreign key constraints (ensures linked tables behave correctly)
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            print(f"Successfully connected to database at: {self.db_path}")
        except sqlite3.Error as database_error:
            print(f"Failed to connect to the database: {database_error}")

    def close(self):
        """Safely closes the database connection."""
        if self.connection:
            self.connection.close()

    # ---------------------------------------------------------
    # SCHEMA CREATION
    # ---------------------------------------------------------
    def create_tables(self):
        """Creates the required tables if they don't already exist."""
        if not self.connection:
            self.connect()

        try:
            # Table 1: Personal Info
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS personal_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    age INTEGER,
                    birthdate TEXT,
                    password TEXT,
                    email TEXT UNIQUE NOT NULL,
                    email_univ TEXT UNIQUE,
                    phone_number TEXT UNIQUE,
                    account_type TEXT NOT NULL CHECK(account_type IN ('student', 'instructor', 'general'))
                )
            """)

            # Table 2: Website Info
            # Linked 1-to-1 with personal_info via user_id
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS website_info (
                    user_id INTEGER PRIMARY KEY,
                    lessons_and_scores TEXT DEFAULT '{}',
                    lesson_completed TEXT DEFAULT '',
                    classroom_hosted TEXT DEFAULT '',
                    classroom_joined TEXT DEFAULT '',
                    FOREIGN KEY (user_id) REFERENCES personal_info (id) ON DELETE CASCADE
                )
            """)
            
            self.connection.commit()
            print("Tables created or verified successfully.")
        except sqlite3.Error as table_error:
            print(f"Error creating tables: {table_error}")
        self.close()

    # ---------------------------------------------------------
    # HELPER METHODS (Age Calculation) - kinda useless rn
    # ---------------------------------------------------------
    def _calculate_age(self, birthdate_string):
        """Calculates age based on a YYYY-MM-DD string."""
        if not birthdate_string:
            return None
        try:
            birth_date = datetime.strptime(birthdate_string, "%Y-%m-%d")
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except ValueError:
            print("Invalid date format. Expected YYYY-MM-DD.")
            return None

    # ---------------------------------------------------------
    # CRUD: CREATE & READ & DELETE
    # ---------------------------------------------------------
    def create_user(self, username, birthdate, email, account_type, password, email_univ=None, phone_number=None):
        """Creates a new user and sets up their empty website info."""
        
        try:
            # 1. Insert into personal_info
            self.cursor.execute("""
                INSERT INTO personal_info 
                (username, birthdate, email, email_univ, phone_number, account_type, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (username, birthdate, email, email_univ, phone_number, account_type, password))
            
            # Grab the ID that SQLite automatically generated for this new user
            new_user_id = self.cursor.lastrowid
            
            # 2. Create the linked row in website_info
            self.cursor.execute("""
                INSERT INTO website_info (user_id) VALUES (?)
            """, (new_user_id,))
            
            self.connection.commit()
            print(f"User '{username}' created successfully with ID {new_user_id}.")
            return new_user_id
            
        except sqlite3.IntegrityError as integrity_error:
            print(f"Failed to create user (Likely a duplicate email or phone): {integrity_error}")
            return None

    def get_user_full_profile(self, user_id):
        """Fetches all data across both tables for a specific user."""

        warnings.deprecated(
            "A better and less convoluted option exist. Use get_user_info() instead.",
            DeprecationWarning,
            )
        
        self.cursor.execute("""
            SELECT p.*, w.lessons_and_scores, w.lesson_completed, w.classroom_hosted, w.classroom_joined
            FROM personal_info p
            JOIN website_info w ON p.id = w.user_id
            WHERE p.id = ?
        """, (user_id,))
        
        return self.cursor.fetchone()

    def get_user_info(self, user_id=-1, username="NULL"):
        print("trying to find", user_id, "or", username)
        self.cursor.execute("SELECT id, username, birthdate, email, email_univ, account_type FROM personal_info WHERE id = ? OR username = ? OR email = ? OR email_univ = ?", (user_id, username, username, username))
        return self.cursor.fetchone()

    def delete_user(self, user_id):
        """Deletes a user. ON DELETE CASCADE ensures website_info is also wiped."""
        try:
            self.cursor.execute("DELETE FROM personal_info WHERE id = ?", (user_id,))
            self.connection.commit()
            print(f"User {user_id} completely removed from database.")
        except sqlite3.Error as delete_error:
            print(f"Error deleting user: {delete_error}")

    # ---------------------------------------------------------
    # CRUD: UPDATE (Convenience Methods)
    # ---------------------------------------------------------
    def _update_single_field(self, table_name, column_name, new_value, user_id):
        """A private helper method to keep code DRY (Don't Repeat Yourself)."""
        try:
            identifier_column = "id" if table_name == "personal_info" else "user_id"
            
            query = f"UPDATE {table_name} SET {column_name} = ? WHERE {identifier_column} = ?"
            self.cursor.execute(query, (new_value, user_id))
            self.connection.commit()
        except sqlite3.Error as update_error:
            print(f"Error updating {column_name}: {update_error}")

    # --- Verification ---

    def verify_user_logon(self, usernameOrEmail, password) -> bool:
        self.connect()
        found = False
        print("Passing: ", usernameOrEmail, password)
        self.cursor.execute("SELECT * FROM personal_info WHERE (username = ? OR email = ? OR email_univ = ?) AND password = ?", (usernameOrEmail, usernameOrEmail, usernameOrEmail, password))
        if (len(self.cursor.fetchall())==1):
            print("Found")
            found = True
        else:
            print("ERROR: None Found or there are duplicates. Perform Manual mentainance if latter.")
            found = False
        self.close()
        return found

    # --- Personal Info Updates ---
    def update_password(self, user_id, new_password):
        """Updates the user's password securely."""
        self._update_single_field("personal_info", "password", new_password, user_id)

    def update_username(self, user_id, new_username):
        self._update_single_field("personal_info", "username", new_username, user_id)

    def update_email(self, user_id, new_email):
        self._update_single_field("personal_info", "email", new_email, user_id)

    def update_phone_number(self, user_id, new_phone):
        self._update_single_field("personal_info", "phone_number", new_phone, user_id)

    def update_birthdate(self, user_id, new_birthdate):
        """Updates the birthdate AND automatically recalculates/updates the age."""
        self._update_single_field("personal_info", "birthdate", new_birthdate, user_id)
        
        new_age = self._calculate_age(new_birthdate)
        if new_age is not None:
            self._update_single_field("personal_info", "age", new_age, user_id)

    # --- Website Info Updates ---
    def update_lessons_and_scores(self, user_id, dictionary_data):
        """Takes a Python dictionary and converts it to a JSON string for storage."""
        json_string = json.dumps(dictionary_data) 
        self._update_single_field("website_info", "lessons_and_scores", json_string, user_id)

    def update_completed_lessons(self, user_id, comma_separated_string):
        self._update_single_field("website_info", "lesson_completed", comma_separated_string, user_id)

    def update_classrooms_joined(self, user_id, comma_separated_string):
        self._update_single_field("website_info", "classroom_joined", comma_separated_string, user_id)    

    # ---------------------------------------------------------
    # WEBSITE INFO: LESSONS & SCORES MANAGEMENT
    # ---------------------------------------------------------

    def _resolve_user_id(self, identifier):
        """Internal helper to find a user_id whether they pass an ID, email, or username."""
        if isinstance(identifier, int):
            return identifier
            
        user_data = self.get_user_info(username=identifier)
        if user_data:
            return user_data[0] # Returns the user's ID
        return None

    def _get_lessons_dict(self, user_id):
        """Internal helper to fetch and parse the JSON dictionary of lessons."""
        self.cursor.execute("SELECT lessons_and_scores FROM website_info WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result and result[0]:
            try:
                return json.loads(result[0])
            except json.JSONDecodeError:
                return {}
        return {}

    def add_lesson(self, identifier, lesson_title):
        """Appends a new lesson to the user's progress with a baseline score of 0."""
        self.connect()
        user_id = self._resolve_user_id(identifier)
        if not user_id:
            print("Failed to add lesson: User not found.")
            self.close()
            return False

        lessons_dict = self._get_lessons_dict(user_id)
        
        if lesson_title not in lessons_dict:
            lessons_dict[lesson_title] = 0
            
            json_string = json.dumps(lessons_dict)
            self.cursor.execute("UPDATE website_info SET lessons_and_scores = ? WHERE user_id = ?", (json_string, user_id))
            self.connection.commit()
            print(f"Added lesson '{lesson_title}' to user ID {user_id}.")
        
        self.close()
        return True

    def add_lesson_score(self, identifier, lesson_title, score_to_add):
        """Adds points to the accumulative score of a specific lesson block."""
        self.connect()
        user_id = self._resolve_user_id(identifier)
        if not user_id:
            print("Failed to add score: User not found.")
            self.close()
            return False

        lessons_dict = self._get_lessons_dict(user_id)
        
        if lesson_title not in lessons_dict:
            lessons_dict[lesson_title] = 0
            
        lessons_dict[lesson_title] += score_to_add
        
        json_string = json.dumps(lessons_dict)
        self.cursor.execute("UPDATE website_info SET lessons_and_scores = ? WHERE user_id = ?", (json_string, user_id))
        self.connection.commit()
        print(f"Added {score_to_add} pts to '{lesson_title}'. New total: {lessons_dict[lesson_title]}")
        
        self.close()
        return True

    def get_user_lessons(self, identifier):
        """Returns a list of all lesson titles the user has interacted with."""
        self.connect()
        user_id = self._resolve_user_id(identifier)
        if not user_id:
            self.close()
            return []
            
        lessons_dict = self._get_lessons_dict(user_id)
        self.close()
        
        # Return just the keys (e.g., ["Intro to Logic Gates", "Boolean Algebra"])
        return list(lessons_dict.keys())

    def get_user_scores(self, identifier):
        """Returns the full dictionary mapping lesson titles to their accumulative scores."""
        self.connect()
        user_id = self._resolve_user_id(identifier)
        if not user_id:
            self.close()
            return {}
            
        lessons_dict = self._get_lessons_dict(user_id)
        self.close()
        
        # Return the whole mapping (e.g., {"Intro to Logic Gates": 85, "Boolean Algebra": 100})
        return lessons_dict