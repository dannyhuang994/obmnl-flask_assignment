# Import libraries
from flask import Flask, url_for, redirect, request, render_template
# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [    {'id': 1, 'date': '2023-06-01', 'amount': 100},
                    {'id': 2, 'date': '2023-06-02', 'amount': -200},
                    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]
 

# Read operation: List all transactions
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation: Display add transaction form
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        # Append the new transaction to the list
        transactions.append(transaction)

        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))
    
    # Render the form template to display the add transaction form
    return render_template("form.html")

# Update operation: Display edit transaction form
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']
        amount = float(request.form['amount'])

        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break

        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))
    
    # Find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

# Delete operation: Delete a transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break

    # Redirect to the transactions list page
    return redirect(url_for("get_transactions"))

# adding a search page
@app.route("/search",methods=["GET", "POST"])
def search_transactions():
    
    if request.method == "POST":
        min_amount = float(request.form.get("min_amount"))
        max_amount = float(request.form.get("max_amount"))
        result = []
        for trans in transactions:
            if trans['amount'] >= min_amount and trans['amount'] <= max_amount:
                result.append(trans)
        ## returning the filtered result        
        return render_template("transactions.html", transactions=result)
    
    # return the page for search
    return render_template("search.html")

@app.route("/balance")
def total_balance():
    total = 0
    for transaction in transactions:
        total += transaction['amount']
    
    return render_template("transactions.html", transactions=transactions, total=total)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
    