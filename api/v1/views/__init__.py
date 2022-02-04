#!/usr/bin/python3
""" to import the views"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')