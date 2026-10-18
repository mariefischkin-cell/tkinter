
import cv2
import numpy as np

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("Camera not available")

canvas = None
previous_point = None
paint_color = (0, 255, 0)

while True:
    success, frame = camera.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)
    height, width = frame.shape[:2]

    if canvas is None:
        canvas = np.zeros_like(frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([90, 70, 50])
    upper = np.array([135, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        np.ones((5, 5), np.uint8)
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    status = "Hold a BLUE object in front of the camera"

    if contours:
        contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(contour)

        if area > 350:
            perimeter = cv2.arcLength(contour, True)

            polygon = cv2.approxPolyDP(
                contour,
                0.035 * perimeter,
                True
            )

            moments = cv2.moments(contour)

            if moments["m00"]:
                point = (
                    int(moments["m10"] / moments["m00"]),
                    int(moments["m01"] / moments["m00"])
                )

                cv2.drawContours(
                    frame,
                    [contour],
                    -1,
                    (0, 255, 255),
                    2
                )

                cv2.circle(
                    frame,
                    point,
                    8,
                    (0, 0, 255),
                    -1
                )

                if len(polygon) >= 6:
                    status = "ROUND SHAPE: DRAW"

                    if previous_point is not None:
                        cv2.line(
                            canvas,
                            previous_point,
                            point,
                            paint_color,
                            5
                        )

                    previous_point = point

                elif len(polygon) == 4:
                    status = "RECTANGLE: MOVE"
                    previous_point = None

                else:
                    status = "OTHER SHAPE"
                    previous_point = None
        else:
            previous_point = None
    else:
        previous_point = None

    output = cv2.addWeighted(
        frame,
        1,
        canvas,
        0.8,
        0
    )

    cv2.putText(
        output,
        status,
        (15, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        output,
        "C: Clear  G/R/Y: Colors  Q: Quit",
        (15, height - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.imshow("OpenCV Gesture Control", output)

    key = cv2.waitKey(1) & 255

    if key == ord("q"):
        break

    if key == ord("c"):
        canvas[:] = 0
        previous_point = None

    if key == ord("g"):
        paint_color = (0, 255, 0)

    if key == ord("r"):
        paint_color = (0, 0, 255)

    if key == ord("y"):
        paint_color = (0, 255, 255)

camera.release()
cv2.destroyAllWindows()
