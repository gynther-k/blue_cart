def retrieve_shopping_cart_by_customer_id(db,cid):
    search = {"customer_Id":cid}
    collection = db.shopping_cart 
    result = collection.find_one(search) 

    return result
