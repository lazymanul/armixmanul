import streamlit as st
from PIL import ImageFont, Image, ImageDraw
from streamlit_image_select import image_select
import pickle
import random
import networkx as nx

# Character image generation routine

fsize = 250
W = 320
H = 320
font = ImageFont.truetype("assets/NotoSansCJK-Regular.ttc", fsize)

def gen_character_image(character, W, H, font):
    """Generates image for given character    
    """
    image = Image.new('L', (W, H), color=255)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), character, font=font)
    draw.text((w/1.5,h/2), character, anchor="mm", font=font)    
    return image


# Load data

@st.cache_data
def load_dataset():
    characters_file_name = "assets/characters.txt"
    sound_file_name = "assets/characters_sound.txt"
    with open(characters_file_name) as f:
        characters = f.read().split(' ')

    with open(sound_file_name) as f:
        sounds = f.read().split(' ')
    return characters, sounds


@st.cache_data
def load_graph_db():
    db_file_name = "assets/similarity_db.pkl"
    graph = pickle.load(open(db_file_name, 'rb'))   
    return graph


def gen_character_neighbour(character, graph, size=8):
    character_neighbors = len([n for n in graph.neighbors(character)])
    neighbors_num = min(character_neighbors, size)
    similar_characters = list(graph.neighbors(character))
    weights = [graph[character][node]['weight'] for node in similar_characters]
    sorted_similar_characters = [x for _, x in sorted(zip(weights, similar_characters), key=lambda pair: pair[0])]
    return sorted_similar_characters[:neighbors_num]

    
def add_sound(char, characters, sounds):    
    idx = characters.index(char)
    return (char, sounds[idx])
    

def gen_quest(characters, graph, sounds):    
    char_id = random.randint(0, len(characters) - 1)
    character = (characters[char_id], sounds[char_id])
    st.session_state['quest_character'] = character
    character_neighbors = gen_character_neighbour(character[0], graph)
    quest = [character] + [add_sound(ch, characters, sounds) for ch in character_neighbors]
    random.shuffle(quest)
    st.session_state['neighbourhood'] = quest
    return character


random.seed(42)
graph = load_graph_db()
characters, sounds = load_dataset()
if ('quest_character' not in st.session_state):
    quest_character = gen_quest(characters, graph, sounds)
    #print(st.session_state['neighbourhood'])

question = f'<p style="font-family:sans-serif; text-align:center; font-size: 42px;">which one is {st.session_state["quest_character"][1]}?</p>'
st.markdown(question, unsafe_allow_html=True)

#print(add_sound(st.session_state['quest_character'][0], characters, sounds))
#print(add_sound(st.session_state['neighbourhood'][0], characters, sounds))


img = image_select(
    label="Select a character",
    images=[        
        gen_character_image(char[0], W, H, font) 
            for char in st.session_state['neighbourhood']
    ],  
    index=-1,  
    use_container_width = False,
    return_value='index'
)

if (img != -1):
    if st.session_state['neighbourhood'][img] == st.session_state['quest_character']:
        st.write('correct!')
    else:
        st.write('wrong answer')




