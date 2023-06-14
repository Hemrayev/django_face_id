import datetime

import cv2

import face_recognition
import pickle5 as pickle
import os
import shutil

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "face_id.settings")
import django

django.setup()

from core.models import Get_In, Get_Out

with open("Data/database.pickle", "rb") as f:
    database = pickle.load(f)

t = 0

while True:
    try:
        if len(os.listdir("Faces_in")) != 0:
            lenlist = len(os.listdir("Faces_in"))
            print('#' * 20)

            for index in range(len(os.listdir("Faces_in"))):
                shutil.move("Faces_in/" + str(os.listdir('Faces_in')[0]),
                            "FacesDir_in/" + str(os.listdir('Faces_in')[0]))

            print("Faces_in to FacesDir_in")

            # for unknown_face_index in range(len(os.listdir("FacesDir_in"))):
            while len(os.listdir("FacesDir_in")) != 0:

                print(os.listdir("FacesDir_in")[0])

                unknown_face = cv2.imread("FacesDir_in/" + str(os.listdir("FacesDir_in")[0]))
                unknown_face_locations = face_recognition.face_locations(unknown_face)
                unknown_face_encodings = face_recognition.face_encodings(unknown_face, unknown_face_locations)[0]

                t = 0

                for index in range(len(database)):
                    data = database[index + 1]
                    known_face_encodings = data['encodings']

                    compare_matches = face_recognition.compare_faces(known_face_encodings, unknown_face_encodings)

                    print(compare_matches)

                    k = 0
                    for match in compare_matches:
                        if match == True:
                            k += 1

                    if k >= 10:
                        # print("Face_Detected")
                        # print(data['name'])
                        id = index + 1
                        sene_doly = datetime.datetime.now()
                        sene = sene_doly.date().strftime("%Y-%m-%d")
                        wagt = sene_doly.time().strftime("%H:%M:%S.%f")
                        slug = data['name'] + '-' + sene_doly.strftime("%Y-%m-%d")
                        try:
                            count = 1
                            get_in = Get_In.objects.create(person_id_id=id, count=count, slug=slug)
                            get_in.save()
                        except:
                            if Get_In.objects.filter(slug=slug).exists():
                                get_in = Get_In.objects.filter(slug=slug).values('get_in_time')
                                d = str(get_in[0]['get_in_time'])
                                g = "00:05:00.0"
                                if d >= g:
                                    count = Get_In.objects.filter(slug=slug).values('count')
                                    f = count[0]['count']+1
                                    slug = data['name'] + '-' + sene_doly.strftime("%Y-%m-%d") + str(f)
                                    h = Get_In.objects.create(person_id_id=id, count=f, slug=slug)
                                    h.save()
                        t += 1
                        shutil.move("FacesDir_in/" + str(os.listdir('FacesDir_in')[0]),
                                    "DetectedFaces/" + str(os.listdir('FacesDir_in')[0]))

                if t == 0:
                    shutil.move("FacesDir_in/" + str(os.listdir('FacesDir_in')[0]),
                                "UnknownFaces/" + str(os.listdir('FacesDir_in')[0]))

            print("+++" * 20)
    except:
        continue
