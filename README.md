# AFL-Data

Some quick scripts for working with the AFL data 

`partial_video_download.py`

Script which downlaods a small clip from the first video of each game from 
each camera. 

Note that each video clip has to start at the beginning of the video for it 
to be playable (missing metadata corrupts it I assume, and we're clipping 
by bytes). 