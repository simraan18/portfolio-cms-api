def normalize(doc):
    doc["id"] = str(doc["_id"])
    doc.pop("_id")
    return doc