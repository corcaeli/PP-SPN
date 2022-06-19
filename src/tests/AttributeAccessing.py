class Dummy:
    def __init__(self) -> None:
        Dummy.local = "12345"
        self.type = "Auto"
        self.__private_type = "Porsche"

    def __repr__(self) -> str:
        return f"local:{self.local}, type: {self.type}, private_type: {self.__private_type}"

    def change_type(self, new_type):
        self.type = new_type

    def change__private_type(self, new_type):
        self.__private_type = new_type


class Abc:
    def __init__(self) -> None:
        self.name = "hans"
        self.dummy = Dummy()
        self.dummy2 = Dummy()
        self.dummy2.change_type("Flugzeug")
        self.dummy2.change__private_type("Boing")

    def __repr__(self) -> str:
        return f"name: {self.name}\n\tdummy: {self.dummy}\n\tdummy2: {self.dummy2}"


def functionA(abc):
    abc.name = "fritz"
    abc.dummy.type = "Ente"
    abc.dummy.change__private_type("Donald")
    abc.dummy2.change_type("Hase")
    abc.dummy2 = Dummy()


little = Abc()
print(little)
functionA(little)
print(little)
