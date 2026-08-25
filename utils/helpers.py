from telegram import Update


def get_user_id(
    update: Update,
) -> int | None:

    if update.effective_user:
        return update.effective_user.id

    return None