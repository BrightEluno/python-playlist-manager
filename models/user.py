from dataclasses import dataclass

@dataclass
class User:
    userName: str
    password: str

    def authentication(self, userName: str, password: str) -> bool:
        # checking for provided credentials against this users credentials
        return self.userName == userName and self.password == password