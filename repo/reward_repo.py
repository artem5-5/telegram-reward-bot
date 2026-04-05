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

    def _get_next_id(self, rewards):
        if not rewards:
            return 1
        return max(r.get('id', 0) for r in rewards) + 1

    def get_rewards(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def save_rewards(self, rewards):
        with open(self.file_path, 'w') as f:
            json.dump(rewards, f, indent=4)

    def add_reward(self, username, comment, awarded_by):
        rewards = self.get_rewards()

        reward = {
            'id': self._get_next_id(rewards),
            'username': username,
            'comment': comment,
            'awarded_by': awarded_by,
            'timestamp': datetime.now().isoformat()
        }

        rewards.append(reward)
        self.save_rewards(rewards)

        return reward

    def get_user_rewards(self, username):
        rewards = self.get_rewards()
        return [r for r in rewards if r['username'] == username]

    def remove_reward(self, username, reason, removed_by):
        rewards = self.get_rewards()

        for i in range(len(rewards) - 1, -1, -1):
            if rewards[i]['username'] == username:
                removed_reward = rewards.pop(i)

                removed_reward['removed'] = {
                    'reason': reason,
                    'removed_by': removed_by,
                    'removed_at': datetime.now().isoformat()
                }

                self.save_rewards(rewards)
                return True, removed_reward

        return False, None

    def remove_reward_by_id(self, username, reward_id, removed_by):
        rewards = self.get_rewards()

        for i, reward in enumerate(rewards):
            if reward.get('id') == reward_id and reward['username'] == username:
                removed_reward = rewards.pop(i)

                removed_reward['removed'] = {
                    'removed_by': removed_by,
                    'removed_at': datetime.now().isoformat()
                }

                self.save_rewards(rewards)
                return True, removed_reward

        return False, None