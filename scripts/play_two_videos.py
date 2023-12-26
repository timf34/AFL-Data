import cv2

def play_videos(video_path1, video_path2, scale=0.5):
    # Open the first video
    cap1 = cv2.VideoCapture(video_path1)
    if not cap1.isOpened():
        print("Error opening video file: ", video_path1)
        return

    # Open the second video
    cap2 = cv2.VideoCapture(video_path2)
    if not cap2.isOpened():
        print("Error opening video file: ", video_path2)
        return

    pause = False

    while True:
        if not pause:
            # Read from both videos
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()

            if not ret1 or not ret2:
                print("Finished playing the videos")
                break

            # Resize the frames
            frame1 = cv2.resize(frame1, None, fx=scale, fy=scale)
            frame2 = cv2.resize(frame2, None, fx=scale, fy=scale)

            # Display the frames in two separate windows
            cv2.imshow('Video 1', frame1)
            cv2.imshow('Video 2', frame2)

        # Wait for a key press and decide the action
        key = cv2.waitKey(25) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):  # Space bar
            pause = not pause

    # Release the video capture objects and close windows
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

# Replace with your video paths
video_path1 = r'C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-3\26_08_2023\marvel3_time_09_09_04_date_27_08_2023_\0.mp4'
video_path2 = r'C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-4\26_08_23\marvel4_time_09_09_03_date_27_08_2023_\0.mp4'

play_videos(video_path1, video_path2, scale=0.5)  # Adjust the scale as needed
