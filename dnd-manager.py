import gradio as gr
import json
from pathlib import Path
import argparse

# Create a data directory if it doesn't exist
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Directories for different character types
CHARACTERS_DIR = DATA_DIR / "characters"
CHARACTERS_DIR.mkdir(exist_ok=True)
NPCS_DIR = DATA_DIR / "npcs"
NPCS_DIR.mkdir(exist_ok=True)
ENEMIES_DIR = DATA_DIR / "enemies"
ENEMIES_DIR.mkdir(exist_ok=True)

class CharacterSheet:
    def __init__(self, character_type="player"):
        self.character_type = character_type
        self.attributes = {
            # Basic Info
            "name": "",
            "class": "",
            "level": 1,
            "race": "",
            "background": "",
            "alignment": "",
            "type": character_type,
            
            # Combat Stats
            "armor_class": 10,
            "initiative_bonus": 0,
            "speed": 30,
            "hit_points_max": 10,
            "hit_points_current": 10,
            "temporary_hp": 0,
            "hit_dice_total": "1d8",
            "hit_dice_remaining": "1d8",
            
            # Abilities
            "abilities": {
                "strength": 10,
                "dexterity": 10,
                "constitution": 10,
                "intelligence": 10,
                "wisdom": 10,
                "charisma": 10
            },
            
            # Saving Throws (proficiency)
            "saving_throws": {
                "strength": False,
                "dexterity": False,
                "constitution": False,
                "intelligence": False,
                "wisdom": False,
                "charisma": False
            },
            
            # Combat Options
            "weapons": [],
            "spellcasting_ability": "",
            "spell_save_dc": 10,
            "spell_attack_bonus": 0,
            
            # Other
            "gold": 0,  # NEW: Added gold attribute
            "equipment": "",
            "features": "",
            "spells": "",
            "proficiency_bonus": 2
        }
    
    def to_dict(self):
        return self.attributes
    
    @classmethod
    def from_dict(cls, data):
        sheet = cls(character_type=data.get("type", "player"))
        sheet.attributes = data
        return sheet

def get_directory(character_type):
    """Get the directory based on character type"""
    if character_type == "player":
        return CHARACTERS_DIR
    elif character_type == "npc":
        return NPCS_DIR
    elif character_type == "enemy":
        return ENEMIES_DIR
    else:
        return CHARACTERS_DIR  # Default to characters

def get_character_list(character_type):
    """Get list of saved characters of a specific type"""
    directory = get_directory(character_type)
    characters = [f.stem.replace('_', ' ').replace(f'-{character_type}', '') for f in directory.glob(f'*-{character_type}.json')]
    return sorted(characters)

def save_character(character_type, name, character_class, level, race, background, alignment,
                   armor_class, initiative_bonus, speed, hp_max, hp_current, temp_hp,
                   hit_dice_total, hit_dice_remaining,
                   strength, dexterity, constitution, intelligence, wisdom, charisma,
                   str_save, dex_save, con_save, int_save, wis_save, cha_save,
                   spellcasting_ability, spell_save_dc, spell_attack_bonus,
                   equipment, features, spells, proficiency_bonus,
                   gold):  # MODIFIED: Added gold parameter
    if not name:
        return ["Error: Character name is required", gr.update(choices=get_character_list(character_type), value=None)]
    
    character = CharacterSheet(character_type=character_type)
    character.attributes.update({
        "name": name,
        "class": character_class,
        "level": level,
        "race": race,
        "background": background,
        "alignment": alignment,
        "type": character_type,
        
        "armor_class": armor_class,
        "initiative_bonus": initiative_bonus,
        "speed": speed,
        "hit_points_max": hp_max,
        "hit_points_current": hp_current,
        "temporary_hp": temp_hp,
        "hit_dice_total": hit_dice_total,
        "hit_dice_remaining": hit_dice_remaining,
        
        "abilities": {
            "strength": strength,
            "dexterity": dexterity,
            "constitution": constitution,
            "intelligence": intelligence,
            "wisdom": wisdom,
            "charisma": charisma
        },
        
        "saving_throws": {
            "strength": str_save,
            "dexterity": dex_save,
            "constitution": con_save,
            "intelligence": int_save,
            "wisdom": wis_save,
            "charisma": cha_save
        },
        
        "spellcasting_ability": spellcasting_ability,
        "spell_save_dc": spell_save_dc,
        "spell_attack_bonus": spell_attack_bonus,
        
        "gold": int(gold),  # MODIFIED: Added gold to attributes
        "equipment": equipment,
        "features": features,
        "spells": spells,
        "proficiency_bonus": proficiency_bonus
    })
    
    directory = get_directory(character_type)
    file_path = directory / f"{name.lower().replace(' ', '_')}-{character_type}.json"
    with open(file_path, 'w') as f:
        json.dump(character.to_dict(), f, indent=2)
    
    # After saving, update the Dropdown with the new list and set the value to the newly saved character
    return [f"Character {name} saved successfully!", gr.update(choices=get_character_list(character_type), value=name)]

