def is_coach(user) -> bool:
    return user.groups.filter(name='Coaches').exists()
