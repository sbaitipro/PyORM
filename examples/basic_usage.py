# examples/basic_usage.py

import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyorm.entity import Entity
from pyorm.db_manager import DBManager


# Define the User entity
class User(Entity):
    _fields = {
        "username": {"type": "TEXT", "constraints": "NOT NULL"},
        "email": {"type": "TEXT", "constraints": "UNIQUE NOT NULL"},
    }

    def __init__(self, id=None, username=None, email=None):
        super().__init__()
        self.id = id
        self.username = username
        self.email = email


def main():
    # Database file path
    db_path = "examples/database/test.db"

    # Step 1: Connect to the database
    try:
        DBManager.connect(db_path)
        User.connect()
        print(f"Connected to database: {db_path}")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return

    # Step 2: Create the 'users' table if it doesn't exist
    if not User.is_table_exist():
        User.create_table()
    else:
        print("Table 'users' already exists.")

    # Step 3: Delete all records if they exist
    User.delete_all()

    # Step 4: Insert a new user
    user = User(username="groot", email="groot@example.com")
    if user.save():
        print(f"Inserted user with ID {user.id}, username: {user.username}")
    else:
        print("Failed to insert user.")
        return

    # Step 5: Retrieve all users
    users = User.all()
    print("All users:")
    for u in users:
        print(f"User: {u.username}, Email: {u.email}")

    # Step 6: Find a user by ID
    found_user = User.find_by_id(user.id)
    if found_user:
        print(f"Found user: {found_user.username}, ID: {found_user.id}")
    else:
        print(f"No user found with ID: {user.id}")

    # Step 7: Update a user
    found_user.username = "baby_groot"
    if found_user.save():
        print(f"Updated user: {found_user.username}, ID: {found_user.id}")
    else:
        print("Failed to update user.")

    # Step 8: Delete a user
    if found_user.delete():
        print(f"Deleted user with ID {found_user.id}")
    else:
        print("Failed to delete user.")

    # Step 9: Drop the 'users' table
    if User.drop():
        print("Dropped 'users' table.")
    else:
        print("Failed to drop 'users' table.")

    # Step 10: Disconnect from the database
    DBManager.disconnect()
    print("Disconnected from the database.")


if __name__ == "__main__":
    main()