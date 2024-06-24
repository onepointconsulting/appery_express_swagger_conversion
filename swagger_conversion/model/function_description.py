function_description_swagger_result = {
    "name": "process_swagger",
    "description": "Processes a Swagger API definition",
    "type": "object",
    "parameters": {
        "type": "object",
        "properties": {
            "swagger_definition": {
                "type": "string",
                "description": "The Swagger definition as Yaml using the openapi format.",
            },
            "description": {
                "type": "string",
                "description": "A textual description of the API",
            },
        },
        "required": ["swagger_definition", "description"],
    },
}
