#
# $Id$
#
from __future__ import print_function
from sphinxapi import *
import sys

docs = ['this is my test text to be highlighted','this is another test text to be highlighted']
words = 'test text'
index = 'forum'

opts = {'before_match':'<b>', 'after_match':'</b>', 'chunk_separator':' ... ', 'limit':400, 'around':15}

cl = SphinxClient()
if res := cl.BuildExcerpts(docs, index, words, opts):
	for n, entry in enumerate(res, start=1):
		print ('n=%d, res=%s' % (n, entry))

else:
	print  ('ERROR: %s\n' % cl.GetLastError())

#
# $Id$
#
