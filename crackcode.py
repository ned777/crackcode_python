import urllib.request
from html.parser import HTMLParser

url = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"
resp = urllib.request.urlopen(url)
raw = resp.read()
text = raw.decode("utf-8", errors="replace")
print(text[:300])

# TODO 1: make a subclass of HTMLParser
class MyParser(HTMLParser):
    # TODO 2: implement handle_data so it prints non-empty chunks
    pass