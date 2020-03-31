import dlib
import cv2

def write_rec(d):
    cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255), 2)
if __name__ == "__main__":

    SvmFile = "detector.svm"
    detector = dlib.simple_object_detector(SvmFile)
    cap = cv2.VideoCapture('output.mp4')
    if cap.isOpened() is not True:
        raise("IO Error")
          
    WinName = "Capture"
    cv2.namedWindow(WinName, cv2.WINDOW_AUTOSIZE)
    win_det = dlib.image_window()
    win_det.set_image(detector)

    while True:
        ret, img = cap.read()

        if ret:
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            dets = detector(rgb)
            if len(dets):
                d = dets[0]
                write_rec(d)
                if len(dets) == 2:
                    d1 = dets[1]
                    write_rec(d1)
                elif len(dets) == 3:
                    d1 = dets[1]
                    d2 = dets[2]
                    write_rec(d1)
                    write_rec(d2)
                elif len(dets) == 4:
                    d1 = dets[1]
                    d2 = dets[2]
                    d3 = dets[3]
                    write_rec(d1)
                    write_rec(d2)
                    write_rec(d3)
                elif len(dets) == 4:
                    d1 = dets[1]
                    d2 = dets[2]
                    d3 = dets[3]
                    d4 = dets[4]
                    write_rec(d1)
                    write_rec(d2)
                    write_rec(d3)
                    write_rec(d4)
            cv2.imshow(WinName, img)

        if cv2.waitKey(1)  > 0:
            break

    cap.release()
    cv2.destroyAllWindows()
