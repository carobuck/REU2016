"""
script to open muliple pages in taree single viewer at once
(sent from John)
"""
import webbrowser

to_judge = [ 'newworldsfaircoo00port_0417',
 'memoirsofliterar01lite_0072',
'cu31924001742083_0034',
 'cu31924090155767_0425',
'candymakingathom00wrig_0076',
 'mathematicalcon00laffgoog_0062',
'cu31924001742083_0016']

for x in to_judge:
    pos = x.rfind('_')
    book = x[:pos]
    page = int(x[pos+1:])
    url = "http://taree.cs.umass.edu:8080/%s/%d" % (book, page)
    webbrowser.open(url)
    