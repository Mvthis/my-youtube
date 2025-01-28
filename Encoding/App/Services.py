import subprocess
import requests


def encoding(video_path, video_id):
    try:
        if video_path.endswith('.mp4'):
            # Define the output path
            output_path = video_path.split('.mp4')[0]

            # Define the target resolutions
            resolutions = ["1920x1080", "1280x720",
                           "854x480", "640x360", "426x240"]
            path = []

            # Get the resolution of the original video
            cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {video_path}'
            resolution = subprocess.check_output(
                cmd, shell=True).decode().strip()

            # Generate copies of the video for each resolution, unless they are higher than the original resolution
            for target_resolution in resolutions:
                if int(target_resolution.split('x')[0]) <= int(resolution.split('x')[0]):
                    # FFmpeg command for encoding to mp4 with the specified resolution

                    cmd = (
                        f"ffmpeg -i {video_path} -vf scale={target_resolution} -c:v libx264 -crf 23 -c:a aac -strict -2 "
                        f"{output_path}_{target_resolution}.mp4"
                    )

                    path = f"{output_path}_{target_resolution}.mp4"

                    # Execute the FFmpeg command
                    subprocess.run(cmd, shell=True)

                    requests.post('http://localhost:5432/video/'+video_id,
                                  data={"video_path": path, "resolution": target_resolution})

            return True, "Encoding successful."
        else:
            return False, "Invalid file format. Only .mp4 files are supported."

    except Exception as e:
        return False, f"An error occurred during encoding: {str(e)}"
