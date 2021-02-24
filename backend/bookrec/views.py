from django.shortcuts import render 


# import pyrebase 

# config={ 
# 	apiKey: "Use Your Api Key Here", 
# 	authDomain: "Use Your authDomain Here", 
# 	databaseURL: "Use Your databaseURL Here", 
# 	projectId: "Use Your projectId Here", 
# 	storageBucket: "Use Your storageBucket Here", 
# 	messagingSenderId: "Use Your messagingSenderId Here", 
# 	appId: "Use Your appId Here"
# } 
# firebase=pyrebase.initialize_app(config) 
# authe = firebase.auth() 
# database=firebase.database() 

# def home(request): 
# 	day = database.child('Data').child('Day').get().val() 
# 	id = database.child('Data').child('Id').get().val() 
# 	projectname = database.child('Data').child('Projectname').get().val() 
# 	return render(request,"Home.html",{"day":day,"id":id,"projectname":projectname })
