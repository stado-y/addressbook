"""Simple phonebook, which i made at the direction from the book 'A byte of Python'

store, view, edit, search and deletion of contacts"""
from os import system
from time import sleep
import pickle
from pyfiglet import Figlet
figlet = Figlet(font='roman')


class People:

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def view(self):
        print(f'    Name:  {self.name}\n'
              f'    Phone: {self.phone}')


#  storage for saving data
storage = {}

# contact list
namelist = []

dumpfile = 'save.p'


#  fun for saving changes
def pickledump():
    with open(dumpfile, 'wb')as file:
        pickle.dump(storage, file)

def pickleload():
    global storage
    with open(dumpfile, 'rb') as file:
        storage = pickle.load(file)


#  just prints info after operations with contacts
def contact_printer(name, operation):
    print(f'    Contact {name} {operation}')


#  add new contact
def additem(name, phone):
    operation = 'created'
    storage.setdefault(name, People(name, phone))
    namelist.append(name)
    namelist.sort()
    pickledump()
    contact_printer(name, operation)


#  delete contact
def delitem(name):
    operation = 'deleted'
    print('''   Are you sure?
        1 - Yes
        2 - No''')
    inputter = inputgetter()
    if inputter == '1':
        storage.pop(name)
        namelist.remove(name)
        contact_printer(name, operation)
        pickledump()
        sleep(2)
        Screen.main()
    elif inputter == '2':
        sleep(1)
        Screen.edit(name)
    else:
        print('    invalid input, try again')
        delitem(name)


#  edit contact
def edititem(oldname, name, phone):
    operation = 'updated'
    name = name.title()
    storage.pop(oldname)
    namelist.remove(oldname)
    storage.setdefault(name, People(name, phone))
    pickledump()
    namelist.append(name)
    namelist.sort()
    contact_printer(name, operation)


#  search contact
def searchitem(name):
    searchresult = []
    for i in namelist:
        if i.lower().startswith(name.lower()):
            searchresult.append(i)
    if len(searchresult) != 0:
        return searchresult
    else:
        contact_printer(name, 'not found')
        return False


#  fully rerfeshing of the contact list
def namelistrefresh():
    global namelist
    for i in storage.keys():
        namelist.append(i)
    namelist.sort()


#  fun for input
def inputgetter():
    choice = input('    input: ')
    return choice


#  cleaning the screen
def cleanscreen():
    _ = system('cls')

#  check for existing contact  
def existcheck(name):
    if name.title() in namelist:
        contact_printer(name, 'already exists')
        return True
    else:
        return False


class Screen:
    @staticmethod
    def main():
        cleanscreen()
        print('''   Addressbook
        
            1 - Contacts list
            2 - Search for contact by name
            3 - Add contact''')
        inputted = inputgetter()
        if inputted == '1':
            Screen.list(namelist)
        elif inputted == '2':
            Screen.search()
        elif inputted == '3':
            Screen.add()
        else:
            print('Invalid input, try again')
            sleep(2)
            Screen.main()

    @staticmethod
    def list(somelist):
        cleanscreen()
        print('''   Contact list
        
        To open contact - input it\'s number. To return to the Main screen - input m''')
        for i in somelist:
            print(f'            {somelist.index(i) + 1} - {i}')
        inputted = inputgetter()

        def tryint():
            try:
                if int(inputted) in range(1, (len(somelist) + 1)):
                    return True
                else:
                    return False

            except ValueError:
                return False

        if inputted == 'm':
            Screen.main()
        elif tryint():
            Screen.contact(somelist[int(inputted) - 1])
        else:
            print('    Invalid input, try again')
            sleep(2)
            Screen.list(somelist)

    @staticmethod
    def contact(name):
        cleanscreen()
        print('''   Contact screen
        
            1 - Edit / Delete
            m - Main screen''')
        storage[name].view()
        inputter = inputgetter()
        if inputter == '1':
            Screen.edit(name)
        elif inputter == 'm':
            Screen.main()
        else:
            print('    Invalid input, try again')
            sleep(2)
            Screen.contact(name)

    @staticmethod
    def search():
        cleanscreen()
        print('''   Search for contacts
        
            Input contact name
            To return to the Main screen - input 1''')
        inputted = inputgetter()
        if inputted == '1':
            Screen.main()
        else:
            if searchitem(inputted):
                names = searchitem(inputted)
                if len(names) == 1:
                    contact_printer(names[0], 'was found')
                    sleep(2)
                    Screen.contact(names[0])
                else:
                    Screen.list(names)
            else:
                sleep(2)
                Screen.search()

    @staticmethod
    def add():
        cleanscreen()
        print('''   Adding new contact
            
            Input name and phone
            e.g: Vasya +38-000-000-00-00
            To return to main screen - input m''')
        inputter = inputgetter()
        if inputter == 'm':
            Screen.main()
        else:
            if ' ' in inputter:
                new = inputter.rsplit(' ', 1)
                if not existcheck(new[0]):
                    additem(new[0].title(), new[1])
                    sleep(2)
                    Screen.contact(new[0].title())
                else:
                    sleep(2)
                    Screen.add()
            else:
                print('    Invalid input, try again')
                sleep(2)
                Screen.add()

    @staticmethod
    def edit(name):
        cleanscreen()
        print('''   Edit contact
        
            1 - Edit name
            2 - Edit phone
            3 - Delete
            m - Return to Main screen''')
        storage[name].view()
        inputted = inputgetter()
        if inputted == 'm':
            Screen.main()
        elif inputted == '1':
            cleanscreen()
            print('''   Edit contact

                m - Return to Main screen''')
            print('    Input new name for contact')
            newname = inputgetter()
            if newname == 'm':
                Screen.main()
            elif not existcheck(newname):
                edititem(name, newname, storage[name].phone)
                sleep(2)
                Screen.contact(newname.title())
            else:
                sleep(2)
                Screen.edit(name)
        elif inputted == '2':
            cleanscreen()
            print('''   Edit contact

                m - Return to Main screen''')
            print('''    Input new phone for contact
                in format: +38-000-000-00-00''')
            newphone = inputgetter()
            if newphone == 'm':
                Screen.main()
            edititem(name, name, newphone)
            sleep(2)
            Screen.contact(name)
        elif inputted == '3':
            delitem(name)
        else:
            print('    Invalid input, try again')
            sleep(2)
            Screen.edit()


def main():
    global storage
    global dumpfile

    try:
        pickleload()
    except FileNotFoundError:
        with open('save.p', 'wb') as f:
            pass


    namelistrefresh()
    cleanscreen()
    print(figlet.renderText('Address book v1'))
    sleep(2)
    Screen.main()


if __name__ == '__main__':
    main()
