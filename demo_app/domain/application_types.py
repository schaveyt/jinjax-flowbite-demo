
class ApplicationState:
    def __init__(self, app_version: str, app_title: str):
        self.app_version = app_version
        self.app_title = app_title        
        self.app_error: str = None
        self.pending_commit_msg: str = ""

    def reset(self) -> None:
        self.app_error = None
	
