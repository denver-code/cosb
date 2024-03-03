from cosb import add_subtitles_to_video


style_file = "style.json"
video_file = "vid.mp4"
subtitle_file = "subs.json"
output_file = "output.mp4"
add_subtitles_to_video(video_file, subtitle_file, output_file, style_file)
