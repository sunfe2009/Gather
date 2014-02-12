# -*- coding:utf-8 -*-

from flask import Blueprint, render_template
from gather.topic.models import Topic

bp = Blueprint("frontend", __name__, url_prefix="/")


@bp.route("/")
def index():
    topics = Topic.query.order_by(Topic.created.desc()).limit(20)
    return render_template("index.html", topics=topics)