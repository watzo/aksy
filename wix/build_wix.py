from lxml import etree
import os, os.path

dist_dir = "../dist" 
build_dir = "../build" 

def find_files(base, sub, ext):
	d = os.path.join(base, sub)
	for f in os.listdir(d):
		if f.endswith(ext):
			yield os.path.join(d, f)

def create_file(comp, path):
	print path
	e = etree.Element("File")
	name = os.path.basename(path)
	e.set('Id', name.replace('-', '_'))
	e.set('Name', name)
	e.set('Source', path)
	return e

doc = etree.parse("aksy-installer.in.wxs")
comps = doc.xpath("/w:Wix/w:Product/w:Directory/w:Directory//w:Component", 
		{'w': 'http://schemas.microsoft.com/wix/2006/wi'})

for c in comps:
	c_id = c.get('Id')
	if c_id == 'Scripts':
		for f in find_files(build_dir, 'bdist.win32/wininst/SCRIPTS', ".py"):
			c.append(create_file(c, f))
	if c_id == 'aksy':
		for f in find_files(dist_dir, '', ".egg"):
			c.append(create_file(c, f))



doc.write('aksy-installer.wxs')