def load_character(character_type, name):
    if not name:
        return [None] * 34  # MODIFIED: Updated number of fields to 34
    
    try:
        directory = get_directory(character_type)
        file_path = directory / f"{name.lower().replace(' ', '_')}-{character_type}.json"
        with open(file_path, 'r') as f:
            data = json.load(f)
        character = CharacterSheet.from_dict(data)
        return [
            # Basic Info
            character.attributes["name"],
            character.attributes["class"],
            character.attributes["level"],
            character.attributes["race"],
            character.attributes["background"],
            character.attributes["alignment"],
            
            # Combat Stats
            character.attributes["armor_class"],
            character.attributes["initiative_bonus"],
            character.attributes["speed"],
            character.attributes["hit_points_max"],
            character.attributes["hit_points_current"],
            character.attributes["temporary_hp"],
            character.attributes["hit_dice_total"],
            character.attributes["hit_dice_remaining"],
            
            # Abilities
            character.attributes["abilities"]["strength"],
            character.attributes["abilities"]["dexterity"],
            character.attributes["abilities"]["constitution"],
            character.attributes["abilities"]["intelligence"],
            character.attributes["abilities"]["wisdom"],
            character.attributes["abilities"]["charisma"],
            
            # Saving Throws
            character.attributes["saving_throws"]["strength"],
            character.attributes["saving_throws"]["dexterity"],
            character.attributes["saving_throws"]["constitution"],
            character.attributes["saving_throws"]["intelligence"],
            character.attributes["saving_throws"]["wisdom"],
            character.attributes["saving_throws"]["charisma"],
            
            # Spellcasting
            character.attributes["spellcasting_ability"],
            character.attributes["spell_save_dc"],
            character.attributes["spell_attack_bonus"],
            
            # Other
            character.attributes["gold"],  # MODIFIED: Added gold to the load output
            character.attributes["equipment"],
            character.attributes["features"],
            character.attributes["spells"],
            character.attributes["proficiency_bonus"]
        ]
    except FileNotFoundError:
        return [None] * 34  # MODIFIED: Updated number of fields

def delete_character(character_type, character_name):
    if not character_name:
        return ["No character selected", gr.update(choices=get_character_list(character_type), value=None)]
    try:
        directory = get_directory(character_type)
        file_path = directory / f"{character_name.lower().replace(' ', '_')}-{character_type}.json"
        file_path.unlink()
        return ["Character deleted successfully!", gr.update(choices=get_character_list(character_type), value=None)]
    except FileNotFoundError:
        return ["Character not found!", gr.update(choices=get_character_list(character_type), value=None)]

def refresh_character_list(character_type):
    """Refresh the character list for the dropdown"""
    return gr.update(choices=get_character_list(character_type), value=None)

def get_all_agents_list():
    """Get a list of all agent names with types"""
    agents = []
    for character_type in ["player", "npc", "enemy"]:
        directory = get_directory(character_type)
        for f in directory.glob(f'*-{character_type}.json'):
            name = f.stem.replace('_', ' ').replace(f'-{character_type}', '')
            agents.append(f"{name} ({character_type})")
    return sorted(agents)

