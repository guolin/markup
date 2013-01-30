# -*- coding: utf-8 -*- 
from bottle import route, run, Bottle
from bottle import jinja2_view as view
import os
import shutil
import markdown

from jinja2 import Environment, FileSystemLoader

class Doc():
	"""
	fullpath  /Users/guolin/root/01_创建新用户/08_asdf.md
	root /Users/guolin/root
	path 01_创建新用户
	name 08_asdf.md
	ext = md

	id 编号
	title asdf
	url asdf.html
	"""
	id = 0
	name = ""

	def __init__(self, fullpath, root):
		# fullpath = fullpath.decode("utf-8")
		self.root = root
		path, filename = os.path.split(fullpath)
		path = path[len(root):]

		self.root = root
		self.fullpath = fullpath
		self.path = path
		self.filename = filename
		self.name, self.ext = os.path.splitext(filename)

		name_list = self.name.split("_")
		if len(name_list) >= 2:
			try:
				self.id = int(name_list[0])
			except:
				self.id = 99
			self.title = name_list[1]
		if len(name_list) == 1:
			self.title= name_list[0]

		self.url = os.path.join(self.path, self.name + ".html")

	def is_file(self):
		return os.path.isfile(self.fullpath) and not self.filename.startswith(".")

	def is_doc(self):
		if self.is_file() and self.ext in [".md",".markdown"]:
			return True
		return False

	def get_content(self):
		f = open(self.fullpath,'r')
		content = f.read()
		f.close()
		return content

	def is_same(self,obj):
		return self.fullpath == obj.fullpath

	def get_html(self):
		return markdown.markdown(self.get_content().decode("utf-8"))


class Folder():

	def __init__(self, path, files, root):
		fullpath = path
		name = os.path.split(fullpath)[1]
		path = fullpath[len(root):]
		deep = len(path.split("/"))

		name_list = name.split("_")
		if len(name_list) >= 2:
			try:
				order = int(name_list[0])
			except:
				order = 99
			title = name_list[1]
		else:
			order = 99 
			title = name_list[0]

		self.fullpath = fullpath
		self.root = root
		self.path = path
		self.name = name
		self.title = title
		self.id = order
		self.deep = deep

		self.url = path

		# 配置文档
		docs = []
		for f in files:
			doc = Doc(os.path.join(fullpath,f), self.root)
			if doc.is_doc():
				docs.append(doc)
		self.docs = docs
		self.sub_folders = []
		

	def get_sub(self, folders):
		if self.sub_folders:
			return self.sub_folders
		for f in folders:
			if f.deep == self.deep+1 and f.path.split("/")[self.deep-1] == self.path.split("/")[self.deep-1]:
				self.sub_folders.append(f)
		return self.sub_folders

	def get_doc(self):
		for d in self.docs:
			if d.title == "index":
				return d
		return None

	def get_docs(self):
		return [x for x in self.docs if x.title != "index"]


def save_to_db(db, path, files):
	name = os.path.split(path)[1]
	if name in ["static","templates"]:
		return None
	c = Folder(path, files, doc_root)
	db["folders"].append(c)
	db["docs"] = db["docs"] + c.docs


# 配置文件
absolute_root = u"/Users/guolin/Workspace/help/src"
doc_root = os.path.join(absolute_root, "root")
www_root = os.path.join(absolute_root, "www")

# 临时数据库
db = {"folders":[], "docs":[], "cached":False}


# hack Bottle
def get_db(self):
	if not self.db.get("cached", False):
		os.path.walk(doc_root, save_to_db, self.db)
		self.db['cached'] = True
	return self.db
Bottle.get_db = get_db

app = Bottle()
app.db = db

@app.route('/')
@view("post.html")
def index():
	db = app.get_db()
	folders = db['folders']
	docs = db['docs']
	root_deep = folders[0].deep
	file_root = db['root']

	return {'db':db,
			'folders':folders,
			'docs':docs ,
			'root_deep':root_deep,
			'file_root':file_root}


def sync_www():

	# set the root 
	db = app.get_db()
	docs = db['docs']
	folders = db['folders']
	root_deep = folders[0].deep


	# copy template
	doc_templates_dir = os.path.join(doc_root, "templates")
	templates_dir = os.path.join(absolute_root, "templates")
	if os.path.exists(doc_templates_dir):
		if os.path.exists(templates_dir):
			shutil.rmtree(templates_dir)
		shutil.copytree(doc_templates_dir, templates_dir)

	# copy static
	for folder in folders:
		if os.path.exists(os.path.join(folder.fullpath, "static")):
			www_path = os.path.join(www_root ,folder.path.strip("/").strip("\\"), "static")
			if os.path.exists(www_path):
				shutil.rmtree(www_path)
			shutil.copytree(os.path.join(folder.fullpath, "static"), www_path)


	# generic doc
	env = Environment(loader = FileSystemLoader("./"))
	template = env.get_template("templates/post.html")

	for doc in docs:
		t = template.render({"folders":folders, "current_doc":doc})
		fullpath = os.path.join(www_root, doc.url.strip("/").strip("\\"))
		fullroot = os.path.join(www_root, doc.path.strip("/").strip("\\"))
		if not os.path.exists(fullroot):
			os.makedirs(fullroot)
		f = open(fullpath,"w")
		f.write(t.encode("utf-8"))
		f.close()

sync_www()




# run(app, host='localhost', port=8080, debug=True)







