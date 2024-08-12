
from typing import Self


class Result:

    def __init__(self, is_success: bool, value: any, error: str) -> None:
        self.__is_success = is_success
        self.__value = value
        self.__error = error

    @property
    def is_failed(self) -> bool:
        return not self.__is_success
    
    @property
    def is_success(self) -> bool:
        return not self.__is_success
    
    @property
    def error(self) -> str:
        return self.__error
    
    @property
    def val(self) -> str:
        return self.__value

    @classmethod
    def fail(cls, error: str) -> Self:
        return Result(False, None, error)
    

    @classmethod
    def success(cls) -> Self:
        return Result(True, None, None)
    

    @classmethod
    def success_val(cls, value: any) -> Self:
        return Result(True, value, None)
    
