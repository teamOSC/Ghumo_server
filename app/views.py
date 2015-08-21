from flask import Flask, request, render_template, url_for, redirect
import json
from app import app


@app.route('/testing')
def testing():
    return "API Working!"
