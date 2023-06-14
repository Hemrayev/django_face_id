import cv2
import face_recognition


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(2)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, image = self.video.read()
        count = 0
        if ret:
            face_locations0 = face_recognition.face_locations(image)
            count += 1
            for index, (x, y, w, h) in enumerate(face_locations0):
                # x *= 4
                # y *= 4
                # w *= 4
                # h *= 4
                faces = image[x:w, h:y]
                # pil_img = Image.fromarray(faces)
                # pil_img.save(f"Faces_in/{count}_face_img.jpg")
                cv2.imwrite('/home/asus/PycharmProjects/Beta_version/face_recognizer/Faces_in/face_in_' + str(index) +
                            '.jpg', faces)
                # cv2.rectangle(image, (h, x), (y, w), (0, 0, 255), 2)

            ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


class VideoCamera_2(object):
    def __init__(self):
        self.video = cv2.VideoCapture(4)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, image = self.video.read()
        if ret:
            #     # if process_this_frame:
            #     small_img1 = cv2.resize(img1, (0, 0), fx = 0.25, fy = 0.25)
            face_locations1 = face_recognition.face_locations(image)
            #     # process_this_frame = not process_this_frame
            #     # print(face_locations)
            #
            for index, (x, y, w, h) in enumerate(face_locations1):
                #         x *= 4
                #         y *= 4
                #         w *= 4
                #         h *= 4
                faces = image[x:w, h:y]
                cv2.imwrite('/home/asus/PycharmProjects/Beta_version/face_recognizer/Faces_out/face_out_' + str(index)
                            + '.jpg', faces)
                # cv2.rectangle(image, (h, x), (y, w), (0, 0, 255), 2)
            ret, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


