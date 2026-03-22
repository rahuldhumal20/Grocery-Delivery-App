
#________________Q1 Create basic FastAPI app__________________

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()

@app.get("/")
def home():
    return {"message":"Welcome to FreshMart Grocery"}

#_________________________Q2 Items lists _________________________

items = [
    {"id": 1, "name":"Milk", "price":72, "unit":"litre", "category":"Dairy","in_stock": True},
    {"id": 2, "name":"Apple", "price":120, "unit":"kg", "category":"Fruit","in_stock": True},
    {"id": 3, "name":"Rice", "price":60, "unit":"kg", "category":"Grain","in_stock": True},
    {"id": 4, "name":"Eggs", "price":80, "unit":"dozen", "category":"Dairy","in_stock": False},
    {"id": 5, "name":"Tomato", "price":30, "unit":"kg", "category":"Vegetable","in_stock": True},
    {"id": 6, "name":"Bread", "price":40, "unit":"piece", "category":"Grain","in_stock": True},

]

orders = []
order_counter = 1

cart = []
#______________________Order Request -Pydantic Model______________________

class OrderRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    item_id: int = Field(gt = 0)
    quantity: int = Field(gt=0, le=50)
    delivery_address: str = Field(min_length=10)
    delivery_slot:str = "Morning"
    bulk_order: bool = False                      # bulk_order
#________________________NewItem Model_____________________

class NewItem(BaseModel):
    name: str = Field(min_length=2)
    price: int = Field(gt=0)
    unit: str = Field(min_length=2)
    category: str = Field(min_length=2)
    in_stock:bool = True
#______________________Checkout model______________________

class CheckoutRequest(BaseModel):
    customer_name: str = Field(min_length = 2)
    delivery_address: str = Field(min_length=10)
    delivery_slot: str ="Morning"


#__________________________Helper Fuctions__________________
#__________________________find Items______________________

def find_item(item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    return None

#______________________Calculate_Order_total____________________

def calculate_order_total(price, quantity, delivery_slot, bulk_order):
    original = price * quantity

    discount = 0

    if bulk_order and quantity >= 10:
        discount = original * 0.08      # 8% discount 
        
    discounted = original - discount

    delivery_charge = 0

    if delivery_slot == "Morning":
        delivery_charge = 40
    elif delivery_slot == "Evening":
        delivery_charge = 60
    
    total = discounted + delivery_charge

    return original, discounted, total

#______________________filter items _________________________

def filter_items_logic(category, max_price, unit, in_stock):
    result = items[:]

    if category is not None:
        result = [i for i in result if i["category"] == category]

    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]

    if unit is not None:
        result = [i for i in result if i["unit"] == unit]

    if in_stock is not None:
        result = [i for i in result if i["in_stock"] == in_stock]

    return result
#__________________________GET /items____________________________

@app.get('/items')
def get_items():
    total= len(items)
    in_stock_count = len([item for item in items if item["in_stock"]])

    return {
        "total_items": total,
        "in_stock_items": in_stock_count,
        "items": items
    }


#__________________________GET /items/summary ____________________

@app.get('/items/summary')
def items_summary():
    total = len(items)

    in_stock = len([i for i in items if i["in_stock"]])
    out_of_stock = total - in_stock

    category_breakdown = {}

    for item in items:
        cat = item["category"]
        category_breakdown[cat] = category_breakdown.get(cat, 0)+1

    return {
        "total_items": total,
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "category_breakdown": category_breakdown
    }
#_____________________filter _________________________

@app.get("/items/filter")
def filter_items(
    category: Optional[str] = None,
    max_price: Optional[int] = None,
    unit: Optional[str] = None,
    in_stock: Optional[bool] = None
):
    
    result = filter_items_logic(category,max_price,unit,in_stock)

    return{
        "total_found":len(result),
        "items": result
    }

#__________________________Search Items by name,category___________________

@app.get("/items/Search")
def search_items(keyword: str):
    keyword_lower = keyword.lower()

    result = [
        item for item in items
        if keyword_lower in item["name"].lower()
        or keyword_lower in item["category"].lower()

    ]
    if not result:
        return{
            "message": "No items Found",
            "total_found": 0,
            "items": []
        }
    return {
        "total_found": len(result),
        "items": result
    }
#_____________________________Sort by - price, name, category_________________

@app.get("/items/sort")
def sort_item(
    sort_by: str = "price",
    order:str = "asc"
):
    valid_fields = ["price","name","category"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail = f"Invalid order. Use 'asc' or 'desc'"
        )
    
    reverse = True if order == "desc" else False

    sorted_items = sorted(
        items,
        key= lambda x: x[sort_by],
        reverse = reverse      
    )

    return {
        "sort_by": sort_by,
        "order" : order,
        "total_items": len(sorted_items),
        "items": sorted_items
    }

