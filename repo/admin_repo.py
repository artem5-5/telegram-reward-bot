import json
import os
from config import OWNER_USERNAME

class AdminRepo:
    def __init__(self, file_path='data/admins.json'):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([OWNER_USERNAME], f)  # Инициализируем с владельцем

    def get_admins(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def add_admin(self, username):
        admins = self.get_admins()
        if username not in admins:
            admins.append(username)
            with open(self.file_path, 'w') as f:
                json.dump(admins, f)

    def remove_admin(self, username):
        admins = self.get_admins()
        if username in admins and username != OWNER_USERNAME:  # Не удалять владельца
            admins.remove(username)
            with open(self.file_path, 'w') as f:
                json.dump(admins, f)

    def is_admin(self, username):
        return username in self.get_admins()