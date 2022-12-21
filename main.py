from flet import *

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

# RANDOM YOU ID DOCUMENT
import uuid

cred = credentials.Certificate("./serviceAccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


class AppFire(UserControl):
	def __init__(self):
		super().__init__()
		self.name = TextField(label="name")
		self.age = TextField(label="age")
		self.alldata  = Column()

	def getdata(self):
		# GET DATA FROM FIREBASE
		docs = db.collection(u'cities').where(u'capital', u'==', True).stream()
		for doc in docs:
			print(f'{doc.id} => {doc.to_dict()}')
			self.alldata.controls.append(
				ListTile(
         title=Text(f"name {str(doc.to_dict()['name'])}"),
         subtitle=Text(f"age {str(doc.to_dict()['age'])}"),
         trailing=PopupMenuButton(
         icon=icons.MORE_VERT,
         items=[
      PopupMenuItem(text="EDIT"),
      PopupMenuItem(text="DELETE"),
               ],
            ),
           ),

			)
			self.update()
	

	def did_mount(self):
		# CALL FUNCTION GET DATA
		self.getdata()

	def addnewdata(self,e):
		yourandom_id = uuid.uuid1()
		# ADD DATA TO FIRESTORE
		city_ref = db.collection(u'users').document(str(yourandom_id))
		try:
			city_ref.set({
			u'name': self.name.value,
			u'age': self.age.value,
			})
			# IF SUCCESS ADD FIRESTORE THEN PUSH NEW COLUMN
			self.alldata.controls.append(
				ListTile(
         title=Text(f"name {self.name.value}"),
         subtitle=Text(f"age {self.age.value}"),
         trailing=PopupMenuButton(
         icon=icons.MORE_VERT,
         items=[
      PopupMenuItem(text="EDIT"),
      PopupMenuItem(text="DELETE"),
               ],
            ),
           ),

			)
			self.update()
		except e:
			print("YOu error is ", str(e))





	# BUILD YOU FRONT END HERE
	def build(self):
		return Column([
		self.name,
		self.age,
		ElevatedButton("Add",
			bgcolor="blue",
			color="white",
			on_click=self.addnewdata
			),
		self.alldata	

			])





def main(page:Page):
	page.update()
	appfire = AppFire()
	page.add(appfire)

flet.app(target=main)
