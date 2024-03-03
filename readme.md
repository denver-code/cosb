# [WIP] COSB - Call of Subtitle  
A simple tool to add subtitles to your video in the CoD MW I-III style.

# Example  
![example](example.png)

### Code
```python
from cosb import add_subtitles_to_video

style_file = "style.json"
video_file = "vid.mp4"
subtitle_file = "subs.json"
output_file = "output.mp4"
add_subtitles_to_video(video_file, subtitle_file, output_file, style_file)
```

# Installation
```bash
git clone https://github.com/denver-code/COSB
cd COSB
poetry install
```

# Usage
1. change the `_style.json` to `style.json` and modify it to your liking
2. change the `_subtitles_.json` to `subtitles.json` and modify it to your liking. This is the place where you can add your subtitles.
3. Provide `vid.mp4` in the root directory or rename `_vid.mp4` to `vid.mp4` to use the provided example video.

then run `main.py`, you able to modify it to your liking or create your own script.

```bash
poetry run python main.py
```

# Style
The style file is a json file that contains the following fields:
```json
{
    "nameColors": {
        "enemy": "#CD716D",
        "friednly": "#86B9E1",
        "neutral": "#C5E3BA"
    },
    "textColors": {
        "general": "#F7F7F9"
    },
    "styles":{
        "stroke": 0,
        "strokeColor": "transparent",
        "fontSize": 24
    },
    "duration": 3,
    "padding": 100
}
```

# Subtitles
```json
[
    {
        "name": "Captain Price",
        "text": "From now.... She's yours.",
        "type": "friednly",
        "startTime": "00:00:01"
    },
     {
        "name": "Graves",
        "text": "Alright, let's go.",
        "type": "enemy",
        "startTime": "00:00:02"
    }
]
```

# Plans
- [x] Add basic support for multiple characters
- [x] Render the suptitles from the file
- [x] Color of the name will be based on the type and will be different from text color
- [ ] Add support for more video formats
- [ ] Change location of the subtitles when multiple characters are speaking
- [ ] Breaking the subtitles into multiple lines when the text is too long
- [ ] GUI
- [ ] Add Custom Fonts