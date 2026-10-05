from Supports import VaultError

class Check():
    def __init__(self, error: bool=True, name: list=None):
        self.name = name
        self.error = error

    def check_name(self):
        if self.name is not None:
            name = self.name[0]
            if len(self.name) == 1:
                character = ['/', '\\', '..', ' ', '']
            else:
                character = self.name[1]

            for Name in name:
                for Character in character:
                    if Character in Name:
                        if self.error == True:
                            raise VaultError.InvalidName(f"Invalid_name:{Name}")
                        else:
                            return "Invalid_name!"
        else:
            return "Name_is_none!"