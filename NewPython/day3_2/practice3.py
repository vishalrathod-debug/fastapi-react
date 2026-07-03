from flask import Flask , request , render_template

app = Flask(__name__)

@app.route('/practice')
def practice():

    items=["Pen", "Book", "Laptop"]

    return render_template('practice.html',items=items)

if __name__ == '__main__':
    app.run(debug=True)