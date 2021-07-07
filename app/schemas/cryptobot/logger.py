from typing import Optional

from pydantic import BaseModel


class LoggerBase(BaseModel):
    filelog: bool = False
    logfile: str = "pycryptobot.log"
    fileloglevel: str # enum("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    consolelog: bool = True
    consoleloglevel: str # enum("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


class LoggerCreate(LoggerBase):
    filelog: bool = False
    logfile: str = "pycryptobot.log"
    fileloglevel: str # enum("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    consolelog: bool = True
    consoleloglevel: str # enum("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


class Logger(LoggerBase):
    pass
