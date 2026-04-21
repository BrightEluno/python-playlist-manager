"""
This is the authentication service with a limited attempt tries locking message.
"""
import time
from models.user import User

class AuthenticationService:
    """
    Authentication service is enforcing three attempts limiting the user for only three attempt after three attempts the system will display a lock simulated by displaying a message
    """

    def __init__(self, users: User, max_attempt: int = 3, minutes_lock: int = 5):
        self.users = users
        self.max_attempt = max_attempt
        self.minutes_lock = minutes_lock
        self.failed_attempts = 0
        self.locked_time = None
    
    def locked(self) -> bool:
        if self.locked_time is None:
            return False
        return time.time() < self.locked_time
    
    def login_attempt (self, userName: str, password: str ) -> bool:
        """
        The attempt to authenticate will returns True if successful and False on failure

        if the max attempts is exceeded the user is locked for 5 minutes
        """
        if self.locked():
            return False

        if self.users.authentication(userName, password):
            self.failed_attempts = 0
            return True
        # failed login
        self.failed_attempts += 1
        if self.failed_attempts >= self.max_attempt:
            self.locked_time = time.time() + (self.minutes_lock * 60)
        return False

