import abc
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
import os
import time
import traceback
from typing import Self
from git import DiffIndex, InvalidGitRepositoryError, Repo
from demo_app.domain.result import Result



# -----------------------------------------------------------------------------------------------

class DiffChangeType(StrEnum):
    Added = 'Added'
    Deleted = 'Deleted'
    Copied = 'Copied'
    Modified = 'Modified'
    Renamed = 'Renamed'
    TypeChange = 'TypeChanged'
    Untracked = 'Untracked'
    UNKNOWN = "UNKNOWN" 

    @staticmethod
    def convert(letter: str) -> Self:

        if letter == "A":
            return DiffChangeType.Added
        elif letter == "D":
            return DiffChangeType.Deleted
        elif letter == "C":
            return DiffChangeType.Copied
        elif letter == "M":
            return DiffChangeType.Modified
        elif letter == "R":
            return DiffChangeType.Renamed
        elif letter == "T":
            return DiffChangeType.TypeChange
        elif letter == "U":
            return DiffChangeType.Untracked
        
        return DiffChangeType.UNKNOWN

# -----------------------------------------------------------------------------------------------

class DiffViewModel:

    __slots__ = 'filename', 'dirname', 'change_type'

    def __init__(self, filename: str = None, dirname: str = None, change_type: DiffChangeType = DiffChangeType.UNKNOWN) -> None:
        self.filename = filename
        self.dirname = dirname
        self.change_type = change_type

    @property
    def filepath(self) -> str:
        if self.filename is None or self.dirname is None:
            return ""
        if len(self.dirname) == 0:
            return self.filename

        return f"{self.dirname}/{self.filename}"

    def __lt__(self, other):
         return self.filepath < other.filepath


# -----------------------------------------------------------------------------------------------

@dataclass(slots=True)
class RemoteStatus:
    commits_behind: int = 0
    commits_ahead: int = 0
    num_changes: int = 0
    

# -----------------------------------------------------------------------------------------------

class ISccService(ABC):

    @abc.abstractproperty
    def repo_path(self) -> str:
        pass

    @abc.abstractproperty
    def is_valid(self) -> bool:
        pass
    
    @abc.abstractproperty
    def active_branch_name(self) -> str | None:
        pass

    @abstractmethod
    def load(self, repo_path: str) -> Result:
        pass
     
    @abstractmethod
    def get_unstaged_items(self) -> list[DiffViewModel]:
        pass

    @abstractmethod
    def get_staged_items(self) -> DiffIndex:
        pass
    
    @abstractmethod
    def get_active_branch_remote_status(self) -> RemoteStatus | None:
        pass
    
    @abstractmethod
    def fetch(self) -> Result:
        pass
    
    @abstractmethod
    def stage_items(self, items: list[str]) -> Result:
        pass
    
    @abstractmethod
    def unstage_items(self, items: list[str]) -> Result:
        pass
    
    @abstractmethod
    def discard_items(self, items: list[str]) -> Result:
        pass

    @abstractmethod
    def pull(self) -> Result:
        pass
    
    @abstractmethod
    def push(self) -> Result:
        pass
    
    @abstractmethod
    def commit(self, message: str) -> Result:
        pass


# -----------------------------------------------------------------------------------------------

class MockSccService(ISccService):

    def __init__(self) -> None:
        self.__repo_path: str = "c:\\some\\path\\to\\the\\repo"
        self.__last_scc_error: str = ""

    @property
    def repo_path(self) -> str:
        return self.__repo_path


    @property
    def is_valid(self) -> bool:
        return True
    

    def load(self, repo_path: str) -> Result:
        return Result.success()

    def get_unstaged_items(self) -> list[DiffViewModel]:

        retval: list[DiffViewModel] = [
            DiffViewModel("new_file.py", "src", DiffChangeType.Added),
            DiffViewModel("old_file.py", "src", DiffChangeType.Deleted),
            DiffViewModel("README.md", "", DiffChangeType.Modified)
        ]

        retval.sort()
        return retval


    def get_staged_items(self) -> DiffIndex:

        retval: list[DiffViewModel] = [
            DiffViewModel("existing_file.py", "src", DiffChangeType.Modified),
        ]

        retval.sort()
        return retval
    
    @property
    def active_branch_name(self) -> str | None:
        return "main"
    

    def get_active_branch_remote_status(self) -> RemoteStatus | None:
        
        time.sleep(1)

        num_changes = len(self.get_staged_items())
        num_changes += len(self.get_unstaged_items())
        
        return RemoteStatus(2, 0, num_changes)
    

    def fetch(self) -> Result:
        time.sleep(1)
        return Result.success()
    

    def stage_items(self, items: list[str]) -> Result:
        return Result.fail("Not implemented by the mock service.")
        
    

    def unstage_items(self, items: list[str]) -> Result:
        return Result.fail("Not implemented by the mock service.")
    

    def discard_items(self, items: list[str]) -> Result:
        return Result.fail("Not implemented by the mock service.")
    


    def pull(self) -> Result:
        time.sleep(1)
        return Result.success()
    

    def push(self) -> Result:
        time.sleep(1)
        return Result.success()
    

    def commit(self, message: str) -> Result:
        time.sleep(1)
        return Result.success()
        

