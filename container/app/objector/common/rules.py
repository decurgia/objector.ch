import rules


@rules.predicate
def user_is_logged_in_user(user, user_record):
    return rules.is_authenticated(user) and user_record == user


rules.add_perm("common.change_user", user_is_logged_in_user)
rules.add_perm("common.view_user", user_is_logged_in_user)
rules.add_perm("common.delete_user", user_is_logged_in_user)
