def retrieve_review_By_Product_Id(db,pid):
    search = {"product_id" : pid}
    collection = db.reviews 
    #print("search")
    #print(search)
    result = list(collection.find(search)) 
    #print("result")
    #print(result)

    return result
