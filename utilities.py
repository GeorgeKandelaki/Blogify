def findById(arr, id):
    for el in arr:
        if el.id == id:
            return el

    return False
