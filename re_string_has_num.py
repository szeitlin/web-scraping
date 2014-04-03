__author__ = 'szeitlin'

#try using a regex to filter strings more quickly

import re

def re_string_has_num(word):
    """
    string -> bool

    if string contains a number, return true

    >>>unique_hits = ["http://events.stanford.edu/xml/rss.xml", "http://events.stanford.edu/events/408/40839",
                   "http://events.stanford.edu/eventlist.ics", "http://events.stanford.edu/events/433/43373"]
    >>>re_string_has_num(unique_hits)
    False, True, False, True
    """
    p = re.compile("[0-9]+")#[0-9] if any digit or any number of digits

    q = p.search(word)
    if q:
        return True
    else:
        return False


re_string_has_num("http://events.stanford.edu/xml/rss.xml")
re_string_has_num("http://events.stanford.edu/events/408/40839")
re_string_has_num("http://events.stanford.edu/eventlist.ics")
re_string_has_num("http://events.stanford.edu/events/433/43373")
