card_with_category_lookup = [
     {
        "$lookup": {
            "from": "cardCategories",
            "localField": "category_id",
            "foreignField": "_id",
            "as": "category"
        }
    },
    {
        "$unwind": "$category"
    }
]

card_with_field_match = lambda field, value: {
        "$match": {
            field: value
        }
}