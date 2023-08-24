# autocheck that reserved keywords match across lexer/parser/sources/docs

import re

def die(m):
	print (m)
	exit(1)

def load(n):
	with open(n) as f:
		v = f.read()
	return v

def diff(a, b):
	b = set(b)
	return [aa for aa in a if aa not in b]

# load special tokens from lexer
res = []
with open('sphinxql.l') as f:
	for line in f:
		r = re.match('^"(\w+)"\s+', line)
		if r:
			res.append(r[1])
if not res:
	die('failed to extract resreved keywords from src/sphinxql.l')

# remove those that are handled by parser
r = re.search('ALL_IDENT_LIST(.*?)ALL_IDENT_LIST_END', load('sphinxql.y'), re.MULTILINE + re.DOTALL)
if not r:
	die('failed to extract ident_set_no_option from src/sphinxql.y')
handled = [
	k[4:]
	for k in re.findall('\w+', r[1])
	if k != 'TOK_IDENT' and k[:4] == 'TOK_'
]
res = sorted(diff(res, handled))

# load reserved keywords list from docs
r = re.search('List of reserved keywords.*?```(.*)```', load('../manual/References.md'), re.MULTILINE + re.DOTALL)
if not r:
	die('failed to extract reserved keywords from manual/References.md')
doc = list(re.findall('(\w+)', r[1]))

# load reserved keywords list from sources
r = re.search('dReserved\[\]\s+=\s+\{(.*?)\}', load('schema/schema.cpp'), re.MULTILINE + re.DOTALL)
if not r:
	die('failed to extract reserved keywords from src/schema/schema.cpp')
src = list(re.findall('"(\w+)"', r[1]))


# now report
not_in_docs = sorted(diff(res, doc))
if not_in_docs:
	print ('=== reserved but not in docs: ' + ', '.join(not_in_docs) + '\n')
	print ('.. code-block:: mysql')
	s = ''
	for k in res:
		if len(s) + len(k) >= 60:
			print (s.strip())
			s = ''
		s += f'{k}, '
	if s:
		print (s.strip()[:-1])
	print ('\n')

not_in_src = sorted(diff(res, src))
if not_in_src:
	print ('=== reserved but not in sources: ' + ', '.join(not_in_src) + '\n')
	print ('\tstatic const char * dReserved[] =\n\t{')
	s = ''
	for k in res:
		if len(s) + len(k) >= 80:
			print ('\t\t' + s.strip())
			s = ''
		s += f'"{k}", '
	print ('\t\t' + s + 'NULL\n\t};\n')

docs_not_res = sorted(diff(doc, res))
if docs_not_res:
	print ('=== in docs but not reserved: ' + ', '.join(docs_not_res) + '\n')

src_not_res = sorted(diff(src, res))
if src_not_res:
	print ('=== in sources but not reserved: ' + ', '.join(src_not_res) + '\n')

if not_in_docs or not_in_src or docs_not_res or src_not_res:
	die('got errors')
