import pyrealsense2 as rs
import numpy as np
import cv2

class RealSense():

    def __init__(self):
        # Setup streaming
        # Create a pipeline
        self.pipeline = rs.pipeline()
        # Create a config and configure the pipeline to stream
        # different resolutions of color and depth streams
        self.config = rs.config()
        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = self.config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)      
       
    # def startStreaming(self):

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        profile = self.pipeline.start(self.config)
        # Calc the depth sensor's depth scale.
        depth_sensor = profile.get_device().first_depth_sensor()
        self.depth_scale = depth_sensor.get_depth_scale()
        print("Depth Scale is: " , self.depth_scale)

    def getFrames(self):
        # Get frameset of color and depth
        frames = self.pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image
        self.allignFrames(frames)         

    def record(self):
        # Stop the pipeline if it was already running
        try:
            # If the pipeline is already running, stop it
            self.pipeline.stop()
        except:
            # Catch any exceptions related to stopping the pipeline if it wasn't running
            pass

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        # Start streaming
        profile = self.pipeline.start(self.config)    
        self.config.enable_record_to_file("tempFile2.bag")

    def playback(self):
        self.config.enable_record_from_file("tempFile")

    def allignFrames(self, frames):
        # Create an align object
        # rs.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        align_to = rs.stream.color
        align = rs.align(align_to)

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            self.cleanUp() # SEEEEEEEEEEEEEEEEEEEEEE

        # Final depth matrix: 480, 640.
        self.depth_image = np.asanyarray(aligned_depth_frame.get_data())
        # Final color matrix: 480, 640, 3.
        self.color_image = np.asanyarray(color_frame.get_data())      

    def clippingBkg(self):
        # Removing the background of objects more than clipping_distance_in_meters meters away.        
        # Calc the clipping distance depth scale
        self.clipping_distance_in_meters = 1 #1 meter
        self.clipping_distance = self.clipping_distance_in_meters / self.depth_scale
        # Remove background - Set pixels further than clipping_distance to grey
        grey_color = 153
        depth_image_3d = np.dstack((self.depth_image, self.depth_image, self.depth_image)) #depth image is 1 channel, color is 3 channels
        bg_removed = np.where((depth_image_3d > self.clipping_distance) | (depth_image_3d <= 0), grey_color, self.color_image)
        return bg_removed
          
    def render(self,bg_removed):
        # Render images:
        #   depth align to color on left
        #   depth on right
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(self.depth_image, alpha=0.03), cv2.COLORMAP_JET)
        images = np.hstack((bg_removed, depth_colormap))
        # The images here is the superposition of bg_removed colourMap and depth value based heatMap.
        cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
        cv2.imshow('Align Example', images)
        

    def cleanUp(self):
        # Stop the pipeline and cleanup.
        self.pipeline.stop()
        # need to see the way correctly here - maybe also need to terminate the main loop of pgm here also.


if __name__ == "__main__":

    # Main loop
    RealSense1 = RealSense()
    try:
        while(True):   
            
            RealSense1.getFrames()
            bgRemoved = RealSense1.clippingBkg()    
            # RealSense1.record()   
            RealSense1.render(bgRemoved) 


            # Trackbar

            alpha_slider_max = 100            
            ########## Cite: gpt ############
            def on_trackbar(x):
                pass
            ########## Cite: gpt ############                                                
            cv2.namedWindow("trackbar window")
            HSV_min = 'Alpha x %d' % alpha_slider_max
            cv2.createTrackbar(HSV_min, "trackbar window" , 0, alpha_slider_max, on_trackbar)


            while True:

                # Load the img
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(RealSense1.depth_image, alpha=0.03), cv2.COLORMAP_JET)
                images = np.hstack((bgRemoved, depth_colormap))           
                # Get the position of the trackbar
                threshold_value = cv2.getTrackbarPos('Threshold', 'trackbar window')
                # Apply a binary threshold to the image
                # _, thresholded_img = cv2.threshold(images, threshold_value, alpha_slider_max, cv2.THRESH_BINARY)
                # Display the thresholded image
                cv2.imshow('trackbar window', images)
                on_trackbar(0)
        
                # To keep the GUI responsive
                key = cv2.waitKey(1)
                # Press esc or 'q' to close the image window
                if key & 0xFF == ord('q') or key == 27:
                    cv2.destroyAllWindows()
                    break


    finally:
        RealSense1.cleanUp()
        









