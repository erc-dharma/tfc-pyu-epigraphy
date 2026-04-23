from glob import glob
from dharma import tree
files = glob("*.xml")

tbl = {s: s[0].upper() for s in ['k·', 'ṅ·', 'c·', 'ñ·', 't·', 'n·', 'p·', 'm·', 'y·', 'r·', 'l·', 'v·']}

letters = {s[0] for s in tbl}
print(letters)

def process_tree(t):
	for seg in t.find("//seg[@type='graphemic']"):
		seg.prepend("<")
		seg.append(">")
		seg.unwrap()
	t.coalesce()
	strings = t.strings()
	for i, s in enumerate(strings):
		data = s.data
		if data.startswith('·'):
			print(data)
			r = strings[i - 1]
			if r.data[-1] in letters:
				repl = tree.String(r.data[:-1] + r.data[-1].upper())
				r.replace_with(repl)
				strings[i - 1] = repl
				data = data[1:]
		for k, v in tbl.items():
			data = data.replace(k, v)
		import re
		def my_repl(m):
			letter = m.group(1)
			return letter.upper()
		data = re.sub(r"°([a-zA-Zāīū])", my_repl, data)
		data = tree.String(data)
		s.replace_with(data)
		strings[i] = data


for file in glob("*.xml"):
	t = tree.parse(file)
	process_tree(t)
	with open(file, "w") as f:
		f.write(t.xml())
