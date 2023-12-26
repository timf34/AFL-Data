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
    forward_a_frame = False
    frame_number1 = 0
    frame_number2 = 0

    while True:
        if not pause or forward_a_frame:
            # Read from both videos
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()

            if not ret1 or not ret2:
                print("Finished playing the videos")
                break

            # Resize the frames
            frame1 = cv2.resize(frame1, None, fx=scale, fy=scale)
            frame2 = cv2.resize(frame2, None, fx=scale, fy=scale)

            # Increment frame numbers
            frame_number1 += 1
            frame_number2 += 1

        # Put frame number text
        cv2.putText(frame1, f'Frame: {frame_number1}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame2, f'Frame: {frame_number2}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display the frames in two separate windows
        cv2.imshow('Video 1', frame1)
        cv2.imshow('Video 2', frame2)

        # Wait for a key press and decide the action
        key = cv2.waitKey(25) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' ') or forward_a_frame:  # Space bar for pause, or pause if moving forward a frame
            pause = not pause
            forward_a_frame = False
        elif key == ord('d') and pause:  # Move forward
            forward_a_frame = True
            pause = False  # unpause to get the next frame
        elif key == ord('a') and pause:  # Move backward
            frame_number1 = max(0, frame_number1 - 2)
            frame_number2 = max(0, frame_number2 - 2)
            cap1.set(cv2.CAP_PROP_POS_FRAMES, frame_number1)
            cap2.set(cv2.CAP_PROP_POS_FRAMES, frame_number2)

            # Read and display the new frame immediately
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()
            if ret1 and ret2:
                frame1 = cv2.resize(frame1, None, fx=scale, fy=scale)
                frame2 = cv2.resize(frame2, None, fx=scale, fy=scale)
                cv2.putText(frame1, f'Frame: {frame_number1}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame2, f'Frame: {frame_number2}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('Video 1', frame1)
                cv2.imshow('Video 2', frame2)

    # Release the video capture objects and close windows
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

# Replace with your video paths
video_path1 = r'C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-3\26_08_2023\marvel3_time_09_09_04_date_27_08_2023_\0.mp4'
video_path2 = r'C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-4\26_08_23\marvel4_time_09_09_03_date_27_08_2023_\0.mp4'

play_videos(video_path1, video_path2, scale=0.5)  # Adjust the scale as needed
