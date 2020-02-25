#Simple example Robot Raconteur webcam service

#Note: This example is intended to demonstrate Robot Raconteur
#and is designed to be simple rather than optimal.

import time
import RobotRaconteur as RR
#Convenience shorthand to the default node.
#RRN is equivalent to RR.RobotRaconteurNode.s
RRN=RR.RobotRaconteurNode.s
import _thread
import threading
import numpy
import traceback
import cv2
import platform
import sys
import argparse

import pyk4a
from pyk4a import Config, PyK4A, ColorResolution

#Class that implements a single webcam
class Kinect_impl(object):
    #Init the camera being passed the camera number and the camera name
    pose = None
    frame = None
    depth = None
    
    def __init__(self):
        #self._lock=threading.RLock()
        

        self.k4a = PyK4A(Config(color_resolution=ColorResolution.RES_720P,
                           depth_mode=pyk4a.DepthMode.NFOV_UNBINNED))

        self.k4a.connect()
        
        try:
           _thread.start_new_thread(self.read_loop, ())
        except:
           print ("Error: unable to start thread")        

#        self.frame, _ = self.k4a.get_capture()
#        self.pose = self.k4a.get_pose()
        #print (self.pose)

    def read_loop(self):
        while True:
            self.frame, self.depth = self.k4a.get_capture()
            self.pose = self.k4a.get_pose()
            #print (self.frame.dtype, self.depth.dtype)
        
    def getpose(self):
        #self.pose = self.k4a.get_pose()
        if self.pose is not None and self.pose.shape[0] == 1:
            for i in range(self.pose.shape[0]):
                self.pose = self.pose[i, :, 2:5].reshape(-1, 3)
            #print (self.pose)
        else:
            self.pose = numpy.zeros([32,3]) 
            
        #print (self.pose.dtype)    
        return list(self.pose.flatten('C'))
    
    def getframe(self):
#        self.frame, _ = self.k4a.get_capture()
        return list(self.frame.flatten('C'))
              
    def getdepth(self):
#        self.frame, _ = self.k4a.get_capture()
        return list(self.depth.flatten('C'))


    #Shutdown the Webcam
    def Shutdown(self):
        self.k4a.disconnect()
        #del(self._capture)




def main():

    port = 5555       
    t1 = RR.LocalTransport()
    t1.StartServerAsNodeName("AzureBodyTracking")
    RRN.RegisterTransport(t1)

    t2 = RR.TcpTransport()
    t2.EnableNodeAnnounce()
    t2.StartServer(port)
    RRN.RegisterTransport(t2)
    
    obj=Kinect_impl()

    with open('AzureBodyTracking.robdef', 'r') as f:
        service_def = f.read()
    
    RRN.RegisterServiceType(service_def)
    RRN.RegisterService("Kinect", "AzureBodyTracking.Kinect", obj)
    
    input("Server started, press enter to quit...")

    obj.Shutdown()
    RRN.Shutdown()
    
#    
#    #Accept the names of the webcams and the nodename from command line
#            
#    parser = argparse.ArgumentParser(description="Azure Kinect Body Tracking Service")
#    #parser.add_argument("--camera-names",type=str,help="List of camera names separated with commas")
#    parser.add_argument("--nodename",type=str,default="AzureBodyTracking.Kinect",help="The NodeName to use")
#    parser.add_argument("--tcp-port",type=int,default=5555,help="The listen TCP port")
#    parser.add_argument("--wait-signal",action='store_const',const=True,default=False)
#    args = parser.parse_args()
#
#    #Initialize the webcam host root object
##    camera_names=[(0,"Left"),(1,"Right")]
##    if args.camera_names is not None:
##        camera_names_split=list(filter(None,args.camera_names.split(',')))
##        assert(len(camera_names_split) > 0)
##        camera_names = [(i,camera_names_split[i]) for i in range(len(camera_names_split))]
#        
#    
#    obj=Kinect_impl()
#    
#    with RR.ServerNodeSetup(args.nodename,args.tcp_port):
#
#        RRN.RegisterServiceTypeFromFile("AzureBodyTracking")
#        RRN.RegisterService("Kinect","AzureBodyTracking.Kinect",obj)
#    
#    
#        if args.wait_signal:  
#            #Wait for shutdown signal if running in service mode          
#            print("Press Ctrl-C to quit...")
#            import signal
#            signal.sigwait([signal.SIGTERM,signal.SIGINT])
#        else:
#            #Wait for the user to shutdown the service
#            if (sys.version_info > (3, 0)):
#                input("Server started, press enter to quit...")
#            else:
#                raw_input("Server started, press enter to quit...")
#    
#        #Shutdown
#        obj.Shutdown()    


if __name__ == '__main__':
    main()
