# DMBuddy

DMBuddy is a Python-based tool for Dungeon Masters to help manage their D&D campaigns.

## Prerequisites

- Python 3.10 or higher
- Git (optional, for cloning the repository)

## Getting the Files

You can get DMBuddy in one of two ways:

1. **Clone with Git:**
   ```bash
   git clone https://github.com/psdwizzard/DMBuddy
   cd DMBuddy
   ```

2. **Direct Download:**
   - Download the repository files from GitHub
   - Extract them to your desired location

## Installation

Choose one of these installation methods:

### Automatic Installation (Recommended)
1. Navigate to the DMBuddy folder
2. Double-click `install.bat`
3. Wait for the installation to complete

That's it! The script will:
- Create a virtual environment (dnd-env)
- Install all required dependencies
- Set up everything you need to run DMBuddy

### Manual Installation
If you prefer to install manually or are not using Windows, follow these steps:

1. Open a terminal in the DMBuddy folder
2. Create a virtual environment:
   ```bash
   python -m venv dnd-env
   ```
3. Activate the virtual environment:
   - Windows: `dnd-env\Scripts\activate.bat`
   - Linux/Mac: `source dnd-env/bin/activate`
4. Update pip:
   ```bash
   python -m pip install --upgrade pip
   ```
5. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Running DMBuddy

1. **Easy Start (Windows)**
   - Double-click `RunDMrun.bat`
   - DMBuddy will start with the default theme

2. **Manual Start**
   - Activate the virtual environment:
     - Windows: `dnd-env\Scripts\activate.bat`
     - Linux/Mac: `source dnd-env/bin/activate`
   - Run:
     ```bash
     python dnd-manager.py --theme psdwizzard/DnDBuddy
     ```

## Customizing the Theme

To use a different theme, edit `RunDMrun.bat` and modify the theme parameter:
```batch
python dnd-manager.py --theme your/preferred/theme
```

## Dependencies

- gradio (version 5.0.0 or higher)
- python-json-logger (version 2.0.0 or higher)

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/psdwizzard/DMBuddy).
