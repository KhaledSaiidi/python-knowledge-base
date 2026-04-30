from dataclasses import dataclass

@dataclass
class Player:
    name: str
    state: str
    def get_infos(self) -> None:
        print(f'The Player name is {self.name} and state is {self.state}')