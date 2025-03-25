import sys
import os

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


# Step 1: Connect to the database
DBManager.connect("examples/database/test.db")
User.connect()

# Step 2: Create the 'users' table if it doesn't exist
if not User.is_table_exist():
    User.create_table()
    

# Delete all records if exist
User.delete_all()

# Step 3: Insert a new user
user = User(username="groot", email="groot@example.com")
user.save()
print(f"Inserted user with ID {user.id}, username: {user.username}")

# Step 4: Retrieve all users
users = User.all()
for u in users:
    print(f"User: {u.username}, Email: {u.email}")

# Step 5: Find a user by ID
found_user = User.find_by_id(user.id)
if found_user:
    print(f"Found user: {found_user.username}, ID: {found_user.id}")

# Step 6: Update a user
found_user.username = "baby_groot"
found_user.save()
print(f"Updated user: {found_user.username}, ID: {found_user.id}")

# Step 7: Delete a user
found_user.delete()
print(f"Deleted user with ID {found_user.id}")

# Step 8: Drop the 'users' table
User.drop()

# Step 9: Disconnect from the database
DBManager.disconnect()