import abc
from abc import ABC, abstractmethod
import time
from typing import Self
from demo_app.domain.result import Result

class IAuthService(ABC):

    @abc.abstractproperty
    def current_user_name(self) -> str:
        pass
    
    @abc.abstractproperty
    def is_authenticated(self) -> bool:
        pass

    @abstractmethod
    def login(self, uname: str, passwd: str) -> Result:
        pass
        
    @abstractmethod
    def logout(self) -> None:
        pass


class MockAuthService(IAuthService):

    def __init__(self) -> None:        
        self.__uname: str = None
        self.__is_authenticated: bool = False


    @property
    def current_user_name(self) -> str:
        return self.__uname
    
    @property
    def is_authenticated(self) -> bool:
        return self.__is_authenticated


    def login(self, uname: str, passwd: str) -> Result:

        time.sleep(2)
        result = Result.success()
        if (uname != "a" or passwd != "a"):
            result = Result.fail("Invalid username and password.")

        self.__is_authenticated = True
        self.__uname: str = "MockUser"
        
        return Result.success()


    def logout(self) -> None:
        self.__uname = None
        self.__is_authenticated = False