def retrieve_review_By_Product_Id(db,pid):
    search = {"product_id" : pid}
    collection = db.reviews 
    result = list(collection.find(search)) 

    return result
