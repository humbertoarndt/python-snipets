from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>humberto</h1>\n<h2>doisberto</h2>\n<h3>trêsberto</h3>\n', 200

@app.route('/post_json', methods=['POST'])
def print_json():
    print("Entrei na rota")
    return 'teste', 200

if __name__ == '__main__':
    app.run(debug=True)

# curl -X POST http://127.0.0.1:5000/post_json -H 'Content-Type: application/json' -d '{"foo": "bar"}'