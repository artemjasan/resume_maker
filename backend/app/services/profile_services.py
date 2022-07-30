from app import models
from app.core.config import settings


def check_profiles_number(current_user: models.User) -> bool:
    """
    Check number of profiles for requested user. If more than config parameter,
    the service return False otherwise True.
    """
    if len(current_user.profiles) >= settings.MAX_USER_PROFILES:
        return False
    return True

