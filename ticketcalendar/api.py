# -*- coding: utf_8 -*-
#
# Copyright (C) 2013 OpenGroove,Inc.
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

from datetime import datetime
try:
    from babel import Locale
    from babel.core import LOCALE_ALIASES, UnknownLocaleError
    from babel.dates import (get_day_names as babel_get_day_names,
                             get_month_names as babel_get_month_names,
                             format_date as babel_format_date)
except ImportError:
    Locale = None
    LOCALE_ALIASES = {}
    UnknownLocaleError = None
    babel_get_day_names = None
    babel_get_month_names = None
    babel_format_date = None

from trac.config import Option, ListOption, IntOption
from trac.util import arity
from trac.util.translation import domain_functions, dgettext


TEXTDOMAIN = 'ticketcalendar'


_, tag_, N_, gettext, add_domain = domain_functions(
    TEXTDOMAIN,
    ('_', 'tag_', 'N_', 'gettext', 'add_domain'))


if arity(Option.__init__) <= 5:
    def _option_with_tx(Base): # Trac 0.12.x
        class Option(Base):
            def __getattribute__(self, name):
                val = Base.__getattribute__(self, name)
                if name == '__doc__':
                    val = dgettext(TEXTDOMAIN, val)
                return val
        return Option
else:
    def _option_with_tx(Base): # Trac 1.0 or later
        class Option(Base):
            def __init__(self, *args, **kwargs):
                kwargs['doc_domain'] = TEXTDOMAIN
                Base.__init__(self, *args, **kwargs)
        return Option


Option = _option_with_tx(Option)
IntOption = _option_with_tx(IntOption)
ListOption = _option_with_tx(ListOption)


def get_day_names(width='wide', context='format', locale=None):
    if locale:
        return babel_get_day_names(width=width, context=context, locale=locale)
    else:
        names = dict()
        for day in range(0, 7):
            dt = datetime(2001, 1, day + 1)
            names[day] = dt.strftime('%a')
        return names


def get_month_names(width='wide', context='format', locale=None):
    if locale:
        return babel_get_month_names(width=width, context=context,
                                     locale=locale)
    else:
        names = dict()
        for m in range(1, 13):
            dt = datetime(2001, m, 1)
            names[m] = dt.strftime('%B')
        return names


def format_date(date=None, format='medium', locale=None):
    if locale:
        return babel_format_date(date=date, format=format, locale=locale)
    else:
        return str(date)


def is_weekend(date, locale):
    if locale:
        return locale.weekend_start <= date.weekday() <= locale.weekend_end
    else:
        return date.weekday() in (5, 6)  # Sat, Sun


def get_today(tzinfo):
    return datetime.now(tzinfo).date()
