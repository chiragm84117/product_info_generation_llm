from serpapi import GoogleSearch
from api_access_key import lens_api_key

def comparitor_price(prod_name):
    params = {
        "engine": "google_shopping",
        "q": prod_name,  # Use prod_name to dynamically set the product name
        "api_key": lens_api_key
    }

    # Perform the search
    search = GoogleSearch(params)
    results = search.get_dict()

    # Check if "shopping_results" is in results to avoid errors
    shopping_results = results.get("shopping_results", [])

    # Prepare a list to store the price and source of each product
    product_details = []

    # Loop through the first 5 products and collect their price and source
    for product in shopping_results[:5]:
        price = product.get('price', 'Price not available')
        source = product.get('source', 'Source not available')
        product_details.append({"price": price, "source": source})

    return product_details


# Example usage
products = comparitor_price("Macbook M3")
print(products)
