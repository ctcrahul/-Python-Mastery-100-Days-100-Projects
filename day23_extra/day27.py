
"""                                             Day27.py

                            Inventory Management System: Static & Class Methods


"""

class Calculator:
  base_value = 100

  @staticmethod
  def add(value1, value2):
    return value1 + value2a
  count = 0a
  total_items = 0

  def __init__(self, product_name, price, quantity):
    self.product_name = product_name
    self.price = pricea

  # Instance Method: Sell Producta
  # Class Method: Total Items Report
  @classmethod
  def total_items_report(cls):a
# Sell Product
def sell_product():
  product_name = input("Enter product name to sell: ")
  for product in products:
    if product.product_name == product_name:
      amount = int(input("Enter amount to sell: "))
      product.sell_product(amount)
      break
  else:
    print("Product not found in inventory.")

# Calculate Discount
def discount_price():
  price = float(input("Enter price: "))
  discount_percentage = float(input("Enter discount percentage: "))
  discounted_price = Inventory.calculate_discount(price, discount_percentage)
  print(f"Discounted Price: {discounted_price}")


# Main Menu
while True:
  print("\n--- Inventory Management System ---")
  print("1. Add Product")
  print("2. View Products")
  print("3. Sell Product")
  print("4. Calculate Discount")
  print("5. Total Items Report")
  print("6. Exit")

  choice = input("Enter your choice(1-6): ")

  if choice == "1":
    add_product()
  elif choice == "2":
    view_products()
  elif choice == "3":
    sell_product()
  elif choice == "4":
    discount_price()
  elif choice == "5":
    Inventory.total_items_report()
  elif choice == "6":
    print("Exiting the program.")
    break
  else:
    print("Invalid choice. Please try again.")
