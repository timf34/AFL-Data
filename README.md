# AFL-Data

### Compression used 

```
ffmpeg -i marvel3_time_09_09_04_date_27_08_2023_.avi -c:v libx264 -preset slow -crf 23 -r 30 output.mp4
```


### Useful scripts 

`remove_frames_without_ball_in.py`

Removes all frames without the ball from `afl-preprocessed` directory locally. Note that we need to copy paste in 
the relevant `.xml` files into the `/annotations` directory.



