from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample product catalog (Product ID, Name, Price, Discount %)
products = {
    1: {"name": "Milk", "price": 2.5, "discount": 10},
    2: {"name": "Bread", "price": 1.5, "discount": 5},
    3: {"name": "Eggs", "price": 3.0, "discount": 0},
    4: {"name": "Rice", "price": 5.0, "discount": 15},
    5: {"name": "Vegetables", "price": 4.0, "discount": 20},
}

# Cart for storing customer purchases
cart = {}

# Route to get all products
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

# Route to get a specific product by ID
@app.route("/product/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

# Route to add a product to the cart
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404

    if product_id in cart:
        cart[product_id]["quantity"] += quantity
    else:
        cart[product_id] = {"name": products[product_id]["name"], "quantity": quantity}

    return jsonify({"message": f"{quantity} {products[product_id]['name']} added to cart"})

# Route to view the cart
@app.route("/cart", methods=["GET"])
def view_cart():
    if not cart:
        return jsonify({"message": "Your cart is empty"})
    return jsonify(cart)

# Route to calculate total price with discount
@app.route("/checkout", methods=["GET"])
def checkout():
    if not cart:
        return jsonify({"message": "Your cart is empty"})

    total_price = 0
    discount_amount = 0

    for product_id, details in cart.items():
        price = products[product_id]["price"]
        discount = products[product_id]["discount"]
        quantity = details["quantity"]

        item_total = price * quantity
        item_discount = (item_total * discount) / 100

        total_price += item_total
        discount_amount += item_discount

    final_price = total_price - discount_amount

    return jsonify({
        "Total Price (Before Discount)": round(total_price, 2),
        "Total Discount Applied": round(discount_amount, 2),
        "Final Price (After Discount)": round(final_price, 2)
    })

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
