## 程序逻辑：

将root目录下的markdown文件转化成www目录下的HTML文件。其中，

* static目录用来存放静态文件，如图片。
* Template目录用来存放模版。



## 目录结构：

根目录：

* markup.py 程序文件
* www: 目录：发布目录，前端web服务器（例如nginx）直接指向这个目录就可以
* root目录：用来存放文档+静态文件+模板
	* templates 存放模版，目前仅有post.html 模版语言采用jinja2
	* static 静态文件夹，需要发布的图片等静态文件需要放到这个目录下。

## 如何转化文件：

运行一次markup.py文件就可以。

运行前需要配置python环境, 由于各个操作系统不一致，所以安装python和pip的步骤我就不写了，安装完成pip以后，运行：

	pip install Jinja2==2.6
	pip install Markdown==2.2.1
	pip install bottle==0.11.4
	
执行markup.py的过程也很简单：

	python markup.py
	
没有报错就算成功了。

## 必要的配置
需要在markup.py中配置文件的绝对位置，例如：

	# 配置文件
	absolute_root = u"/Users/guolin/Workspace/help/src"
	doc_root = os.path.join(absolute_root, "root")
	www_root = os.path.join(absolute_root, "www")


## 什么是markdown？

通过在文本文件中添加简答的标记来实现格式化的标记语言，下载一个markdown软件10分钟绝对能学会：

软件：http://www.appinn.com/markdown-tools/

	例如:
	# 标题一，则代表HTML中的<h1>标题一</h1>。 
	## 标题二，则代表HTML中的<H2>标题二</h2>


