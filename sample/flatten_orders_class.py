import json
from dataclasses import dataclass
from typing import List

@dataclass
class LineItem:
    item_id: int
    product_name: str
    price: float

@dataclass
class Order:
    order_id: int
    customer_name: str
    sale_date: str
    line_items: List[LineItem]
    
    # Adding a helper method directly to the class
    def get_order_total(self) -> float:
        return sum(item.price for item in self.line_items)

def flatten_orders_to_dicts(orders: List[Order]) -> List[dict]:
    """
    Takes a list of Order objects and flattens them into a list of dictionaries.
    """
    result = []
    
    for order in orders:
        for item in order.line_items:
            flat_record = {
                "order_id": order.order_id,
                "customer": order.customer_name,
                "date": order.sale_date,
                "line_id": item.item_id,
                "prod": item.product_name,
                "amount": item.price,
            }
            result.append(flat_record)
            
    return result

if __name__ == "__main__":
    # Standard JSON payload as provided by an API
    api_response = [
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

    print("----- 1. Convert Raw JSON into Python Objects -----")
    # This is where we manually map the dictionaries to our new dataclasses
    orders_list: List[Order] = []
    for raw_order in api_response:
        
        # First build the inner line items
        items = []
        for raw_item in raw_order.get("line_items", []):
            item_obj = LineItem(
                item_id=raw_item.get("item_id"),
                product_name=raw_item.get("product_name"),
                price=raw_item.get("price")
            )
            items.append(item_obj)
            
        # Then build the parent order with the parsed items
        order_obj = Order(
            order_id=raw_order.get("order_id"),
            customer_name=raw_order.get("customer_name"),
            sale_date=raw_order.get("sale_date"),
            line_items=items
        )
        orders_list.append(order_obj)

    print("Successfully created %d Python Order Objects." % len(orders_list))
    print(orders_list)
    print("\n")


    print("----- 2. Demonstrate Object Behavior (Methods) -----")
    # Because they are objects, we can easily run methods on them!
    for o in orders_list:
        print(f"Order #{o.order_id} Total Amount: ${o.get_order_total():.2f}")
    print("\n")


    print("----- 3. Flatten the Objects -----")
    # Now we pass our strong Objects to the flatten function instead of raw dicts
    flattened_data = flatten_orders_to_dicts(orders_list)
    
    print(json.dumps(flattened_data, indent=2))
