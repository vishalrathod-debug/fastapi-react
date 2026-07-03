from flask import Flask , request

app = Flask(__name__)


@app.route('/search')
def search():
    item = request.args.get("item",default="unknown")
    prize = request.args.get("prize",default="0.00")

    return {"item":item ,"prize":prize,"message":"Query parameters received"}
    #This Flask app creates a /search endpoint that extracts query parameters
    # from the URL and returns them as a JSON response.
    #/search?item=apple&price=10

@app.route('/register',methods=['POST','GET'])
def register():
    data = request.json

    if not data:
        return {"message":"No JSON data provided"}, 400
    name = data.get("name")
    age = data.get("age")

    if not name and not age :
        return {"error": "name and age are required"}, 400

    return {"name":name ,
            "age":age ,
            "message":"User registered successfully"
            }



if __name__ == '__main__':
    app.run(debug=True)