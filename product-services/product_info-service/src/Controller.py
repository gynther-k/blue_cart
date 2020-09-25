def retrieve_Product_By_Id(db,pid):
    search = {"product_id" : pid}
    collection = db.products 
    result = collection.find_one(search) 

    return result