# Vehicle_detection

### Інсталювання потрібних пакетів: 

```sh
pip install -r requirements.txt
```

Використовується [Tensorflow API](https://github.com/tensorflow/models/tree/master/research/object_detection).

### Tracker
![](https://user-images.githubusercontent.com/22610163/41812993-a4b5a172-7735-11e8-89f6-083ec0625f21.png)
Source video is read frame by frame with OpenCV. Each frames is processed by "SSD with Mobilenet" model is developed on TensorFlow.
This is a loop that continue working till reaching end of the video. 
The main pipeline of the tracker is given at the above Figure

### Запуск
```sh
python3 vehicle_detection_main.py
```
