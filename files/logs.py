import os
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


class Logs:

    def __init__(self, objectName:str):

        self.level = 'INFO'
        if "LOG_LEVEL" in os.environ:
            self.level = os.environ["LOG_LEVEL"]

        self.format = 'TEXT'
        if "LOG_FORMAT" in os.environ:
            self.format = os.environ["LOG_FORMAT"]

        self.objectName = objectName

    def __print__(self, level:str, extraFields:dict):
        current_timezone_str = os.getenv('TZ', 'UTC')
        current_timezone = ZoneInfo(current_timezone_str)

        fields = {
            'date': datetime.now(tz=current_timezone).strftime("%Y-%m-%d %H:%M:%S"),
            'level': level,
            'objectName': self.objectName
        }

        # Include extra fields custom by the user
        if extraFields is not None:
            fields.update(extraFields)

        if self.format == 'JSON':
            print(json.dumps(fields))
        else:
            print(' - '.join(map(str, fields.values())))

    def error(self, extraFields:dict=None):
        if self.level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            self.__print__('ERROR', extraFields)

    def warning(self, extraFields:dict=None):
        if self.level in ['DEBUG', 'INFO', 'WARNING']:
            self.__print__('WARNING', extraFields)

    def info(self, extraFields:dict=None):
        if self.level in ['DEBUG', 'INFO']:
            self.__print__('INFO', extraFields)

    def debug(self, extraFields:dict=None):
        if self.level in ['DEBUG']:
            self.__print__('DEBUG', extraFields)
