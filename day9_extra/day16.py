
"""                                   Day16.py

                          Daily Journal Logger: Writing Files


"""


# Step 3: View all entries
def view_entries():
  try:
    with open(JOURNAL_FIng today")
  except FileNotFoundError:
    print("No journal file found. Add an entry first!")

# Step 4: Search entries by keyword
def search_entries()
        if keyword in entry.lower():
          print(entry.strip())
          found = True
      if not found:
        print("No matching entries found.")
  except FileNotFoundError:
    print("No journal file found. Add an entry first!")


# Step 5: Display Menu
def show_menu():
  print("\n--- Daily Journal Logger ---")
  print("1. Add a new entry")
  print("2. View all entries")
  print("3. Search entries by keyword")
  print("4. Exit")

    add_entry()
  elif choice == '2':
    view_entries()
  elif choice == '3':
    search_entries()
