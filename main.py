import json
from fastapi import FastAPI, HTTPException

app = FastAPI()


def load_menu():
    try:
        with open("mcdonalds_menu.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Menu file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading menu: {str(e)}")


@app.get("/all_products/")
def get_all_products():
    return load_menu()


@app.get("/products/{product_name}")
def get_product(product_name: str):
    products = load_menu()

    for product in products:
        if product["name"] == product_name:
            return product

    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/products/{product_name}/{product_field}")
def get_product_field(product_name: str, product_field: str):
    products = load_menu()

    for product in products:
        if product["name"] == product_name:
            if product_field in product:
                return {product_field: product[product_field]}
            else:
                raise HTTPException(status_code=404,
                                    detail=f"Field '{product_field}' not found for product '{product_name}'")

    raise HTTPException(status_code=404, detail="Product not found")
