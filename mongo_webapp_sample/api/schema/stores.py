add_store = {
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
        "address": {
            "type": "string",
            "minLength": 4,
            "maxLength": 255
        },
        "email": {
            "type": "string",
            "minLength": 4,
            "maxLength": 255,
            "format": "email"
        },
        "phone": {
            "type": "string",
            "minLength": 6,
            "maxLength": 64,
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 2,
                "maxLength": 255,
            },
        },
        "location": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "pattern": "^Point$"
                },
                "coordinates": {
                    "type": "array",
                    "items": {
                        "type": "number",
                        "minLength": 2,
                        "maxLength": 2,
                    },
                },
            },
            "required": ["coordinates"],
        },
    },
    "required": ["name"],
}

update_store = {
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
        "address": {
            "type": "string",
            "minLength": 4,
            "maxLength": 255
        },
        "email": {
            "type": "string",
            "minLength": 4,
            "maxLength": 255,
            "format": "email"
        },
        "phone": {
            "type": "string",
            "minLength": 6,
            "maxLength": 64,
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 2,
                "maxLength": 255,
            },
        },
        "location": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "pattern": "^Point$"
                },
                "coordinates": {
                    "type": "array",
                    "items": {
                        "type": "number",
                        "minLength": 2,
                        "maxLength": 2,
                    },
                },
            },
            "required": ["coordinates"],
        },
    },
}
