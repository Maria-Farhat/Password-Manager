from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():

	letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

	password_letters = [choice(letters) for _ in range(randint(8, 10))]
	password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
	password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

	password_list = password_letters + password_symbols + password_numbers
	shuffle(password_list)

	passw = "".join(password_list)
	password_entry.insert(0,passw)
	pyperclip.copy(passw)

# -------------------------- SAVE PASSWORD ----------------------------- #

def save():
	email = email_entry.get()
	password = password_entry.get()
	website = website_entry.get().title()
	new_data = {
		website: {
			"email": email,
			"password": password,
		}
	}
	if len(email) == 0 or len(password) == 0 or len(website) == 0:
		messagebox.showwarning(title='Oops', message='Please do not leave any field empty')

	else:
		try:
			with open('data.json','r') as file:
				# Reading old data
				data = json.load(file)
		except FileNotFoundError:
			with open('data.json','w') as file:
				json.dump(new_data, file, indent=4)
		else:
			# Updating old data with new data
			data.update(new_data)
			with open('data.json','w') as file:
				# Saving updated data
				json.dump(data, file, indent=4)

		finally:
			website_entry.delete(0, END)
			password_entry.delete(0, END)
			website_entry.focus()

#------------------------- SEARCH FROM DATA ---------------------------- #

def find_password():
	website_name = website_entry.get().title()
	try:
		with open('data.json') as file:
			data = json.load(file)
	except FileNotFoundError:
		messagebox.showwarning(title='Error', message='No Data File Found')
		return
	else:
		if website_name in data:
			searched_email = data[website_name]["email"]
			searched_password = data[website_name]["password"]
			messagebox.showinfo(title=website_name, message=f'Email: {searched_email}\nPassword: {searched_password}')
		else:
			messagebox.showinfo(title='Error', message=f'No Details for {website_name}')

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx = 50, pady = 20, bg = "white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:", bg="white")
website_label.grid(row=1, column=0)

email_username = Label(text="Email/Username:", bg="white")
email_username.grid(row=2, column=0)

password_label = Label(text="Password:", bg="white")
password_label.grid(row=3, column=0)

add = Button(text="Add", bg="white", fg="black", width=36, command=save)
add.grid(row=4, column=1, columnspan=2)

generate = Button(text="Generate ", bg="white", fg="black", command=generate_password)
generate.grid(row=3, column=2, columnspan=2)

search_button = Button(text='Search', bg='white', fg='black', activebackground='blue', command=find_password)
search_button.grid(row=1, column=2, sticky='ew')

website_entry = Entry(width=32)
website_entry.grid(row=1, column=1,columnspan=2, sticky='w')
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky='ew')
email_entry.insert(0, "username@email.com")

password_entry = Entry(width=32)
password_entry.grid(row=3, column=1,columnspan=2, sticky='w')


window.mainloop()