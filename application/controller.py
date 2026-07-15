#business logic
from flask import Flask, render_template, redirect, url_for, request
#from app import app circular import error
from flask import current_app as app
from .models import *