import pymongo
from pymongo import MongoClient
from colorama import init, Fore
init(autoreset=True)

cluster = MongoClient("mongodb://localhost:27017")

# Replace test as your database name
db = cluster["test"]
collection = db["test"]

def create(name, first_task):
	collection.insert_one({"_id":name, "tasks":[first_task], "show":True})

def push(name, push_task):
	collection.update_one({"_id":name}, {"$push":{"tasks":push_task}})

def pull(name, pull_task):
	collection.update_one({"_id":name}, {"$pull":{"tasks":pull_task}})

def delete_block(name):
	collection.delete_one({"_id":name})

def delete_all():
	collection.delete_many({})

def display():
	result = collection.find({"show":True}, {"_id":1, "tasks":1})
	for i in list(result):
		print(Fore.MAGENTA + i["_id"].title() + ":")
		i.pop("_id")
		for j in i.values():
			for k in j:
				print(Fore.CYAN + "    |--->" + k)
		print()

def id_list(name):
	result = collection.find({"_id":name}, {"_id":1, "tasks":0, "show":0})
	for i in result:
		if i["_id"] == name:
			return True
		else:
			return False

def main():
	run = True
	while run:
		try:
			print(Fore.YELLOW + "===========================================================================\n")
			choice = int(input("Select the choice [1.Display || 2.Create || 3.Add || 4.Remove || 5.Exit]:~$ "))
			if choice == 1:
				display()
				continue
			
			elif choice == 2:
				name_block = input("name@Enter name of the block:~$ ").strip().lower()
				if id_list(name_block) == True:	raise NameError
				first_task = input("task@Enter the first task:~$ ").lower()
				if len(name_block) == 0 and len(first_task) == 0:	raise NameError
				create(name_block, first_task)
				display()
				continue

			elif choice == 3:
				name_block = input("name@Enter name of the block:~$ ").strip().lower()
				if id_list(name_block) != True:	raise NameError
				range_task = int(input("task@How many task do you want to enter:~$ "))
				if len(name_block) == 0 and len(range_task) == 0:	raise NameError
				for _ in range(1, range_task+1):
					task = input("task@Enter the task:~$ ").lower()
					push(name_block, task)

			elif choice == 4:
				ch = int(input("delete@Enter choice (1.Delete_Task || 2.Delete_Block || 3.Delete_All_Blocks):~$ "))
				if ch == 3:
					delete_all()
					continue
				name_block = input("name@Enter name of the block:~$ ").strip().lower()
				if id_list(name_block) != True:	raise NameError
				elif ch == 1:
					task = input("task@Enter the task to delete:~$ ").lower()
					pull(name_block, task)
				elif ch == 2:
					delete_block(name_block)

			elif choice == 5:
				run = False
				quit()

			else:
				print(Fore.RED + "Please select correct choice!")
			display()
		except:
			print(Fore.RED + "Error !")
main()