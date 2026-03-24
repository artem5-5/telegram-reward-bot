from repo.admin_repo import AdminRepo
from repo.reward_repo import RewardRepo
from config import OWNER_USERNAME

class RewardService:
    def __init__(self):
        self.admin_repo = AdminRepo()
        self.reward_repo = RewardRepo()

    def can_award(self, username):
        return self.admin_repo.is_admin(username)

    def award_reward(self, awarded_username, comment, awarded_by_username):
        if not self.can_award(awarded_by_username):
            return False, "У вас нет прав для выдачи наград."
        self.reward_repo.add_reward(awarded_username, comment, awarded_by_username)
        return True, f"🎉 Поздравляем @{awarded_username} с наградой! 🎉\nПричина: {comment}"

    def add_admin(self, owner_username, new_admin_username):
        if owner_username != OWNER_USERNAME:
            return False, "Только владелец может добавлять администраторов."
        self.admin_repo.add_admin(new_admin_username)
        return True, "Администратор добавлен."

    def remove_admin(self, owner_username, admin_username):
        if owner_username != OWNER_USERNAME:
            return False, "Только владелец может удалять администраторов."
        self.admin_repo.remove_admin(admin_username)
        return True, "Администратор удалён."

    def get_user_reward_count(self, username):
        return len(self.reward_repo.get_user_rewards(username))