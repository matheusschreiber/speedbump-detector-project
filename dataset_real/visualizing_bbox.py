import cv2

IMGS_PATH = 'imgs'
ANNO_PATH = 'speedbumps.csv'


with open(ANNO_PATH, 'r') as annos:
    for anno in annos:
        fields = anno.split(',')
        image = cv2.imread(fields[1])

        xmin = int(float(fields[3]) * image.shape[1])
        ymin = int(float(fields[4]) * image.shape[0])
        xmax = int(float(fields[7]) * image.shape[1])
        ymax = int(float(fields[8]) * image.shape[0])

        # xmin = 100
        # ymin = 100
        # xmax = 200
        # ymax = 200
        
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 0, 255),10)
        
        image = cv2.resize(image, (600,600))
        
        cv2.imshow('image', image)

        wait_time = 1000
        while cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) >= 1:
            keyCode = cv2.waitKey(wait_time)
            if (keyCode & 0xFF) == ord("q"):
                cv2.destroyAllWindows()
                break
        
