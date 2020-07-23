# aibeing
Motion Dection and face detection

Implementation:
1)python
2)opencv

working:
* when "motion still detection.py " executed ,videocapture starts and first frame is taken as baseline_frame(baseline_frame will be updated every 30 seconds)
for comparing with next upcoming frame where any changes occurred will be captured by contours and  displaying as "motion detected" else displaying as "no motion detected"
*if "NO motion is detected for 2 mins(can be N number of minutes) then exiting the program"
