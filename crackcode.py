from urllib.request import urlopen
from html.parser import HTMLParser

URL = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"

class SimpleTableParser(HTMLParser):
    """
    Minimal table parser:
    - collects tables -> rows -> cells (strings)
    """
    def __init__(self):
        super().__init__()
        self.tables = []
        self._in_table = False
        self._in_row = False
        self._in_cell = False
        self._cell = []
        self._row = []
        self._table = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._in_table = True
            self._table = []
        elif tag == "tr" and self._in_table:
            self._in_row = True
            self._row = []
        elif tag in ("td", "th") and self._in_row:
            self._in_cell = True
            self._cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._in_cell:
            self._in_cell = False
            text = "".join(self._cell).strip()
            self._row.append(text)
        elif tag == "tr" and self._in_row:
            self._in_row = False
            if self._row:
                self._table.append(self._row)
        elif tag == "table" and self._in_table:
            self._in_table = False
            if self._table:
                self.tables.append(self._table)

    def handle_data(self, data):
        if self._in_cell:
            self._cell.append(data)

def fetch_html(url: str) -> str:
    # adding ?embedded=true often simplifies google's published markup
    u = url if "embedded=true" in url else (url + ("&embedded=true" if "?" in url else "?embedded=true"))
    with urlopen(u) as resp:
        return resp.read().decode("utf-8", errors="replace")

def to_points(table):
    """
    Convert table rows into (x, ch, y) triples.
    Assumes header row with something like: x-coordinate | Character | y-coordinate
    """
    points = []
    for row in table[1:]:  # skip header
        if len(row) < 3: 
            continue
        try:
            x = int(row[0])
            ch = row[1][:1] if row[1] else " "
            y = int(row[2])
            points.append((x, ch, y))
        except ValueError:
            # skip lines that aren't numeric where expected
            continue
    return points

def build_and_print(points):
    if not points:
        print("[no points found]")
        return
    max_x = max(x for x, _, _ in points)
    max_y = max(y for _, _, y in points)
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, ch, y in points:
        if 0 <= y <= max_y and 0 <= x <= max_x:
            grid[y][x] = ch
    for row in grid:
        print("".join(row))

def main():
    html = fetch_html(URL)
    parser = SimpleTableParser()
    parser.feed(html)

    if not parser.tables:
        print("no tables found — is the doc published?")
        return

    # take the first non-empty table that looks like 3 columns
    table = next((t for t in parser.tables if len(t) > 1 and len(t[0]) >= 3), parser.tables[0])
    points = to_points(table)
    build_and_print(points)

if __name__ == "__main__":
    main()
