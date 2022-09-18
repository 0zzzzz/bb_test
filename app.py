from flask import Flask, request
import main


app = Flask(__name__)


@app.route('/Datalore', methods=['POST'])
def webhook():
    if request.method == 'POST':
        if 'function' in request.json:
            try:
                function = getattr(main, request.json['function'])
                if 'attributes' in request.json:
                    attributes = request.json['attributes']
                    return f'{function(attributes)}'
                try:
                    return f'{function()}'
                except TypeError:
                    return f'Не переданы атрибуты функции {request.json["function"]}'
            except AttributeError:
                return 'Данная функция отсутствует'
        return f'{request.json}'


app.run(host='0.0.0.0', port=8087)
