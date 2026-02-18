# we have to enable the virtual environment for every new project 
# then run this commmand to install the uvicorn and FastApi pip install fastapi uvicorn
# the uvicorn is like the heart beat if the FastApi is brain
# uvicorn is ASGI server 
# ASGI stands for Asynchrounuous Server Gateway Interface
# to run the app we need to run this command at the directory of the file 
# uvicorn filename:'FastApi instance name' --reload
# to start our 
# pydantic is the backbone of the fastapi
## this to implement the query with the path 
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/products/{product_id}")
# def get_product(product_id:int, discount:float=0.0):
#     original_price = 100.0
#     discounted_price = original_price * (1 - discount/100)
#     return {
#         "product_id": product_id,
#         "original_price": original_price,
#         "discounted_price": discounted_price,
#         "status": "retrieved successfully"
#     }

### to create the professional secret key use this command python -c "import secrets; print(secrets.token_hex(32))"