def battle_state_to_table(battle_state):
    """Convert battle state to table data for DataFrame"""
    table_data = []
    for agent in battle_state:
        row = [
            agent["Type"],
            agent["Name"],
            agent["Default Initiative"],
            agent["Rolled Initiative"],
            agent["Total Initiative"],
            agent["Armor Class"],
            agent["HP"],
            agent["Damage Taken"]
        ]
        table_data.append(row)
    return table_data

def add_agent_to_battle(agent_selection, battle_state):
    if not battle_state:
        battle_state = []
    
    if not agent_selection:
        return battle_state, battle_state_to_table(battle_state)
    
    # Parse the agent name and type
    if '(' in agent_selection and agent_selection.endswith(')'):
        name, type_with_paren = agent_selection.rsplit(' (', 1)
        character_type = type_with_paren[:-1]  # Remove the closing ')'
    else:
        return battle_state, battle_state_to_table(battle_state)  # Invalid selection
    
    # Load the character sheet
    try:
        directory = get_directory(character_type)
        file_path = directory / f"{name.lower().replace(' ', '_')}-{character_type}.json"
        with open(file_path, 'r') as f:
            data = json.load(f)
        character = CharacterSheet.from_dict(data)
    except FileNotFoundError:
        return battle_state, battle_state_to_table(battle_state)  # Character not found
    
    # Check if agent is already in battle (only for non-enemies)
    if character_type != "enemy":
        for agent in battle_state:
            if agent['Type'] == character_type and agent['Name'] == name:
                return battle_state, battle_state_to_table(battle_state)  # Agent already in battle
    
    # Extract necessary information
    agent = {
        "Type": character_type,
        "Name": name,
        "Default Initiative": character.attributes.get("initiative_bonus", 0),
        "Rolled Initiative": 0,
        "Total Initiative": 0,  # Will be calculated
        "Armor Class": character.attributes.get("armor_class", 10),
        "HP": character.attributes.get("hit_points_current", 10),
        "Damage Taken": 0
    }
    
    # Create a new battle_state
    new_battle_state = battle_state + [agent]
    
    # Return updated battle state and table data
    return new_battle_state, battle_state_to_table(new_battle_state)

def start_battle(battle_state, battle_table_data):
    """Start the battle by calculating Total Initiative and sorting agents"""
    # Check if battle_state is empty
    if not battle_state:
        return battle_state, battle_table_data  # No agents to process
    
    # Ensure battle_table_data does not exceed battle_state length
    battle_table_data = battle_table_data[:len(battle_state)]
    
    # Create a new battle_state
    new_battle_state = []
    
    # Update battle_state with data from battle_table_data
    for i, agent in enumerate(battle_state):
        row = battle_table_data[i]
        # Create a copy of the agent to avoid modifying the original
        agent = agent.copy()
        # Convert Rolled Initiative to integer, handle empty or invalid input
        try:
            agent["Rolled Initiative"] = int(row[3])
        except (ValueError, TypeError, IndexError):
            agent["Rolled Initiative"] = 0  # Default to 0 if invalid input
    
        agent["Total Initiative"] = agent["Default Initiative"] + agent["Rolled Initiative"]
        agent["Damage Taken"] = 0  # Reset Damage Taken
        new_battle_state.append(agent)
    
    # Sort agents by Total Initiative
    new_battle_state.sort(key=lambda x: x["Total Initiative"], reverse=True)
    
    # Update battle_table_data
    table_data = battle_state_to_table(new_battle_state)
    
    return new_battle_state, table_data

