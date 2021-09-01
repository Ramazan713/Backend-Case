from flask import Flask
from flask import make_response,jsonify,stream_with_context

from dataPokemon import DataPokemon

app=Flask(__name__)

dt=DataPokemon()


@app.route('/pokemons',methods=["GET"])
def index():
    return app.response_class(stream_with_context(dt.getAllPokemons(False)),mimetype='application/json')

@app.route("/pokemon/<name>",methods=['GET'])
def info(name):
    try:
        rs=dt.getPokemon(name)
        return make_response(jsonify(rs),200)
    except Exception as e:
        return make_response(jsonify(error='some error occured'),400)
    


if __name__=='__main__':
    app.run()