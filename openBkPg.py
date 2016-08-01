"""
script to open muliple pages in taree single viewer at once
(sent from John)
"""
import webbrowser

to_judge = [ 'compendiumofcook01blak_0220',
 'cu31924087318436_0239',
 'cu31924085641656_0169',
 'cu31924086713777_0172',
 'centurycookbook00arnoiala_0272',
 'cu31924001803877_0083',
 'cu31924087257873_0478',
 'cu31924085803215_0012',
 'cu31924094662511_0076',
 'cu31924001345507_0082',
'modernpracticalc00broo_0050',
 'cu31924087319681_0203',
 'cu31924001803877_0145',
'mrsrorersphilade00rorerich_0398',
'cu31924003571365_0112',
'cu31924003584061_0226']

for x in to_judge:
    pos = x.rfind('_')
    book = x[:pos]
    page = int(x[pos+1:])
    url = "http://taree.cs.umass.edu:8080/%s/%d" % (book, page)
    webbrowser.open(url)
    