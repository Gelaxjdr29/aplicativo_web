from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
products = []

class Product:
    def __init__(self, name, price, min_stock, max_stock):
        self.name = name
        self.price = price
        self.min_stock = min_stock
        self.max_stock = max_stock
        self.sales = 0

@app.route('/templates')
def pagina_1():
    return render_template('agregar_producto.html')
@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    min_stock = request.form.get('min_stock')
    max_stock = request.form.get('max_stock')
    
    if name and price and min_stock and max_stock:
        new_product = Product(name, price, min_stock, max_stock)
        products.append(new_product)
        message = 'Producto agregado exitosamente!'
    else:
        message = 'Faltan detalles del producto. Por favor, inténtalo de nuevo.'

    return render_template('index.html', message=message, products=products)

@app.route('/delete', methods=['POST'])
def delete_product():
    name = request.form.get('name')
    products[:] = [product for product in products if product.name != name]
    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def update_product():
    name = request.form.get('name')
    price = request.form.get('price')
    min_stock = request.form.get('min_stock')
    max_stock = request.form.get('max_stock')

    for product in products:
        if product.name == name:
            if price:
                product.price = price
            if min_stock:
                product.min_stock = min_stock
            if max_stock:
                product.max_stock = max_stock
            break

    return redirect(url_for('home'))

@app.route('/sales', methods=['POST'])
def register_sale():
    name = request.form.get('name')
    quantity = int(request.form.get('quantity'))

    for product in products:
        if product.name == name:
            product.sales += quantity
            break

    return redirect(url_for('home'))

@app.route('/sales_report', methods=['GET'])
def sales_report():
    sales_report = []
    for product in products:
        if product.sales > 0:
            sales_report.append({
                'name': product.name,
                'quantity_sold': product.sales,
                'total_price': product.sales * product.price
            })
    return render_template('sales_report.html', sales_report=sales_report)



if __name__ == '__main__':
    app.run(debug=True)