# -----------------------------------------------------------------------------------------------

class SccService(ISccService):

    def __init__(self) -> None:
        self.__repo_path: str = None
        self.__repo_handle: Repo = None
        self.__last_scc_error: str = None

    @property
    def repo_path(self) -> str:
        return self.__repo_path


    @property
    def is_valid(self) -> bool:
        return self.__repo_handle is not None
    


    def load(self, repo_path: str) -> Result:
        print(f"dbg: SccService::load({repo_path})")

        try:
            if (self.__repo_handle is not None):
                self.__repo_handle.close()
                self.__repo_handle = None

            repo = Repo(repo_path)
        except InvalidGitRepositoryError:
            self.__last_scc_error = f"The directory '{repo_path}' is not a valid git repository."
            return Result.fail(f"SCC ERROR: {self.__last_scc_error}")
        except Exception as e:
            return Result.fail(f"SCC ERROR: \n\n{traceback.format_exc()}")
        
        self.__repo_handle = repo
        self.__repo_path = repo_path

        return Result.success()
        




    def get_unstaged_items(self) -> list[DiffViewModel]:

        retval: list[DiffViewModel] = []

        diff_list  = self.__repo_handle.index.diff(None)

        for diff in diff_list:
            vm = DiffViewModel()
            vm.change_type = DiffChangeType.convert(diff.change_type)
            vm.filename = os.path.basename(diff.a_path)
            vm.dirname = os.path.dirname(diff.a_path)
            retval.append(vm)

        untracked_files = self.__repo_handle.untracked_files
        for file in untracked_files:
            vm = DiffViewModel()
            vm.change_type = DiffChangeType.Untracked
            vm.filename = os.path.basename(file)
            vm.dirname = os.path.dirname(file)
            retval.append(vm)

        retval.sort()
        return retval




    def get_staged_items(self) -> DiffIndex:

        retval: list[DiffViewModel] = []

        diff_list  = self.__repo_handle.head.commit.diff()

        for diff in diff_list:
            vm = DiffViewModel()
            vm.change_type = DiffChangeType.convert(diff.change_type)
            vm.filename = os.path.basename(diff.a_path)
            vm.dirname = os.path.dirname(diff.a_path)
            retval.append(vm)

        retval.sort()
        return retval
    
    @property
    def active_branch_name(self) -> str | None:
        if self.__repo_handle is None:
            return None
        return self.__repo_handle.active_branch.name
    

    def get_active_branch_remote_status(self) -> RemoteStatus | None:
        if self.__repo_handle is None:
            return None
        branch_name = self.active_branch_name
        commits_diff = self.__repo_handle.git.rev_list('--left-right', '--count', f'{branch_name}...{branch_name}@{{u}}')
        num_ahead, num_behind = commits_diff.split('\t')

        num_changes = len(self.get_staged_items())
        num_changes += len(self.get_unstaged_items())
        
        return RemoteStatus(num_behind, num_ahead, num_changes)
    

    def fetch(self) -> Result:
        if self.__repo_handle is None:
            return Result.fail("SCC Service not initialized.")
        
        for remote in self.__repo_handle.remotes:
            remote.fetch()

        return Result.success()
    

    def stage_items(self, items: list[str]) -> Result:
        if self.__repo_handle is None:
            return Result.fail("SCC Service is not initialized.")
        
        try:
            for item in items:
                self.__repo_handle.git.add('-A', item)
        except Exception as e:
            return Result.fail(str(e))
        
        return Result.success()
    

    def unstage_items(self, items: list[str]) -> Result:
        if self.__repo_handle is None:
            return Result.fail("SCC Service is not initialized.")
        
        try:
            for item in items:
                self.__repo_handle.git.reset("HEAD", item)

        except Exception as e:
            return Result.fail(str(e))
        
        return Result.success()
    

    def discard_items(self, items: list[str]) -> Result:
        if self.__repo_handle is None:
            return Result.fail("SCC Service is not initialized.")
        
        untracked_files = self.__repo_handle.untracked_files

        try:
            for item in items:
                if item in untracked_files:
                    self.__repo_handle.git.clean("-f", item)
                else:
                    self.__repo_handle.git.checkout("-f", item)

            self.__repo_handle.git.checkout()

        except Exception as e:
            return Result.fail(str(e))
        
        return Result.success()
    


    def pull(self) -> Result:
        if self.__repo_handle is None:
            return Result.fail("SCC Service is not initialized.")
        
        try:
            self.__repo_handle.git.pull('--tags')

        except Exception as e:
            return Result.fail(str(e))
        
        return Result.success()
    

    def push(self) -> Result:
        if self.__repo_handle is None:
            return Result.fail("SCC Service is not initialized.")
        
        try:
            self.__repo_handle.git.push()

        except Exception as e:
            return Result.fail(str(e))
        
        return Result.success()
    

    def commit(self, message: str) -> Result:
        if self.__repo_handle is None:
            return Result.fail("SCC Service is not initialized.")
        
        try:
            self.__repo_handle.index.commit(message)
        except Exception as e:
            return Result.fail(str(e))
        
        return Result.success()
        