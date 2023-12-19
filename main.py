import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

url = "https://dnd5eapi.co/api/spells"
headers = {'Accept': 'application/json'}
response = requests.get(url=url, headers=headers)

if response.status_code == 200:
    spells_data = response.json()
    spells = spells_data['results']


@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template(template_name_or_list="index.html",
                               spells_data=spells_data,
                               spells=spells,
                               request=request
                               )
    else:
        spell = request.form['search_spell']
        return redirect(url_for('search_spells', user_spell=spell))


@app.route('/list_spells')
def list_spells():
    return render_template(template_name_or_list='spell-list.html',
                           spells=spells)


@app.route('/spell_search/<user_spell>')
def search_spells(user_spell):
    matching_spell = [spell for spell in spells if spell['name'].lower() == user_spell.lower()]
    spell_url = matching_spell[0]['url']

    search_header = {'Accept': 'application/json'}
    search_response = requests.get(url='https://dnd5eapi.co' + spell_url, headers=search_header)
    if search_response.status_code == 200:
        spell_data = search_response.json()
        classes = [dnd_class['name'] for dnd_class in spell_data['classes']]
        return render_template(template_name_or_list='spell-search.html',
                               spell_data=spell_data,
                               classes=classes
                               )


if __name__ == "__main__":
    app.run(debug=True)
