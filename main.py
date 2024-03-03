import json
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


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


def add_subtitles_to_video(video_file, subtitle_file, output_file, padding=100):
    video_clip = VideoFileClip(video_file)
    subtitles = load_subtitles(subtitle_file)
    clips = []

    for subtitle in subtitles:
        start_time = parse_time(subtitle["startTime"])
        end_time = start_time + 3
        name = subtitle["name"] + ": "
        text = f"{subtitle['text']}"

        # Create the name and text clips with respective styles
        name_clip = TextClip(
            name,
            fontsize=24,
            color="#86B9E1",  # Blue color
        ).set_duration(end_time - start_time)

        text_clip = TextClip(
            text,
            fontsize=24,
            color="white",
        ).set_duration(end_time - start_time)

        # Concatenate name and text into one line
        combined_text_clip = TextClip(
            txt=name + text,
            fontsize=24,
        ).set_duration(end_time - start_time)

        # Calculate position for centering
        x_position = (video_clip.size[0] - combined_text_clip.size[0]) / 2
        y_position = video_clip.size[1] - combined_text_clip.size[1] - padding

        # Set position for name clip
        name_clip = name_clip.set_position((x_position, y_position)).set_start(
            start_time
        )

        # Set position for text clip
        text_clip = text_clip.set_position(
            (x_position + name_clip.size[0], y_position)
        ).set_start(start_time)

        clips.extend([name_clip, text_clip])

    final_clip = CompositeVideoClip([video_clip] + clips)
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")


# Example usage
video_file = "vid.mp4"
subtitle_file = "subs.json"
output_file = "output.mp4"
add_subtitles_to_video(video_file, subtitle_file, output_file)
