
#________________Q1 Create basic FastAPI app__________________

from fastapi import FastAPI, HTTPException


app = FastAPI()

@app.get("/")
def home():
    return {"message:" "Welcome to FreshMart Grocery"}

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

