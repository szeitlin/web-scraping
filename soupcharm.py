__author__ = 'szeitlin'

## an application that when given a URL, returns 10 other URLs on the same site (root domain) that also
## contain activities

from bs4 import BeautifulSoup
import sys
import urllib2
import urlparse


global address

linklist = ["http://calendar.boston.com/lowell_ma/events/show/274127485-mrt-presents-shakespeares-will",
    "http://www.sfmoma.org/exhib_events/exhibitions/513",
    "http://www.workshopsf.org/?page_id=140&id=1328",
    "http://events.stanford.edu/events/353/35309/"]

def get_roothost(link):
    """url list -> root domain/hostname

    >>>get_root_host("http://pythonchallenge.com/pc/def/linkedlist.php?nothing=12345')
       pythonchallenge.com
    """

    roothost = "http://" + urlparse.urlparse(link).hostname #returns the "root domain" of the url

    pagename = roothost

    return roothost, pagename


def read_page(pagename):
    """ url -> page source -> list of all urls in page

    >>> read_page('http://pythonchallenge.com/pc/def/linkedlist.php?nothing=12345')
    and the next nothing is 44827

    """

    response = urllib2.urlopen(pagename)
    j = response.read()

    soup = BeautifulSoup(j)  #use this to find all the urls in the page
    taglist = []

    for tag in soup.findAll('a', href=True):
        taglist.append(tag['href'])

    return taglist


def find_event_strings(taglist):
    """
       start with things that explicitly say "event"
       if that works, consider adding "music" "movies" "Thingstodo" etc.

       >>> "http://calendar.boston.com/lowell_ma/events/show/274127485-mrt-presents-shakespeares-will"
       http://www.boston.com/thingstodo/
       """
   rawhitlist = []

    for tag in taglist:
        if "search?" in tag:
            continue
        if "event" in tag:
            rawhitlist.append(tag)
        elif "?page_id=" in tag:
            rawhitlist.append(tag)
        elif "calendar" in tag.lower():
            rawhitlist.append(tag)
        elif "tickets" in tag.lower():
            rawhitlist.append(tag)

    return rawhitlist

def remove_duplicates(rawhitlist):
    """identify strings that appear more than once in the rawhitlist, and delete them.
    http:///boston_ma/events/show/368924700-toronto-blue-jays-vs-boston-red-sox
    http:///boston_ma/events/show/368924700-toronto-blue-jays-vs-boston-red-sox
    http:///boston_ma/events/show/368924700-toronto-blue-jays-vs-boston-red-sox
    http:///boston_ma/events/show/368924712-baltimore-orioles-vs-boston-red-sox
    http:///boston_ma/events/show/368924712-baltimore-orioles-vs-boston-red-sox
    http:///boston_ma/events/show/368924712-baltimore-orioles-vs-boston-red-sox

    returns
    http:///boston_ma/events/show/368924700-toronto-blue-jays-vs-boston-red-sox
    http:///boston_ma/events/show/368924712-baltimore-orioles-vs-boston-red-sox
    """

    unique_hits = []

    #would it be faster to convert to a dictionary?

    for item in rawhitlist:
        #might be slow but try it this way first - just write out a new list
        if item not in unique_hits:
            unique_hits.append(item)

    return unique_hits

def check_other():
    """ ask at the command prompt for other urls to search"""

    global link

    plan_c = raw_input("Would you like to try another url? (y/n)")
    if plan_c =="y":
        link = raw_input("Ok, what's the new url, e.g. http://sfsymphony.org? ")
        roothost, pagename = get_roothost(link)
        find_events_at_domain(roothost, pagename)

def string_has_num(word):
    """helper function to check whether string contains any numbers. returns true if numbers are present,
     false otherwise.

     #may be faster to replace this with a regex later?

    string --> bool

    >>> string_has_num("abcdef")
    False
    >>> string_has_num("12345")
    True
    >>> string_has_num("abc/1234")
    True

    """
    flag = False

    for char in word:
        if char.isdigit():
            flag = True
            break
    return flag

def move_nonspecifics(unique_hits):
    """ identify strings that are links to categories rather than specific events
    http:///boston_ma/events/community

    initial logic: if there are no numbers in the string

    >>>  move_nonspecifics(["http://events.stanford.edu/xml/rss.xml", "http://events.stanford.edu/events/408/40839",
                   "http://events.stanford.edu/eventlist.ics", "http://events.stanford.edu/events/433/43373"])

    returns
    unique_hits = ["http://events.stanford.edu/events/408/40839," "http://events.stanford.edu/events/433/43373"]
    categories = ["http://events.stanford.edu/xml/rss.xml", "http://events.stanford.edu/eventlist.ics"]

    """

    categories = []

    for item in unique_hits[:]:  #makes a complete copy of unique_hits to avoid modifying it as you go
        if string_has_num(item) == True: #if there is a number, assume it's a specific event, keep it in "unique hits"
            continue                #do the next item in the for loop
        else:
            categories.append(item) #if there are no numbers, assume it is a category, move it to the new list
            unique_hits.remove(item)

    return categories

def make_pretty(unique_hits, roothost, howmany):
    """ return the final hitlist on separate lines with "http://" added if it's not there"""

    for item in unique_hits[:howmany]:
        if roothost not in item:
            item = roothost + item
        if "http://" not in item:
            item = "http://" + item
        print item + "\n"

def return_only_ten():
    """ make this optional - to truncate the number of hits you return from a given domain"""

    # if "-g" in sys.argv:
    #     howmany = len(unique_hits)   #if greedy flag is turned on, get all the unique events
    # else:
    #could also ask at the prompt about this

    howmany = 10                #default

    return howmany

def find_events_at_domain(roothost, pagename):
    """ url -> domain homepage
      run find_event_strings from there

    >>> "http://calendar.boston.com/lowell_ma/events/show/274127485-mrt-presents-shakespeares-will"
    http://calendar.boston.com

    """
    global link

    taglist = read_page(pagename)
    rawhitlist = find_event_strings(taglist)
    unique_hits = remove_duplicates(rawhitlist)

    if len(unique_hits) < 10:    #check whether there are any hits, and if not, search the page itself
        pagename = link
        taglist = read_page(pagename)
        rawhitlist = find_event_strings(taglist)
        unique_hits = remove_duplicates(rawhitlist)

    categories = move_nonspecifics(unique_hits) #this is very slow

    if len(unique_hits) < 10:
        rawhitlist = find_event_strings(categories)
        unique_hits += remove_duplicates(rawhitlist)
        move_nonspecifics(unique_hits)

    howmany = return_only_ten()

    make_pretty(unique_hits, roothost, howmany)

link = None

for address in linklist:
    link = address
    roothost, pagename = get_roothost(link)
    find_events_at_domain(roothost, pagename)

check_other()

