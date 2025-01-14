from flask import Blueprint

damath = Blueprint("damath", __name__)

from . import controller
