# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash
from . import ranking
from ..utils import ranking_statics


@ranking.route('/Ranking')
def ranking():
    owns = ranking_statics.count_owned()
    reads = ranking_statics.count_borrowed()
    pops = ranking_statics.count_pop_book()
    return render_template('ranking.html', owns=owns, reads=reads, pops=pops)
