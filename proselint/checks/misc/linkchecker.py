# -*- coding: utf-8 -*-
"""MSC404: Checks that links are viable.

---
layout:     post
error_code: MSC404
source:     SublimeLinter-annotations
source_url: http://bit.ly/16Q7H41
title:      broken links
date:       2014-06-10 12:31:19
categories: writing
---

Check that links are not not broken.

"""
from proselint.tools import memoize
import re
import urllib2


@memoize
def check(text):
    """Check the text."""
    err = "ANN100"
    msg = u"Broken link: {}"

    r = ur"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)
        (?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|
        (\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d
        \u2018\u2019]))"""

    regex = re.compile(r, re.U)

    errors = []
    for m in re.finditer(regex, text):
        url = m.group(0).strip()

        if is_broken_link(url):
            errors.append((m.start()+1, m.end(), err, msg.format(url)))

    return errors


@memoize
def is_broken_link(url):
    print url
    try:
        urllib2.urlopen(url)
        return False
    except urllib2.URLError:
        return True