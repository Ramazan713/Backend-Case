import requests as rq
import json



class DataPokemon:
    def __init__(self) -> None:
        self.pokemons=[]

    # return generator object which produce list of json contains pokemon's name and pokemon's image_url
    # way of working => '[' yield firstly, then all data send as '{...},{...}' after that ']' yield. finally output becomes like '[{...},{...}]'  
    def getAllPokemons(self,getChache=False):

        try:
            if self.pokemons and getChache:
                yield json.dumps(self.pokemons)
                return

            yield '['
            self.pokemons.clear()

            limit=20
            next_url=f'https://pokeapi.co/api/v2/pokemon?limit={limit}'
            
            while next_url:
                response=rq.get(next_url)
                response_dict=response.json()
                next_url=response_dict["next"]
                previous_url=response_dict['previous']
                
                pokemons_text=',' if previous_url else ''

                for result in response_dict["results"]:
                    name=result["name"]
                    pokeman_url=result["url"]

                    pokemon_response=rq.get(pokeman_url)
                    pokemon_dict=pokemon_response.json()
                    image_url=pokemon_dict["sprites"]["back_default"]
                    data={"name":name,"image_url":image_url}
                    self.pokemons.append(data)
                    pokemons_text+=json.dumps(data)+','

                pokemons_text=pokemons_text[:len(pokemons_text)-1]
                    
                yield pokemons_text
                  
            yield ']'
        except Exception as e:
            yield ']'
    
    # return dictionary pokemon features accordingly name
    def getPokemon(self,name):
        url=f'https://pokeapi.co/api/v2/pokemon/{name}'
        response=rq.get(url)
        response_dict=response.json()
        image_url=response_dict["sprites"]["back_default"]
        abilities=[]
        for ability_dict in response_dict["abilities"]:
            abilities.append(ability_dict["ability"]["name"])
        return {'name':name,'image_url':image_url,'abilities':abilities}






