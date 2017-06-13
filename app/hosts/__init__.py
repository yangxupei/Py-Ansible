# coding:utf-8
from flask import Blueprint
hosts = Blueprint('hosts', __name__,)
from app.hosts import views