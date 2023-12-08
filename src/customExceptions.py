class InvalidFunctionArguments(Exception):
    pass

class CannotFollowSelf(Exception):
    def __init__(self):
        super().__init__("Não é possível seguir a si mesmo.")

class CannotUnfollowSelf(Exception):
    def __init__(self):
        super().__init__("Não é possível deixar de seguir a si mesmo.")

class AlreadyFollowing(Exception):
    def __init__(self):
        super().__init__("Não é possível seguir novamente o mesmo usuário.")

class AlreadyNotFollowing(Exception):
    def __init__(self) -> None:
        super().__init__("Não é possível deixar de seguir novamente o mesmo usuário.")
class FollowInvalidUser(Exception):
    def __init__(self) -> None:
        super().__init__("Não é possível seguir usuário inválido.")
class UnfollowInvalidUser(Exception):
    def __init__(self) -> None:
        super().__init__("Não é possível deixar de seguir usuário inválido.")