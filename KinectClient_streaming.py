#Simple example Robot Raconteur webcam client
#This program will show a live streamed image from
#the webcams.  Because Python is a slow language
#the framerate is low...

from RobotRaconteur.Client import *

import time
import numpy
import cv2
import sys
import timeit
import numpy as np
#Function to take the data structure returned from the Webcam service
#and convert it to an OpenCV array
#def WebcamImageToMat(image):
#    frame2=image.pose#data.reshape([image.height, image.width, 3], order='C')
#    return frame2
#
#current_frame=None


def main():

    #url='tcp://localhost:5555/AzureBodyTracking/Kinect'
    url='rr+tcp://localhost:5555?service=Kinect'
    if (len(sys.argv)>=2):
        url=sys.argv[1]

    #Startup, connect, and pull out the camera from the objref    
    c_host=RRN.ConnectService(url)



    #cv2.namedWindow("Image")
    t_all = []
    for i in range(100):
        tic = timeit.default_timer()
        #Just loop resetting the frame
        #This is not ideal but good enough for demonstration
        pose = c_host.getpose()
        #depth = c_host.getdepth()
        
        if all(pose) != 0: 
            pose = np.array(pose).reshape(-1,3)
            print (pose)
            #cv2.imshow("Image",current_frame)
#        if cv2.waitKey(50)!=-1:
#            break
        t_all.append(timeit.default_timer()-tic)    
        print (t_all[-1])
#    cv2.destroyAllWindows()

    print (np.mean(t_all))


#This function is called when a new pipe packet arrives
#def new_frame(pipe_ep):
#    global current_frame
#
#    #Loop to get the newest frame
#    while (pipe_ep.Available > 0):
#        #Receive the packet
#        image=pipe_ep.ReceivePacket()
#        #Convert the packet to an image and set the global variable
#        current_frame=WebcamImageToMat(image)

if __name__ == '__main__':
    main()
