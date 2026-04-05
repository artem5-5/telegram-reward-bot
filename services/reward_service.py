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

        reward = self.reward_repo.add_reward(
            awarded_username,
            comment,
            awarded_by_username
        )

        return True, (
            f"🎉 Поздравляем @{awarded_username} с наградой! 🎉\n"
            f"ID: #{reward['id']}\n"
            f"Причина: {comment}"
        )

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

    def get_user_rewards(self, username):
        return self.reward_repo.get_user_rewards(username)

    # 🔴 старый способ (оставили)
    def remove_reward(self, target_username, reason, removed_by):
        if not self.can_award(removed_by):
            return False, "У вас нет прав для удаления наград."

        success, removed_reward = self.reward_repo.remove_reward(
            target_username,
            reason,
            removed_by
        )

        if not success:
            return False, f"У пользователя @{target_username} нет наград."

        return True, (
            f"❌ Удалена последняя награда у @{target_username}\n"
            f"Причина: {reason}"
        )

    # 🆕 новый способ по ID
    def remove_reward_by_id(self, target_username, reward_id, removed_by):
        if not self.can_award(removed_by):
            return False, "У вас нет прав для удаления наград."

        success, removed_reward = self.reward_repo.remove_reward_by_id(
            target_username,
            reward_id,
            removed_by
        )

        if not success:
            return False, f"Награда с ID {reward_id} не найдена у @{target_username}."

        return True, f"❌ Награда #{reward_id} удалена у @{target_username}."

    def format_user_rewards(self, username):
        rewards = self.get_user_rewards(username)

        if not rewards:
            return f"У пользователя @{username} нет наград."

        lines = [f"📜 Награды пользователя @{username}:\n"]

        for r in rewards:
            lines.append(
                f"#{r.get('id', '?')}. {r['comment']} "
                f"(выдал @{r['awarded_by']}, {r['timestamp']})"
            )

        return "\n".join(lines)