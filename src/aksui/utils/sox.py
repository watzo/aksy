import os.path, os

def convert(filename):
	if os.path.exists(filename):
		[path, fileend] = os.path.split(filename)
		[name, ext] = os.path.splitext(fileend)
		src = filename
		dest = path + "\\" + name + "_rs" + ext
		cmd = "sox \"" + src + "\" -r 44100 \"" + dest + "\" resample -ql" 
		print cmd
		os.system(cmd)
		return dest
	else:
		return None
	# run cmd
