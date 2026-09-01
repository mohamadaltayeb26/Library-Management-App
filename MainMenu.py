"""
Main Menu
"""

from Funcs import *

def sys_main_menu():
  """System Main Menu"""
  title = """======== Library Management System ========"""
  options = """
1. Manage Books
2. Manage Members
3. Return and Borrow
4. Exit
"""
  while True:
    print(title)
    print(options)
    while True:
      try:
        index = int(input("[Menu] Choose Option: "))
      except:
        print("Wrong index! Must be integer.")
      else:
        if index in (1, 2, 3, 4):
          if index == 1:
            from Books import books_storage
            books_storage()
            break
          elif index == 2:
            from Members import members_database
            members_database()
            break
          elif index == 3:
            from BorrowAndReturn import borrow_return_menu
            borrow_return_menu()
            break
          else:
            exit()
        else:
          print(f"Index {index} is not defined!")

setup_database()
sys_main_menu()