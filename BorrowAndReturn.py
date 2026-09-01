"""
Borrow And Return
"""
from Funcs import *
from Members import search_member

def borrow_return_menu():
  """Borrow And Return Main Menu"""
  db, cr = connect_database()
  title = """
=====================
  Borrow And Return  
====================="""
  options = """
1. Show Available Books
2. Show Borrowed Books
3. Back
"""
  while True:
    print(title)
    print(options)
    while True:
      try:
        index = int(input("[B&R] Choose Option: "))
      except:
        print("Wrong index! Must be integer.")
      else:
        if index in (1, 2, 3):
          if index == 1:
            show_available_books()
            break
          elif index == 2:
            show_borrowed_books()
            break
          else:
            db.close()
            return
        else:
          print(f"Index {index} is not defined!")

def show_available_books():
  db, cr = connect_database()
  title = "======== Available Books In Library ========"
  while True:
    print(title)
    cr.execute("SELECT * FROM books WHERE status = 'Available'")
    ava_books = cr.fetchall()
    if not ava_books:
      print("There are no available books to borrow.")
      print("=" * len(title))
      input("Press Enter ro return")
      return
    for book in ava_books:
      result = f"({book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]})"
      print(result)
    print("=" * len(title))
    print("1. Borrow | 2. Back")
    while True:
      try:
        index = int(input("[Borrowing] Choose Option: "))
      except:
        print("Wrong index! Must be integer.")
      else:
        if index in (1, 2):
          if index == 1:
            borrow_book(db, cr, result)
            break
          else:
            return
        else:
          print(f"Index {index} is not defined!")

def borrow_book(db, cr, result):
  is_members = check_for_members()
  if not is_members:
    print("There are no members to borrow book!")
    input("Press Enter to return ")
    return
  while True:
    try:
      book_id = int(input("Enter Book ID to borrow: "))
    except:
      print("Wrong index! Must be integer.")
    else:
      cr.execute(f"SELECT * FROM books WHERE id = '{book_id}'")
      selected_book = cr.fetchone()
      if not selected_book:
        print(f"There is no book with ID = {book_id}")
      else:
        borrowed = is_borrowed(book_id)
        if borrowed:
          print(f"Book with ID = {book_id} is already borrowed!")
          continue
        print("-" * len(result))
        print(f"({selected_book[0]} | {selected_book[1]} | {selected_book[2]} | {selected_book[3]} | {selected_book[4]})")
        print("-" * len(result))
        search_member(is_members)
        while True:
          try:
            member_id = int(input("Enter Member ID to borrow book: "))
          except:
            print("Wrong index! Must be integer.")
          else:
            cr.execute(f"SELECT * FROM members WHERE id = '{member_id}'")
            selected_member = cr.fetchone()
            if not selected_member:
              print(f"There is no member with ID = '{member_id}'")
            else:
              cnfrm_msg = f"Borrowing Book: ({selected_book[0]} | {selected_book[1]} | {selected_book[2]})\nTo Member: ({selected_member[0]} | {selected_member[1]} | {selected_member[2]})"
              print("-" * (len(cnfrm_msg) - 40))
              print(cnfrm_msg)
              print("-" * (len(cnfrm_msg) - 40))
              cnfrm = confirmation("Confirm Borrowing? (y/n) ")
              if cnfrm:
                borrowed_book_member = [selected_book[0], selected_book[1], selected_book[2], selected_member[0], selected_member[1], selected_member[2]]
                cr.execute("INSERT INTO borrowed(book_id, book_title, book_author, mem_id, mem_name, mem_phone) VALUES(?, ?, ?, ?, ?, ?)", borrowed_book_member)
                cr.execute(f"UPDATE books SET status = 'Borrowed' WHERE id = {selected_book[0]}")
                db.commit()
                print("Book Borrowed Seccessfully!")
              input("Press Enter to return ")
              return

def show_borrowed_books():
  db, cr = connect_database()
  title = "======== Borrowed Books From Library ========"
  while True:
    print(title)
    cr.execute("SELECT * FROM borrowed")
    borrowed_list = cr.fetchall()
    if not borrowed_list:
      print("There are no borrowed books.")
      print("=" * len(title))
      input("Press Enter to return ")
      return
    for book in borrowed_list:
      result = f"({book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {book[5]})"
      print(result)
    print("=" * len(title))
    print("1. Return | 2. Back")
    while True:
      try:
        index = int(input("[Returning] Choose Option: "))
      except:
        print("Wrong index! Must be integer.")
      else:
        if index in (1, 2):
          if index == 1:
            return_book(db, cr)
            break
          else:
            return
        else:
          print(f"Index {index} is not defined!")

def return_book(db, cr):
  while True:
    try:
      book_id = int(input("Enter Book ID: "))
    except:
      print("Wrong index! Must be integer.")
    else:
      borrowed = is_borrowed(book_id)
      if not borrowed:
        print(f"There is no borrowed book with ID = {book_id}")
      else:
        cr.execute(f"SELECT * FROM borrowed WHERE book_id = '{book_id}'")
        selected_book = cr.fetchone()
        cnfrm_msg = f"Returning Book: ({selected_book[0]} | {selected_book[1]} | {selected_book[2]})"
        print("-" * len(cnfrm_msg))
        print(cnfrm_msg)
        print("-" * len(cnfrm_msg))
        cnfrm = confirmation("Confirm Returning? (y/n) ")
        if cnfrm:
          cr.execute(f"DELETE FROM borrowed WHERE book_id = '{book_id}'")
          cr.execute(f"UPDATE books SET 'status' = 'Available' WHERE id = '{book_id}'")
          db.commit()
          print("Book Retruned Seccsefully!")
        input("Press Enter to return")
        return