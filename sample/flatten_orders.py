import json

def flatten_orders(api_response):
    """
    Transforms a nested list of API orders into a flat list of dictionaries.
    """
    result = []
    
    # Iterate through each order in the API response
    for order in api_response:
        
        # For each order, iterate through its line items
        for item in order.get("line_items", []):
            
            # Create a single flat dictionary combining order and item data
            flat_record = {
                "order_id": order.get("order_id"),
                "customer": order.get("customer_name"),
                "date": order.get("sale_date"),
                "line_id": item.get("item_id"),
                "prod": item.get("product_name"),
                "amount": item.get("price")
            }
            
            # Add this flat dictionary to our result list
            result.append(flat_record)
            
    return result

if __name__ == "__main__":
    sample_data = [
        {
            "order_id": 101,
            "customer_name": "Acme Corp",
            "sale_date": "2023-10-27",
            "line_items": [
                {"item_id": 1, "product_name": "Widget A", "price": 50.0},
                {"item_id": 2, "product_name": "Widget B", "price": 100.0}
            ]
        },
        {
            "order_id": 102,
            "customer_name": "Globex",
            "sale_date": "2023-10-27",
            "line_items": [
                {"item_id": 3, "product_name": "Gadget X", "price": 75.0}
            ]
        }
    ]

    print("----- Original Data -----")
    print(json.dumps(sample_data, indent=2))
    
    flattened = flatten_orders(sample_data)
    
    print("\n----- Flattened Data -----")
    print(json.dumps(flattened, indent=2))
