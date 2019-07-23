import pyrebase
from firebase.firebase import FirebaseApplication
import json
from flask import Flask, request, jsonify, render_template
from github import Github, GithubException

app = Flask(__name__)
#http://serveo.net/
config = {
  "apiKey": "AIzaSyAvbcA36dCFDGs8r8OpvdfLVl-Unh9CCT4",
    "authDomain": "commuteapp-90b42.firebaseapp.com",
    "databaseURL": "https://commuteapp-90b42.firebaseio.com",
    "projectId": "commuteapp-90b42",
    "storageBucket": "commuteapp-90b42.appspot.com",
	"serviceAccount": "./commuteapp-90b42-firebase-adminsdk-ct2h6-926c224be6.json"
}

firebase = pyrebase.initialize_app(config)

@app.route("/", methods = ['GET', 'POST'])
def renderHomePage():
	return render_template("HomePage.html")

@app.route("/renderLoginAccessPage", methods = ['GET', 'POST'])
def renderLoginAccessPage():
	if request.method == 'POST':
		data = request.form.to_dict()
		print("JSON data: ", data)
		if data.get("username") is not None:
			g = Github(data.get("username"), data.get("password"))
		else:
			try:
				g = Github(data.get("accessToken"))
			except GithubException.BadCredentialsException as e:
				return render_template("Login_AccessToken.html")
			
		print(g)
		user = g.get_user()
		print(user)
		try:
			for repo in g.get_user().get_repos():
				print(repo.name)
		except GithubException as e:
			return render_template("Login_AccessToken.html")
		auth = True
		return render_template('Landing_Page.html')
	return render_template("Login_AccessToken.html")

# cc052069cddccbaac3fbdbd9198614282109ffea accesstoken
@app.route("/authenticate", methods = ['GET','POST'])
def authenticate():
	if request.method == 'POST':
		data = request.form.to_dict()
		print("JSON data: ", data)
		# print("first ", data)
		# data = json.loads(data)
		# print("he;llo ",data)
		if data.get("username") is not None:
			g = Github(data.get("username"), data.get("password"))
		else:
			try:
				g = Github(data.get("accessToken"))
			except GithubException.BadCredentialsException as e:
				return render_template("login.html")
			
		print(g)
		user = g.get_user()
		print(user)
		try:
			for repo in g.get_user().get_repos():
				print(repo.name)
		except GithubException as e:
			return render_template("login.html")
		auth = True

		return render_template('Landing_Page.html')
	return render_template('login.html')

@app.route("/create_repo", methods=['GET', 'POST'])
def createRepo():
	call = True
	if request.method == 'POST':
		if call is True:
			call = False
			requestData = request.form.to_dict()
			print(requestData)
			print(requestData.get('template_name'))
			return render_template('createPage.html', mystring = requestData.get('template_name'))
		else:
			if requestData.get("username") is not None:
				g = Github(requestData.get("username"), requestData.get("password"))
			else:
				g = Github(requestData.get("accessToken"))
			try:
				g = Github(requestData.get("username"), requestData.get("password"))
				user = g.get_user()
				repo = user.create_repo(requestData.get("repoName"))
				print(repo)
			except:
				return "Hey !! Awesome your repository is created !!! Naaaaaaa I am kidding its already there !!! Please create a new one"

			return "Hey !! Awesome your repository is created !!!"
	return render_template('createTemplate.html')

@app.route("/create_template", methods = ['POST'])
def createTemplate():
	PostData = request.json
	templateAttr = PostData.get("struct")
	db = firebase.database()
	db.child(PostData.get("tempName")).set(templateAttr)
	return "The necessary template is created"

@app.route("/create_files", methods = ['POST'])
def createFiles():
	PostData = request.json
	templateAttr = PostData.get("struct")
	if PostData.get("username") is not None:
		g = Github(PostData.get("username"), PostData.get("password"))
	else:
		g = Github(PostData.get("accessToken"))
	user = g.get_user()
	repo = g.get_repo("Shreyasgujjar/example0")
	depth = 1
	try:
		# for item in templateAttr:
		# 	print(item + " ")
		# 	if type(templateAttr.get(item)) is dict:
		# 		itemsInsideFolder = templateAttr.get(item)
		# 		for items in itemsInsideFolder:
		# 			if type(templateAttr.get(items)) is str:
		# 				repo.create_file(item+"/"+itemsInsideFolder.get(items), "test", "")
		# 				print("file " + itemsInsideFolder.get(items) + " is created")
		# 			else:
		# 				depth2 = itemsInsideFolder.get(items)
		# 				for item2 in depth2:
		# 					if type(itemsInsideFolder.get(item2)) is str:
		# 						repo.create_file(item+"/"+itemsInsideFolder.get(items)+"/"+depth2.get(item2), "test", "")
		# 						print("file " + itemsInsideFolder.get(items) + " is created")
		# 		print("------------------Folder is created-----------------------")
		# 	else:
		# 		repo.create_file(templateAttr.get(item), "test", "test")
		# 		print("file " + templateAttr.get(item) + " is created")
			
		################################################
				
		for item in templateAttr:
			if type(templateAttr.get(item)) is dict:
				
				f1(item,templateAttr.get(item),repo)

			else:
				repo.create_file(templateAttr.get(item), "test", "test")
				print("file " + templateAttr.get(item) + " is created")

		print("-"*10)
		print("peace")


		################################################
	except GithubException as e:
		return "There was some error creating the files " + str(e)
	db = firebase.database()
	db.child(PostData.get("repoName")).set(templateAttr)
	return "The necessary file is created"


def removepath(path):
	print("path v = " + path)
	ind = path.rfind("/")
	if "/" not in path:
		return path
	path = path[:ind]
	return path
def f1(path,item,repo):
	for i in item:
		if type(item.get(i)) is str:
			repo.create_file(path+"/"+item.get(i), "test", "test")
			print("file " + item.get(i) + " is created")
		else:
			f1(path+"/"+i,item.get(i),repo)
			path=removepath(path)

# @app.context_processor
# def f2(items):
# 	for i in items:
# 		if type(items.get(i)) is str:
# 			return(items.get(i))
# 		else:
# 			f2(items.get(i))



#sdbvjns

# def createFoldersAndFiles(path):
# 	for item in templateAttr:
# 		print(item + " ")
# 		if type(templateAttr.get(item)) is dict:
# 			itemsInsideFolder = templateAttr.get(item)
# 			for items in itemsInsideFolder:
# 				if type(templateAttr.get(items)) is str:
# 					repo.create_file(item+"/"+itemsInsideFolder.get(items), "test", "")
# 					print("file " + itemsInsideFolder.get(items) + " is created")
# 			print("------------------Folder is created-----------------------")
# 		else:
# 			repo.create_file(templateAttr.get(item), "test", "test")
# 			print("file " + templateAttr.get(item) + " is created")
# 		print("-"*10)

@app.route("/retrieve", methods=['GET'])
def retrieveData():
	firebase = FirebaseApplication("https://commuteapp-90b42.firebaseio.com")
	retrieveData = firebase.get("/template", None)
	print(dict(retrieveData))
	retrieveData = jsonify(retrieveData)
	print(type(retrieveData))

	return retrieveData
	# return render_template("datadisplay.html",data = firebase.get("/example0", None))

# shreyasshivajirao.pythonanywhere.com.

if __name__ == '__main__':
	auth = False
	app.run(debug = True)