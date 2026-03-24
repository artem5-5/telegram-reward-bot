import json
import os
from datetime import datetime

class RewardRepo:
    def __init__(self, file_path='data/rewards.json'):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def add_reward(self, username, comment, awarded_by):
        rewards = self.get_rewards()
        reward = {
            'username': username,
            'comment': comment,
            'awarded_by': awarded_by,
            'timestamp': datetime.now().isoformat()
        }
        rewards.append(reward)
        with open(self.file_path, 'w') as f:
            json.dump(rewards, f, indent=4)

    def get_rewards(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def get_user_rewards(self, username):
        rewards = self.get_rewards()
        return [r for r in rewards if r['username'] == username]