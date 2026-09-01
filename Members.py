"""
Members Section
"""

from Funcs import *

def members_database():
  """Members Database"""
  db, cr = connect_database()
  title = """
====================
  Members Database
===================="""
  syntax = "(ID | Name | Phone)"
  options = "1. Add | 2. Edit | 3. Delete | 4. Search | 5. Back"
  while True:
    print(title)
    print(syntax)
    print("=" * (len(options) - 20))
    is_members = check_for_members()
    if not is_members:
      print("---- Members list is empty ----")
    else:
      cr.execute("SELECT * FROM members")
      members = cr.fetchall()
      for member in members:
        result = f"({member[0]} | {member[1]} | {member[2]})"
        print(result)
    print("=" * (len(options) - 20))
    print(options)
    print("=" * (len(options) - 20))
    while True:
      try:
        index = int(input("[Members] Choose Option: "))
      except:
        print("Wrong index! Must be integer.")
      else:
        if index in (1, 2, 3, 4, 5):
          if index == 1:
            add_member()
            break
          elif index == 2:
            edit_member_menu(is_members)
            break
          elif index == 3:
            delete_member(is_members)
            break
          elif index == 4:
            search_member(is_members)
            break
          else:
            db.close()
            return
        else:
          print(f"Index {index} is not defined!")

def add_member():
  db, cr = connect_database()
  title = "======== Add Member ========"
  print(title)
  member_data = []
  while True:
    full_name = input("Enter Full Name: ").strip().title()
    checked_name = check_input(full_name)
    if not checked_name:
      continue
    while True:
      phone_number = input("Enter Phone Number: ").strip()
      if not phone_number.isdigit():
        print("Phone number must be all digits!")
        continue
      break
    break
  member_data.append(checked_name)
  member_data.append(phone_number)
  cr.execute("INSERT INTO members(name, phone) VALUES(?, ?)", member_data)
  db.commit()
  print(f'Member "{member_data[0]}" added seccesfully!')
  input("Press Enter to return")

def edit_member_menu(is_members: bool):
  title = "======== Edit Member ========"
  options = "1. Name | 2. Phone Number | 3. Back"
  print(title)
  if not is_members:
    print("There are no members to edit.")
    cnfrm = confirmation("Would you like to add amember now? (y/n) ")
    if cnfrm:
      add_member()
      return
    else:
      return
  else:
    print("What do you want to edit?")
    print("=" * len(options))
    print(options)
    print("=" * len(options))
    while True:
      try:
        index = int(input("[Edit Member] Choose Option: "))
      except:
        print("Wrong index! Must be integer.")
      else:
        if index in (1, 2, 3):
          if index == 1:
            edit_member("name")
            break
          elif index == 2:
            edit_member("phone")
            break
          else:
            break
        else:
          print(f"Index {index} is not defined!")

def edit_member(data: str):
  db, cr = connect_database()
  while True:
    try:
      member_id = int(input("Enter Member ID: "))
    except:
      print("Wrong index! Must be integer.")
    else:
      cr.execute(f"SELECT * FROM members WHERE id = '{member_id}'")
      member_data = cr.fetchone()
      if not member_data:
        print(f"There is no member with ID = {member_id}")
      else:
        result = f"({member_data[0]} | {member_data[1]} | {member_data[2]}"
        print("-" * len(result))
        print(result)
        print("-" * len(result))
        if data == "name":
          while True:
            new_name = input("Enter New Name: ").strip().title()
            new_data = check_input(new_name)
            if not new_data:
              continue
            break
        elif data == "phone":
          while True:
            new_data = input("Enter New Phone: ").strip()
            if not new_data.isdigit():
              print("Phone number must be all digits!")
              continue
            break
        cnfrm = confirmation("Apply new edit? (y/n) ")
        if cnfrm:
          if data == "name":
            cr.execute(f"UPDATE borrowed SET mem_name = '{new_data}' WHERE mem_id = '{member_id}'")
          cr.execute(f"UPDATE members SET '{data}' = '{new_data}' WHERE id = '{member_id}'")
          db.commit()
          print(f"{data.title()} Updated!")
        input("Press Enter to return ")
        return

def delete_member(is_members: bool):
  db, cr = connect_database()
  title = "======== Delete Member ========"
  print(title)
  if not is_members:
    print("There are no members to delete.")
    input("Press Enter to return ")
    return
  while True:
    try:
      member_id = int(input("Enter Member ID to delete: "))
    except:
      print("Wrong input! Must be integer.")
    else:
      if member_id == 0:
        return
      cr.execute(f"SELECT * FROM members WHERE id = '{member_id}'")
      member = cr.fetchone()
      if not member:
        print(f"There is no member with ID = {member_id}")
      else:
        result = f"{member[0]} | {member[1]}"
        print("-" * len(result))
        print(result)
        print("-" * len(result))
        borrows = check_member_borrows(member_id)
        if borrows:
          print("This member has borrowed book! Can not delete them.")
        else:
          cnfrm = confirmation("Are you sure you want to delete the selected member? (y/n) ")
          if cnfrm:
            cr.execute(f"DELETE FROM members WHERE id = '{member_id}'")
            db.commit()
            print(f"Member '{member[0]}' deleted seccesfully.")
          input("Press Enter to return ")
          return

def search_member(is_members: bool):
  db, cr = connect_database()
  title = "======== Seacrh Member By Name ========"
  print(title)
  if not is_members:
    print("There are no members to search.")
    input("Press Enter to return ")
    return
  while True:
    search = input("Enter Member Name to search: ").strip()
    cr.execute(f"SELECT * FROM members WHERE name LIKE '%{search}%'")
    search_result = cr.fetchall()
    if not search_result:
      print(f"There is no members with the name: '{search}'")
    else:
      print("-" * 30)
      print(f"Members with the name '{search}':")
      for member in search_result:
        final_result = f"({member[0]} | {member[1]} | {member[2]})"
        print(final_result)
      print("-" * 30)
    cnfrm = confirmation("Search Again? (y/n) ")
    if cnfrm:
      continue
    input("Press Enter to return ")
    return