#__________________________GET items by id____________________

@app.get('/items/{item_id}')
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
        
    raise HTTPException(status_code=404, detail="Item not found")


#__________________________GET Orders____________________________

@app.get('/orders')
def get_orders():
    return{
        "total_orders": len(orders),
        "orders": orders
    }

#_____________________ Endpoint - Post Orders ________________________

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderRequest):
    global order_counter

    item = find_item(order.item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if not item["in_stock"]:
        raise HTTPException(status_code=400, detail="Item out of stock")
    
    original, discounted, total_cost = calculate_order_total(
        item["price"],
        order.quantity,
        order.delivery_slot,
        order.bulk_order
    )

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "item_name": item["name"],
        "quantity": order.quantity,
        "unit": item["unit"],
        "delivery_slot": order.delivery_slot,
        "delivery_address": order.delivery_address,
        "original_amount": original,
        "discounted_amount":discounted,
        "total_cost": total_cost,
        "status": "confirmed"

    }

    orders.append(new_order)
    order_counter += 1

    return new_order

#___________________________POST - Add NewItem ____________________________

@app.post("/items", status_code=status.HTTP_201_CREATED)
def add_item(item: NewItem):

    for i in items:
        if i["name"].lower() == item.name.lower():
            raise HTTPException(status_code=400, detail="Item already exists")
        
    new_id = len(items) + 1

    new_item = {
        "id": new_id,
        "name": item.name,
        "price": item.price,
        "unit": item.unit,
        "category": item.category,
        "in_stock": item.in_stock,

    }
    items.append(new_item)

    return new_item


#_____________________________PUT - Update item______________________

@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    price: Optional[int]= None,
    in_stock: Optional[bool]= None,
    
):
    item = find_item(item_id)

    if not item:
        raise HTTPException(status_code=404,detail="Item not Found")
    
    if price is not None:
        item["price"] = price

    if in_stock is not None:
        item["in_stock"] = in_stock

    return item

#_______________________Delete item________________________

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    item = find_item(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for order in orders:
        if order["item_name"] == item["name"]:
            raise HTTPException(
                status_code=400,
                detail="Item has active orders, cannot delete"
            )
        
    item_name = item["name"]
        
    items.remove(item)

    return {
        "message": "Item deleted successfully",
        "deleted_item": item_name
        
    }

#_______________________________Cart- Post________________________

@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_item(item_id)

    if not item:
        raise HTTPException(status_code=404,detail= "Item not found")
    
    if not item["in_stock"]:
        raise HTTPException(status_code=400, detail="Item out of stock")
    
    # check if alreay in cart

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            c["subtotal"] = c["quantity"] * c["price"]
            return {"message":"Cart Updated", "cart_item": c}

    # add new item
       
    new_cart_item = {
        "item_id": item_id,
        "name": item["name"],
        "price":item["price"],
        "quantity": quantity,
        "subtotal": item["price"] * quantity
    }

    cart.append(new_cart_item)

    return{"message": "Item added to cart" ,"cart_item":new_cart_item}


#_________________GET - cart________________________________

@app.get("/cart")
def view_cart():
    grand_total= sum(item["subtotal"] for item in cart)

    return {
        "total_items": len(cart),
        "grand_total": grand_total,
        "cart": cart
    }

#_____________________Delete cart item by id__________________

@app.delete("/cart/{item_id}")
def remove_from_cart(item_id: int):
    for item in cart:
        if item["item_id"] == item_id:
            cart.remove(item)
            return{"message":f"{item['name']} removed from cart"}

    raise HTTPException(status_code=404, detail= "Item not in cart")

#______________________Cart Checkout_______________________

@app.post("/cart/checkout", status_code=status.HTTP_201_CREATED)
def checkout(request: CheckoutRequest):
    global order_counter

    if not cart:
        raise HTTPException(status_code=404, detail="Cart is empty")
    
    created_orders = []
    grand_total = 0

    for c in cart:
        total_cost = calculate_order_total(
            c["price"],
            c["quantity"],
            request.delivery_slot,
            False       #bulk not applied here
        )[2]     

        new_order = {
            "order_id": order_counter,
            "customer_name": request.customer_name,
            "item_name": c["name"],
            "quantity": c["quantity"],
            "unit": find_item(c["item_id"])["unit"],
            "delivery_slot": request.delivery_slot,
            "delivery_address": request.delivery_address,
            "total_cost": total_cost,
            "status": "confirmed"
        }

        orders.append(new_order)
        created_orders.append(new_order)

        grand_total += total_cost
        order_counter += 1

    cart.clear()

    return{
        "message":"Checkout sucessful",
        "total_orders_created": len(created_orders),
        "grand_total": grand_total,
        "orders": created_orders
    }









