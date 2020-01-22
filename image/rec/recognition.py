import csv
import os
import face_recognition

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
import django
django.setup()
from home.models import Profile


trainings = []
ids = []
usernames = []


def readCsvTrainingFile(p):
    p = os.path.join('data', p)
    o = open(p)
    return string2csv(o)


def generate_embeddings(img):
    try:
        emb = face_recognition.face_encodings(img)[0]
    except:
        return None
    return emb


def compare_emb_min(emb):
    # print('len(trainings)', len(trainings))
    # for i, tr in enumerate(trainings):
    #    print('len(trainings[' + str(i) + '])', len(trainings[i]), 'ID', ids[i])
    idx = -1
    fin = 99.99
    for i, train in enumerate(trainings):
        length = len(train)
        if length:
            if length < 11:
                res = face_recognition.face_distance(train, emb).mean()
            else:
                res = face_recognition.face_distance(train, emb)
                res.sort()
                res = res[0:int(0.9*length)]
                res = res.mean()
            if res<fin:
                fin = res
                idx = ids[i]
    return(fin, idx)


def set_currnt_trainings():
    ids.clear()
    trainings.clear()
    usernames.clear()
    for elm in Profile.objects.all():
        ids.append(elm.pk)
        usernames.append(elm.user.username)
        # trainings.append(readCsvTrainingFile(elm.train))
        try:
            trainings.append(readCsvTrainingFile(elm.train))
            # print('set done')
        except:
            trainings.append([])


def get_currnt_trainings():
    s = []
    # print('trainings', trainings)
    for i, elm in enumerate(ids):
        s.append((elm, usernames[i], len(trainings[i])))
    return s


def string2csv(si):
    cw = csv.reader(si, delimiter=',')
    data = []
    for i, row in enumerate(cw):
        data.append([])
        for j in range(128):
            data[i].append(float(row[j]))
    return data


set_currnt_trainings()