import json
import os
import traceback
from demo_app.domain.application_types import ApplicationState
from demo_app.domain.result import Result
from demo_app.services.auth_service import IAuthService, MockAuthService
from demo_app.services.scc_service import ISccService, MockSccService


class ApplicationServices:
    
    def __init__(self, app_title: str, app_version: str) -> None:
        self.app_state: ApplicationState = ApplicationState(app_version, app_title)
        self.auth_service: IAuthService = MockAuthService() # change when actually have an auth services
        self.scc_service: ISccService = MockSccService() # change when actually have an auth services
        
