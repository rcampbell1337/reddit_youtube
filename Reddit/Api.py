from abc import abstractmethod
from typing import List

class Api:

    @abstractmethod
    def get_list_of_posts(self) -> List[str]:
        pass