def advance_turn(battle_state, battle_table_data, collected_gold, collected_items):
    """Advance the turn, apply damage, remove defeated agents, and accumulate gold/items"""
    if not battle_state:
        return battle_state, battle_table_data, collected_gold, collected_items, collected_gold, collected_items
    
    # Create a new battle_state and list of defeated agents
    new_battle_state = []
    defeated_agents = []
    
    for i, agent in enumerate(battle_state):
        row = battle_table_data[i]
        agent = agent.copy()
        # Convert Damage Taken to integer, handle empty or invalid input
        try:
            agent["Damage Taken"] = int(row[7])
        except (ValueError, TypeError, IndexError):
            agent["Damage Taken"] = 0  # Default to 0 if invalid input
        
        # Subtract damage taken from HP
        agent["HP"] -= agent["Damage Taken"]
        if agent["HP"] < 0:
            agent["HP"] = 0  # Don't allow negative HP
        
        if agent["HP"] > 0:
            new_battle_state.append(agent)
        else:
            defeated_agents.append(agent)
    
    # Accumulate gold and items from defeated agents
    for agent in defeated_agents:
        name = agent["Name"]
        character_type = agent["Type"]
        directory = get_directory(character_type)
        file_path = directory / f"{name.lower().replace(' ', '_')}-{character_type}.json"
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            character = CharacterSheet.from_dict(data)
            # Accumulate gold
            gold = character.attributes.get("gold", 0)
            collected_gold += gold
            # Accumulate items
            equipment_str = character.attributes.get("equipment", "")
            if equipment_str:
                # Assuming equipment is separated by commas or newlines
                items = [item.strip() for item in equipment_str.replace(',', '\n').split('\n') if item.strip()]
                if collected_items:
                    collected_items += "\n" + "\n".join(items)
                else:
                    collected_items = "\n".join(items)
        except FileNotFoundError:
            pass  # Character not found, skip
    
    if not new_battle_state:
        table_data = []
    else:
        # Rotate turn order: move first agent to end
        new_battle_state = new_battle_state[1:] + [new_battle_state[0]]
        # Clear damage taken
        for agent in new_battle_state:
            agent["Damage Taken"] = 0
    
        table_data = battle_state_to_table(new_battle_state)
    
    return new_battle_state, table_data, collected_gold, collected_items, collected_gold, collected_items  # RETURN BOTH STATE AND DISPLAY

def reset_battle():
    """Reset the battle state, accumulated gold, and collected items"""
    return [], [], 0, "", 0, ""  # MODIFIED: Reset battle_state, battle_table, collected_gold, collected_items, gold_display, items_display

# Theme mapping
THEMES = {
    "Default": gr.themes.Default(),
    "Monochrome": gr.themes.Monochrome(),
    "Soft": gr.themes.Soft(),
    "Glass": gr.themes.Glass(),
    "Citrus": gr.themes.Citrus(),
    "Ocean": gr.themes.Ocean(),
    "Origin": gr.themes.Origin(),
    "Base": gr.themes.Base(),
}

