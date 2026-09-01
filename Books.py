"""
Books Section
"""

from Funcs import *

def books_storage():
  """Books Main Menu"""
  db, cr = connect_database()
  title = """
=================
  Books Storage
================="""
  syntax = "(ID | Title | Author | Category | Status)"
  options = "1. Add | 2. Edit | 3. Delete | 4. Search | 5. Back"
  back = False
  while True:
    print(title)
    print(syntax)
    print("=" * len(syntax))
    cr.execute("SELECT * FROM books")
    books = cr.fetchall()
    if not books:
      print("---- Books list is empty ----")
    else:
      is_books = True
      for book in books:
        result = f"({book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]})"
        print(result)
    print("=" * len(syntax))
    print(options)
    print("=" * len(syntax))
    while True:
      try:
        index = int(input("[Storage] Choose Option: "))
      except:
        print("Wrong index! Must be integer.")
      else:
        if index in (1, 2, 3, 4, 5):
          if index == 1:
            add_book()
            break
          elif index == 2:
            edit_book_menu(is_books)
            break
          elif index == 3:
            delete_book(is_books)
            break
          elif index == 4:
            search_book(is_books)
            break
          else:
            db.close()
            return
        else:
          print(f"Index {index} is not defined!")

def add_book():
  db, cr = connect_database()
  title = "======== Adding Book ========"
  print(title)
  book_data = []
  for title in ("Book Title", "Author Name", "Category"):
    while True:
      user_input = input(f"Enter {title}: ").strip().title()
      checked_input = check_input(user_input)
      if not checked_input:
        continue
      else:
        book_data.append(checked_input)
        break
  book_data.append("Available")
  cr.execute("INSERT INTO books(title, author, category, status) VALUES(?, ?, ?, ?)", book_data)
  db.commit()
  print(f"Book '{book_data[0]}' added seccesfully!")
  input("Press Enter to return ")

def edit_book_menu(is_books: bool):
  title = "======== Edit Book ========"
  if not is_books:
    print("There are no books to edit.")
    cnfrm = confirmation("Would you like to add a book now? (y/n) ")
    if cnfrm:
      add_book()
      return
    else:
      return
  else:
    title_two = "What do you want to edit?"
    options = "1. Title | 2. Author | 3. Category | 4. Back"
    while True:
      print(title)
      print(title_two)
      print("=" * 41)
      print(options)
      print("=" * 41)
      back = False
      while True:
        try:
          index = int(input("[Edit Book] Choose Option: "))
        except:
          print("Wrong index! Must be integer.")
        else:
          if index in (1, 2, 3, 4):
            if index == 1:
              edit_book("title")
              return
            elif index == 2:
              edit_book("author")
              return
            elif index == 3:
              edit_book("category")
              return
            else:
              return
          else:
            print(f"Index {index} is not defined!")

def edit_book(data: str):
  db, cr = connect_database()
  while True:
    try:
      book_id = int(input("Enter Book ID: "))
    except:
      print("Wrong input! Must be Integer.")
    else:
      cr.execute(f"SELECT * FROM books WHERE id = {book_id}")
      book_data = cr.fetchone()
      if not book_data:
        print(f"There is no book with ID = {book_id}")
      else:
        result = f"({book_data[0]} | {book_data[1]} | {book_data[2]} | {book_data[3]})"
        print("-" * len(result))
        print(result)
        print("-" * len(result))
        while True:
          new_data = input(f"Enter new {data.title()}: ").strip().title()
          checked_input = check_input(new_data)
          if not checked_input:
            continue
          else:
            break
        cnfrm = confirmation("Apply new edit? (y/n) ")
        if cnfrm:
          if data == "title":
            cr.execute(f"UPDATE borrowed SET book_title = '{checked_input}' WHERE book_id = '{book_id}'")
          cr.execute(f"UPDATE books SET '{data}' = '{checked_input}' WHERE id = '{book_id}'")
          db.commit()
          print(f"{data.title()} Updated!")
        input("Press Enter to return ")
        return

def delete_book(is_books: bool):
  db, cr = connect_database()
  title = "======== Deleting Book ========"
  print(title)
  if not is_books:
      print("There are no books to delete.")
      input("Press Enter to return ")
      return
  while True:
    try:
      book_id = int(input("Enter Book ID to delete: "))
    except:
      print("Wrong input! Must be integer.")
    else:
      if book_id == 0:
        return
      cr.execute(f"SELECT * FROM books WHERE id = {book_id}")
      book = cr.fetchone()
      if not book:
        print(f"There is no book with ID = {book_id}")
      else:
        borrowed = is_borrowed(book_id)
        if borrowed:
          print(f"The book with ID = {book_id} is borrowed, can not delete it.")
        else:
          result = f"({book[0]} | {book[1]} | {book[2]} | {book[3]})"
          print("-" * len(result))
          print(result)
          print("-" * len(result))
          cnfrm = confirmation("Are you sure you want to delete the selected book? (y/n) ")
          if cnfrm:
            cr.execute(f"DELETE FROM books WHERE id = '{book_id}'")
            db.commit()
            print(f"Book '{book[0]}' deleted seccesfully.")
          input("Press Enter to return ")
          return

def search_book(is_books: bool):
  db, cr = connect_database()
  title = "======== Search Book By Title ========"
  print(title)
  if not is_books:
    print("There are no books to search.")
    input("Press Enter to return")
    return
  while True:
    search = input("Enter search: ").strip()
    cr.execute(f"SELECT * FROM books WHERE title LIKE '%{search}%'")
    search_result = cr.fetchall()
    if not search_result:
      print(f"There is no book with the keyword: '{search}'")
    else:
      print(f"Books with the keyword '{search}':")
      for book in search_result:
        final_result = f"({book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]})"
        print(final_result)
      input("Press Enter to return ")
      break
