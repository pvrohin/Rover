### NOTE
Pass source of yolo as argument

Directory structure of yoloSource:

```bash
  tree
    yoloSource
      ├── coco.names(https://github.com/pjreddie/darknet/blob/master/data/coco.names)
      ├── yolov3.cfg(https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg)
      └── yolov3.weights(https://pjreddie.com/media/files/yolov3.weights)

```

Sample: rosrun object_detect yolo_video.py -y yoloSource