def main():
    # Argument parser for theme selection
    parser = argparse.ArgumentParser(description="D&D Character Manager")
    parser.add_argument(
        "--theme",
        type=str,
        default="Default",
        help="Select the theme for the app. Can be a built-in theme or a Hugging Face Hub theme (e.g., 'NoCrypt/miku')",
    )
    args = parser.parse_args()

    # Initialize the selected theme
    if args.theme in THEMES:
        selected_theme = THEMES[args.theme]
    else:
        # Attempt to load the theme from the Hugging Face Hub
        try:
            selected_theme = gr.themes.ThemeClass.from_hub(args.theme)
            print(f"Loaded theme '{args.theme}' from Hugging Face Hub.")
        except Exception as e:
            print(f"Error loading theme '{args.theme}': {e}")
            print("Using default theme.")
            selected_theme = gr.themes.Default()

    # Gradio Interface
    with gr.Blocks(theme=selected_theme) as demo:
        gr.Markdown("# D&D Character Manager")

        with gr.Tabs():
            with gr.Tab("Battle"):
                gr.Markdown("### Battle Tracker")

                # State for battle participants
                battle_state = gr.State([])
                # NEW: States for accumulated gold and collected items
                collected_gold = gr.State(0)
                collected_items = gr.State("")

                # Refresh agent list
                agent_list = get_all_agents_list()

                with gr.Row():
                    agent_dropdown = gr.Dropdown(
                        label="Select Agent to Add",
                        choices=agent_list,
                        interactive=True
                    )
                    add_agent_btn = gr.Button("Add Agent")

                battle_table = gr.Dataframe(
                    headers=["Type", "Name", "Default Initiative", "Rolled Initiative", "Total Initiative", "Armor Class", "HP", "Damage Taken"],
                    datatype=["str", "str", "number", "number", "number", "number", "number", "number"],
                    interactive=True,
                    value=[],
                    type="array"  # Ensure the data is a list of lists
                )

                with gr.Row():
                    start_battle_btn = gr.Button("Start Battle", variant="primary")
                    next_turn_btn = gr.Button("Next Turn")
                    reset_battle_btn = gr.Button("Reset Battle", variant="secondary")

                # NEW: Display areas for accumulated gold and collected items
                with gr.Row():
                    gold_display = gr.Number(label="Total Gold Collected", value=0, interactive=False)
                    items_display = gr.Textbox(label="Collected Items", value="", lines=3, interactive=False)

                # Event handlers
                add_agent_btn.click(
                    fn=add_agent_to_battle,
                    inputs=[agent_dropdown, battle_state],
                    outputs=[battle_state, battle_table]
                )

                start_battle_btn.click(
                    fn=start_battle,
                    inputs=[battle_state, battle_table],
                    outputs=[battle_state, battle_table]
                )

                next_turn_btn.click(
                    fn=advance_turn,
                    inputs=[battle_state, battle_table, collected_gold, collected_items],  # Inputs
                    outputs=[battle_state, battle_table, collected_gold, collected_items, gold_display, items_display]    # Outputs mapped to both State and display components
                )

                reset_battle_btn.click(
                    fn=reset_battle,
                    inputs=[],
                    outputs=[battle_state, battle_table, collected_gold, collected_items, gold_display, items_display]    # Reset battle_state, battle_table, gold, and items
                )

            for character_type in ["player", "npc", "enemy"]:
                tab_label = character_type.capitalize() + "s"
                with gr.Tab(tab_label):
                    with gr.Row():
                        # Column 1: Basic Info
                        with gr.Column():
                            name = gr.Textbox(label="Character Name")
                            character_class = gr.Textbox(label="Class")
                            level = gr.Number(label="Level", value=1, minimum=1)
                            race = gr.Textbox(label="Race")
                            background = gr.Textbox(label="Background")
                            alignment = gr.Dropdown(
                                label="Alignment",
                                choices=["Lawful Good", "Neutral Good", "Chaotic Good",
                                         "Lawful Neutral", "True Neutral", "Chaotic Neutral",
                                         "Lawful Evil", "Neutral Evil", "Chaotic Evil"]
                            )
                            proficiency_bonus = gr.Number(label="Proficiency Bonus", value=2, minimum=2)

                        # Column 2: Combat Stats
                        with gr.Column():
                            gr.Markdown("### Combat Statistics")
                            armor_class = gr.Number(label="Armor Class", value=10, minimum=0)
                            initiative_bonus = gr.Number(label="Initiative Bonus", value=0)
                            speed = gr.Number(label="Speed", value=30)
                            hp_max = gr.Number(label="Max Hit Points", value=10, minimum=1)
                            hp_current = gr.Number(label="Current Hit Points", value=10)
                            temp_hp = gr.Number(label="Temporary Hit Points", value=0, minimum=0)
                            hit_dice_total = gr.Textbox(label="Hit Dice Total", value="1d8")
                            hit_dice_remaining = gr.Textbox(label="Hit Dice Remaining", value="1d8")

                        # Column 3: Ability Scores
                        with gr.Column():
                            gr.Markdown("### Ability Scores")
                            strength = gr.Slider(label="Strength", minimum=1, maximum=20, step=1, value=10)
                            dexterity = gr.Slider(label="Dexterity", minimum=1, maximum=20, step=1, value=10)
                            constitution = gr.Slider(label="Constitution", minimum=1, maximum=20, step=1, value=10)
                            intelligence = gr.Slider(label="Intelligence", minimum=1, maximum=20, step=1, value=10)
                            wisdom = gr.Slider(label="Wisdom", minimum=1, maximum=20, step=1, value=10)
                            charisma = gr.Slider(label="Charisma", minimum=1, maximum=20, step=1, value=10)

                    with gr.Row():
                        # Saving Throws
                        with gr.Column():
                            gr.Markdown("### Saving Throw Proficiencies")
                            str_save = gr.Checkbox(label="Strength Saving Throw")
                            dex_save = gr.Checkbox(label="Dexterity Saving Throw")
                            con_save = gr.Checkbox(label="Constitution Saving Throw")
                            int_save = gr.Checkbox(label="Intelligence Saving Throw")
                            wis_save = gr.Checkbox(label="Wisdom Saving Throw")
                            cha_save = gr.Checkbox(label="Charisma Saving Throw")

                        # Spellcasting
                        with gr.Column():
                            gr.Markdown("### Spellcasting")
                            spellcasting_ability = gr.Dropdown(
                                label="Spellcasting Ability",
                                choices=["", "Intelligence", "Wisdom", "Charisma"]
                            )
                            spell_save_dc = gr.Number(label="Spell Save DC", value=10)
                            spell_attack_bonus = gr.Number(label="Spell Attack Bonus", value=0)

                    with gr.Row():
                        with gr.Column():
                            equipment = gr.Textbox(label="Equipment", lines=3)
                            features = gr.Textbox(label="Features & Traits", lines=3)
                            spells = gr.Textbox(label="Spells", lines=3)
                            gold = gr.Number(label="Gold", value=0, minimum=0)  # NEW: Added Gold input

                    with gr.Row():
                        save_btn = gr.Button("Save Character", variant="primary")
                        load_dropdown = gr.Dropdown(
                            label="Load Character",
                            choices=get_character_list(character_type),
                            interactive=True
                        )
                        load_btn = gr.Button("Load")
                        delete_btn = gr.Button("Delete Character", variant="danger")
                        refresh_btn = gr.Button("Refresh Character List", variant="secondary")

                    output = gr.Textbox(label="Status", interactive=False)

                    # Event handlers
                    save_btn.click(
                        fn=save_character,
                        inputs=[
                            gr.State(character_type),
                            name, character_class, level, race, background, alignment,
                            armor_class, initiative_bonus, speed, hp_max, hp_current, temp_hp,
                            hit_dice_total, hit_dice_remaining,
                            strength, dexterity, constitution, intelligence, wisdom, charisma,
                            str_save, dex_save, con_save, int_save, wis_save, cha_save,
                            spellcasting_ability, spell_save_dc, spell_attack_bonus,
                            equipment, features, spells, proficiency_bonus,
                            gold  # MODIFIED: Added gold to inputs
                        ],
                        outputs=[output, load_dropdown]
                    )

                    load_btn.click(
                        fn=load_character,
                        inputs=[gr.State(character_type), load_dropdown],
                        outputs=[
                            name, character_class, level, race, background, alignment,
                            armor_class, initiative_bonus, speed, hp_max, hp_current, temp_hp,
                            hit_dice_total, hit_dice_remaining,
                            strength, dexterity, constitution, intelligence, wisdom, charisma,
                            str_save, dex_save, con_save, int_save, wis_save, cha_save,
                            spellcasting_ability, spell_save_dc, spell_attack_bonus,
                            gold,  # MODIFIED: Mapped gold to output
                            equipment, features, spells, proficiency_bonus
                        ]
                    )

                    delete_btn.click(
                        fn=delete_character,
                        inputs=[gr.State(character_type), load_dropdown],
                        outputs=[output, load_dropdown]
                    )

                    refresh_btn.click(
                        fn=refresh_character_list,
                        inputs=[gr.State(character_type)],
                        outputs=[load_dropdown]
                    )

        # Move the theme selection information to the bottom
        with gr.Row():
            gr.Markdown("### Theme Selection")
            gr.Markdown("To change the theme, restart the app with the `--theme` argument.")
            gr.Markdown("You can use built-in themes or themes from the Hugging Face Hub (e.g., 'NoCrypt/miku').")
            built_in_themes = ", ".join(THEMES.keys())
            gr.Markdown(f"Built-in themes: {built_in_themes}")

        demo.launch()

if __name__ == "__main__":
    main()
