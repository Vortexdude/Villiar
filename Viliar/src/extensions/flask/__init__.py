from flask import Flask as BaseFlask
from .config import Config


class Flask(BaseFlask):

    config_class = Config
