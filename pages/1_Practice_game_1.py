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
initial_quest_seed = 42
initial_num_characters = 4

if 'num_characters' not in st.session_state:
    st.session_state['num_characters'] = initial_num_characters

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
    

def gen_quest(characters, graph, sounds, size = 8):
    char_id = random.randint(0, len(characters) - 1)
    character = (characters[char_id], sounds[char_id])
    st.session_state['quest_character'] = character
    character_neighbors = gen_character_neighbour(character[0], graph, size - 1)
    quest = [character] + [add_sound(ch, characters, sounds) for ch in character_neighbors]
    random.shuffle(quest)
    st.session_state['quest'] = quest
    return character
    

def gen_interface():
    graph = load_graph_db()
    characters, sounds = load_dataset()

    if 'seed' not in st.session_state:
        st.session_state['seed'] = random.randint(0, 1000)
        random.seed(st.session_state['seed'])
        
        quest_character = gen_quest(characters, graph, sounds, size = st.session_state['num_characters'])
        st.session_state['images'] = [gen_character_image(char[0], W, H, font) 
                for char in st.session_state['quest']]
        #print(st.session_state['quest_character'])
        #print(st.session_state['quest'])
        
    if st.button("next question"):
        st.session_state['seed'] += 1 % 10000000
        random.seed(st.session_state['seed'])        
        quest_character = gen_quest(characters, graph, sounds, size = st.session_state['num_characters'])
        st.session_state['images'] = [gen_character_image(char[0], W, H, font) 
                for char in st.session_state['quest']] 
        #print(st.session_state['quest_character'])
        #print(st.session_state['quest'])

    question = f'<p style="font-family:sans-serif; text-align:center; font-size: 42px;">which symbol is {st.session_state["quest_character"][1]}?</p>'
    st.markdown(question, unsafe_allow_html=True)

    st.session_state['img'] = image_select(
        label="Select a character",
        images=st.session_state['images'],
        index=-1,  
        use_container_width = False,
        return_value='index'
    )

    if (st.session_state['img'] != -1):
        if st.session_state['quest'][st.session_state['img']] == st.session_state['quest_character']:
            st.write('correct!')
        else:
            st.write('wrong answer')


gen_interface()
