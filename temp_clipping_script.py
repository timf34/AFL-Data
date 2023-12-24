from moviepy.editor import VideoFileClip
import math


def split_video_into_clips(filename, clip_duration=60):
    # Load the video file
    video = VideoFileClip(filename)

    # Calculate the number of clips
    total_duration = video.duration
    num_clips = math.ceil(total_duration / clip_duration)

    for i in range(num_clips):
        # Define the start and end of the clip
        start = i * clip_duration
        end = min((i + 1) * clip_duration, total_duration)

        # Create the subclip
        clip = video.subclip(start, end)

        # Save the clip
        clip_filename = f"{filename}_clip_{i + 1}.mp4"
        clip.write_videofile(clip_filename, codec="libx264")
        print(f"Clip {i + 1} saved: {clip_filename}")


# Example usage
split_video_into_clips("marvel\\marvel-fov-3\\26_08_2023\\output.mp4")
