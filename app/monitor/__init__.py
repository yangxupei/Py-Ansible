# coding:utf-8
from flask import Blueprint
monitor = Blueprint('monitor', __name__,)
from app.monitor import views