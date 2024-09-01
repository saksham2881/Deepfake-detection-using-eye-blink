import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector 
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture('vid.mp4')
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(640, 360, [20, 50])
idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratioList = []
blinkcounter = 0
counter = 0
c=0
start_time = cv2.getTickCount() / cv2.getTickFrequency()  # Get current time in seconds

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)
    
    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 5, (255, 0, 255), cv2.FILLED)
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lengthVer, _ = detector.findDistance(leftUp, leftDown)
        lengthHor, _ = detector.findDistance(leftLeft, leftRight)
        ratio = int((lengthVer / lengthHor) * 100)
        ratioList.append(ratio)
        
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        if ratioAvg < 35 and counter == 0:
            blinkcounter += 1
            if blinkcounter == 2 and c != 1:
            	blinkcounter = 1
            	c=1
            	
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                
        cvzone.putTextRect(img, f'Blink count: {blinkcounter}', (50, 100))

        imgPlot = plotY.update(ratioAvg)
        cv2.imshow("ImagePlot", imgPlot)

    img = cv2.resize(img, (640, 360))
    cv2.imshow("Image", img)
    
    current_time = cv2.getTickCount() / cv2.getTickFrequency()  # Get current time in seconds
    elapsed_time = current_time - start_time
    if elapsed_time >= 20:  # Terminate after 10 seconds
        break
    
    cv2.waitKey(15)

if blinkcounter >= 4 and blinkcounter <= 8:
    print("Video is authentic")
else:
    print("Video is deepfake")

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()

