def retrieve_recommendation_by_product_id(db,pid):
    search = {"product_Id":pid}
    collection = db.recommendation 
    result = collection.find_one(search) 

    return result
