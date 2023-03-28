import requests
from lxml import etree
import re

with open('release-groups.txt', 'r') as f:
    orig_set = set(f.read().split('\n'))

url = 'http://torrentinvites.org/f23/internal-encoders-groups-private-tracker-62009/'
r = requests.get(url)
page = etree.HTML(r.text)
gp_cells = page.xpath('//table[@class="cms_table_grid"]//tr/td[position()=2]')

split_pat = re.compile(r'(?:,|&| and )')
strip_pat = re.compile(r'(?:^(?:\s*[,()]*\s*)|\s*\(inactive\)\s*$|\s*[,()]*\s*$|None!?|all encodes are internal|\s*Team\s*$)')

gp_set = set()
for cell in gp_cells:
    for txt in cell.itertext():
        for g_raw in re.split(split_pat, txt):
            g = re.sub(strip_pat, '', g_raw)
            if g:
                gp_set.add(g)

new_set = orig_set.union(gp_set)
with open('new-groups.txt', 'w') as f:
    f.write('\n'.join(sorted(list(new_set), key=str.lower)))
