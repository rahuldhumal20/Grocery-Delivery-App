
#________________Q1 Create basic FastAPI app__________________

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message:" "Welcome to FreshMart Grocery"}

#______________________Q2 Items lists _________________________

items = [
    {"id": 1, "name":"Milk", "price":72, "unit":"litre", "category":"Dairy","in_stock": True},
    {"id": 2, "name":"Apple", "price":120, "unit":"kg", "category":"Fruit","in_stock": True},
    {"id": 3, "name":"Rice", "price":60, "unit":"kg", "category":"Grain","in_stock": True},
    {"id": 4, "name":"Eggs", "price":80, "unit":"dozen", "category":"Dairy","in_stock": False},
    {"id": 5, "name":"Tomato", "price":30, "unit":"kg", "category":"Vegetable","in_stock": True},
    {"id": 6, "name":"Bread", "price":40, "unit":"piece", "category":"Grain","in_stock": True},

]

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