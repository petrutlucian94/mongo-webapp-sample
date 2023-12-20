add_product = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 4,
            "maxLength": 255
        },
        "description": {
            "type": "string",
            "minLength": 4,
            "maxLength": 255
        },
        "price": {
            "type": "number",
        },
        "price_currency": {
            "type": "string",
            "minLength": 1,
            "maxLength": 32,
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 2,
                "maxLength": 255,
            },
        },
    },
    "required": ["name"],
}
