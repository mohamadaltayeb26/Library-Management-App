"""
Functions
"""

import os
import sqlite3
from string import ascii_letters as letters

def connect_database():
  """Connect To Database"""
  db_abs_path = os.path.join(os.path.dirname(__file__), "Library.db")
  db = sqlite3.connect(db_abs_path)
  cr = db.cursor()
  return db, cr

def setup_database():
  db, cr = connect_database()
  cr.execute(
    "CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, title TEXT, author TEXT, category TEXT, status TEXT)"
  )
  cr.execute(
    "CREATE TABLE IF NOT EXISTS members(id INTEGER PRIMARY KEY, name TEXT, phone TEXT)"
  )
  cr.execute(
    "CREATE TABLE IF NOT EXISTS borrowed(book_id INTEGER, book_title TEXT, book_author TEXT, mem_id INTEGER, mem_name TEXT, mem_phone TEXT)"
  )
  db.commit()
  db.close()

def check_input(input: str, type: str):
  """
  Checks if input if allowed.

  Args:
    input(str): the user input.
    type(str): book name, or member name.

  Returns True if Yes, False if No.
  """
  new_string = ""
  if len(input) < 3:
    print("Must be at least 3 letters!")
    return False
  if type == "book":
    i = 0
    while i < len(input):
      if input[i] != " ":
        new_string += input[i]
      elif input[i] == " " and input[i-1] != " ":
        new_string += " "
      i += 1
    return new_string
  if type == "name":
    for letter in input:
      if letter not in letters + " ":
        print("Only English letters allowed!")
        return False
    i = 0
    while i < len(input):
      if input[i] in letters:
        new_string += input[i]
      elif input[i] == " " and input[i-1] != " ":
        new_string += " "
      i += 1
    return new_string

def confirmation(cnfrm_msg: str):
  """
  Shows a confirmation message, to answer with Yes or No.

  Argument:
    cnfrm_msg(str): The confrimation message intended to show up.
  
  Retruns:
    True if yes, False if no.
  """
  while True:
    cnfrm = input(cnfrm_msg).strip().lower()
    if cnfrm in ("y", "yes", "n", "no"):
      if cnfrm in ("y" , "yes"):
        return True
      else:
        return False
    else:
      print("Answer with 'Y' or 'N'")

def is_borrowed(book_id: int):
  """
  Checks if book is borrowed, return True if borrowed, False if available.
  """
  db, cr = connect_database()
  cr.execute(f"SELECT * FROM borrowed WHERE book_id = '{book_id}' ")
  result = cr.fetchone()
  if not result:
    return False
  else:
    return True

def check_member_borrows(member_id: int):
  """
  Checks if member has borrowed books, returns True if they has, False if otherwise.
  """
  db, cr = connect_database()
  cr.execute(f"SELECT * FROM borrowed WHERE mem_id = '{member_id}'")
  result = cr.fetchall()
  if not result:
    return False
  else:
    return True

def check_for_members():
  """
  Checks if there are members in the database, returns True if there are, False if not.
  """
  db, cr = connect_database()
  cr.execute("SELECT * FROM members")
  members = cr.fetchall()
  if not members:
    return False
  else:
    return True
