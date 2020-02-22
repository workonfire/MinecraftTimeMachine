# MinecraftTimeMachine

[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=flat&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

Have you ever wanted to... go back in time within Minecraft?

If so, this app is for you! It simply reads the Minecraft chat logs files in real-time, to make the experience of going back in time more realistic.


------------



### Features
- Going back in time to an exact timestamp
- Taking to the closest time available, if logs from the specified time are not present
- Remembering the most used timestamp
- Showing timestamps in real-time chat logs
- Adjusting the chat playback speed
- Filtering logs and outputting chat messages only with certain phrases
- COLOR SUPPORT! Since Minecraft does not store colors in logs, you can define your own color variables and make the app search for certain values and replace them with the colored ones.
- *TODO: Displaying content using the Minecraft font*
- *TODO: Going back to random time*
- *TODO: Screenshots and GUI support*

### Downloads
The latest release is always available [here](https://github.com/workonfire/MinecraftTimeMachine/releases "here").

### Supported languages
- English
- Polish

### Dependencies
- [Python 3](https://www.python.org/downloads/ "Python 3")
- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation "PyYAML")
- [ciso8601](https://pypi.org/project/ciso8601/ "ciso8601")
- [pypresence](https://pypi.org/project/pypresence/ "pypresence") (optional)

### Screenshots
[![Screenshot](https://i.imgur.com/tmTHKFZ.png "Screenshot")](https://i.imgur.com/tmTHKFZ.png "Screenshot")

### Example configuration file
    selected_time: none
    logs_path: default
    show_timestamps: true
    playback_speed: 1
    filter: default
    spacing: false
    locale: en
    
    replace:
      'Buty935': "&c&lB&6&lu&e&lt&a&ly&b&l9&3&l3&9&l5&f"
      'admin': '&4admin&f'
      '*VIP*': '&6*&eVIP&6*&f'
