import json
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


def parse_style(style_file):
    with open(style_file, "r") as file:
        style_data = json.load(file)

    name_colors = style_data.get("nameColors", {})
    text_colors = style_data.get("textColors", {})
    styles = style_data.get("styles", {})
    padding = style_data.get("padding", 0)
    duration = style_data.get("duration", 3)

    return name_colors, text_colors, styles, padding, duration


# Function to parse time string to seconds
def parse_time(time_str):
    if ":" in time_str:
        time_parts = time_str.split(":")
        if len(time_parts) == 3:
            return (
                int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2])
            )
    return int(time_str)


# Function to load subtitle data from JSON file
def load_subtitles(subtitle_file):
    with open(subtitle_file, "r") as file:
        subtitles = json.load(file)
    return subtitles


def add_subtitles_to_video(video_file, subtitle_file, output_file, style_file):
    video_clip = VideoFileClip(video_file)
    subtitles = load_subtitles(subtitle_file)
    clips = []
    name_colors, text_colors, styles, padding, duration = parse_style(style_file)

    # Track the end time of each subtitle
    last_end_time = 0

    for subtitle in subtitles:
        start_time = parse_time(subtitle["startTime"])
        end_time = start_time + duration
        name = subtitle["name"] + ": "
        text = f"{subtitle['text']}"

        # Create the name and text clips with respective styles
        name_clip = TextClip(
            name,
            fontsize=styles.get("fontSize", 24),
            color=name_colors.get(subtitle["type"], "#C5E3BA"),
            stroke_color=styles.get("strokeColor", "transparent"),
            stroke_width=styles.get("stroke", 0),
        ).set_duration(end_time - start_time)

        text_clip = TextClip(
            text,
            fontsize=styles.get("fontSize", 24),
            color=text_colors.get("general", "#F7F7F9"),
            stroke_color=styles.get("strokeColor", "transparent"),
            stroke_width=styles.get("stroke", 0),
        ).set_duration(end_time - start_time)

        # Concatenate name and text into one line
        combined_text_clip = TextClip(
            txt=name + text,
            fontsize=styles.get("fontSize", 24),
            color="white",
            bg_color="black",
            stroke_color="black",
            stroke_width=0.5,
        ).set_duration(end_time - start_time)

        # Calculate position for centering
        x_position = (video_clip.size[0] - combined_text_clip.size[0]) / 2
        y_position = video_clip.size[1] - combined_text_clip.size[1] - padding

        # Adjust position if there is an overlap with the previous subtitle
        if start_time < last_end_time:
            # Move the old subtitle up
            y_position -= combined_text_clip.size[1]

        # Set position for name clip
        name_clip = name_clip.set_position((x_position, y_position)).set_start(
            start_time
        )

        # Set position for text clip
        text_clip = text_clip.set_position(
            (x_position + name_clip.size[0], y_position)
        ).set_start(start_time)

        clips.extend([name_clip, text_clip])

        # Update last end time
        last_end_time = end_time

    final_clip = CompositeVideoClip([video_clip] + clips)
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
