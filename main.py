import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap

# init flask app and bootstrap
app = Flask(__name__)
Bootstrap(app)

CLASSES = [('barbarian', 'For some, their rage springs from a communion with fierce animal spirits. Others draw from a roiling reservoir of anger at a world full of pain. For every barbarian, rage is a power that fuels not just a battle frenzy but also uncanny reflexes, resilience, and feats of strength.'),
           ('bard', 'Whether scholar, skald, or scoundrel, a bard weaves magic through words and music to inspire allies, demoralize foes, manipulate minds, create illusions, and even heal wounds. The bard is a master of song, speech, and the magic they contain.'),
           ('cleric', 'Clerics are intermediaries between the mortal world and the distant planes of the gods. As varied as the gods they serve, clerics strive to embody the handiwork of their deities. No ordinary priest, a cleric is imbued with divine magic.'),
           ('druid', "Whether calling on the elemental forces of nature or emulating the creatures of the animal world, druids are an embodiment of nature's resilience, cunning, and fury. They claim no mastery over nature, but see themselves as extensions of nature's indomitable will."),
           ('fighter', 'Fighters share an unparalleled mastery with weapons and armor, and a thorough knowledge of the skills of combat. They are well acquainted with death, both meting it out and staring it defiantly in the face.'),
           ('monk', 'Monks are united in their ability to magically harness the energy that flows in their bodies. Whether channeled as a striking display of combat prowess or a subtler focus of defensive ability and speed, this energy infuses all that a monk does.'),
           ('paladin', "Whether sworn before a god's altar and the witness of a priest, in a sacred glade before nature spirits and fey beings, or in a moment of desperation and grief with the dead as the only witness, a paladin's oath is a powerful bond."),
           ('ranger', 'Far from the bustle of cities and towns, past the hedges that shelter the most distant farms from the terrors of the wild, amid the dense-packed trees of trackless forests and across wide and empty plains, rangers keep their unending watch.'),
           ('rogue', "Rogues rely on skill, stealth, and their foes' vulnerabilities to get the upper hand in any situation. They have a knack for finding the solution to just about any problem, demonstrating a resourcefulness and versatility that is the cornerstone of any successful adventuring party."),
           ('sorcerer', 'Sorcerers carry a magical birthright conferred upon them by an exotic bloodline, some otherworldly influence, or exposure to unknown cosmic forces. No one chooses sorcery; the power chooses the sorcerer.'),
           ('warlock', 'Warlocks are seekers of the knowledge that lies hidden in the fabric of the multiverse. Through pacts made with mysterious beings of supernatural power, warlocks unlock magical effects both subtle and spectacular.'),
           ('wizard', 'Wizards are supreme magic-users, defined and united as a class by the spells they cast. Drawing on the subtle weave of magic that permeates the cosmos, wizards cast spells of explosive fire, arcing lightning, subtle deception, brute-force mind control, and much more.')]

# make api request
url = "https://dnd5eapi.co/api/"
headers = {'Accept': 'application/json'}
ranger_spells = []

response = requests.get(url=url + "spells", headers=headers)
if response.status_code == 200:
    all_spells_data = response.json()
    spells = all_spells_data['results']
    spell_names = [spell['index'] for spell in spells]


# home route
@app.route('/', methods=["GET", "POST"])
def home_page():
    """check if a user makes a search request, if so redirect to search page.
    if not render home page"""

    if request.method == "GET":
        return render_template(template_name_or_list="index.html",
                               spells_data=all_spells_data,
                               spells=spells,
                               request=request,
                               classes=CLASSES
                               )
    else:
        spell = request.form['search_spell']
        return redirect(url_for('search_spells',
                                user_spell=spell,
                                ))


@app.route('/about')
def about_page():
    """Renders the about page"""
    return render_template(template_name_or_list='about.html')


# route to list all spells
@app.route('/list-spells')
def list_spells():
    """render webpage for a list of all spells in spellbook"""
    return render_template(template_name_or_list='spell-list.html',
                           spells=spells,
                           )


# route for ranger spells
@app.route('/<class_name>', methods=['GET'])
def class_info(class_name):
    """render webpage for class data"""
    class_spells = []
    total_spells = 0
    class_resources = []
    class_response = requests.get(url=f"{url}classes/{class_name}/levels", headers=headers)

    if class_response.status_code == 200:
        class_resources = class_response.json()

    # if class_response.status_code == 200:
    #     total_spells = class_response.json()['count']
    #     class_spells = class_response.json()['results']
    #     if total_spells == 0:
    #         return render_template('class-spells.html',
    #                                class_name=class_name)

    return render_template(template_name_or_list='class-spells.html',
                           class_name=class_name,
                           class_resources=class_resources,
                           )


# route for spell search
@app.route('/spell-search/<user_spell>')
def search_spells(user_spell):
    """search for matching spell and make request to the api for spell data.
    render front-end and provide spell and class data"""
    matching_spell = [spell for spell in spells if spell['name'].lower() == user_spell.lower()]
    spell_url = matching_spell[0]['url']

    search_header = {'Accept': 'application/json'}
    search_response = requests.get(url='https://dnd5eapi.co' + spell_url, headers=search_header)
    if search_response.status_code == 200:
        spell_data = search_response.json()
        classes = [dnd_class['name'] for dnd_class in spell_data['classes']]
        return render_template(template_name_or_list='spell-search.html',
                               spell_data=spell_data,
                               classes=classes,
                               )


if __name__ == "__main__":
    app.run(debug=True)
