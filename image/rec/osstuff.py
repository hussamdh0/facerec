import csv
import os
import random
import string

import cv2
import face_recognition

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
import django
django.setup()
from home.models import Profile, Node, User


trainings = []
ids = []
usernames = []
nodes = []
caps = []
cap = cv2.VideoCapture(0)


def getDirList(path):
    return [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]


def add_user(name):
    a = User(username=name)
    a.set_password('pass1234')
    a.save()
    paths = getImagesPathsFromPath(os.path.join('samples', name))
    data = []
    for path in paths:
        img = cv2.imread(path, 1)
        emb = generate_embeddings(img)
        if emb is not None:
            data.append(emb)

    path = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    prf = Profile.objects.get(pk=a.id)
    prf.train = path
    prf.save()
    writeCsvTrainingFile(path, data)
    set_currnt_trainings()


def predict_folder(name):
    paths = getImagesPathsFromPath(os.path.join('topredict', name))
    results = []
    j=0
    length = len(paths)
    for path in paths:
        img = cv2.imread(path, 1)
        try:
            embs = face_recognition.face_encodings(img)
            for i, emb in enumerate(embs):
                result = []
                res = compare_emb_min(emb)
                result.append(usernames[res[1]])
                result.append(res[0])
                result.append(path + ': ' + str(i))
                results.append(result)
        except:
            print('not supported file')
        print(name + ':', j, '/', length)
        j += 1

    p = os.path.join('topredict', name + '.csv')
    o = open(p, mode='w', newline='')
    csv2string(o, results)
    o.close()
    print('predicted:', length, 'for', name)


def getImagesPathsFromPath(path):
    return [os.path.join(path, f) for f in os.listdir(path) if f.split(".")[-1] == "jpg"]


def readCsvTraining(path):
    file = open(path, newline='')
    reader = csv.reader(file)
    data = []
    names = []
    count = 0
    for j, row in enumerate(reader):
        print(str(count) + "\t/\t946")
        features = []
        for i in range(0, 128):
            features.append(float(row[i]))
        data.append(features)
        names.append(row[128] + "." + str(j))
        count = count + 1
    return names, data


def readCsvTrainingFile(p):
    p = os.path.join('data', p)
    o = open(p)
    return string2csv(o)


def writeCsvTrainingFile(p, data):
    p = os.path.join('data', p)
    o = open(p, mode='w', newline='')
    csv2string(o, data)


def generate_embeddings(img):
    try:
        emb = face_recognition.face_encodings(img)[0]
    except:
        return None

    return emb


def generate_embeddings_cap():
    _, img = cap.read()
    try:
        emb = face_recognition.face_encodings(img)[0]
    except:
        return None
    return emb


def predict():
    print('NODES', nodes)
    for i, node in enumerate(nodes):
        caps[i].read()*5
        _, img = caps[i].read()
        emb = generate_embeddings(img)
        if emb is not None:
            res = compare_emb_min(emb)
            print('res', res[0], usernames[res[1]])


def compare_emb_min(emb):
    print('len(trainings)', len(trainings))
    print('len(trainings[0])', len(trainings[0]))
    print('MIN')
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
                idx = i
    return [fin, idx]


def set_trainings(id):
    prf = Profile.objects.get(pk=id)
    data = []
    path = prf.train
    hastrain = False
    if prf.has_train():
        try:
            data = readCsvTrainingFile(path)
            hastrain = True
        except:
            pass
    else:
        path = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        # print('random string', path)
        prf.train = path
        prf.save()
    tot = 0
    while True:
        _, image = cap.read()
        cv2.imshow('read image', image)
        emb = generate_embeddings(image)
        if emb is None:
            cv2.waitKey(1)
        else:
            k = cv2.waitKey(10000) & 0xFF
            if k == 27:
                cv2.destroyAllWindows()
                break
            if k == ord('s'):
                data.append(emb)
                tot += 1
            if k == ord('p'):
                pass
            cap.read()*4

    print('Total Trainings Added for', prf.user.username, 'are', tot)
    writeCsvTrainingFile(path, data)
    set_currnt_trainings()


def set_currnt_trainings():
    ids.clear()
    trainings.clear()
    usernames.clear()
    caps.clear()
    nodes.clear()
    for elm in Profile.objects.all():
        ids.append(elm.pk)
        usernames.append(elm.user.username)
        # trainings.append(readCsvTrainingFile(elm.train))
        try:
            trainings.append(readCsvTrainingFile(elm.train))
            # print('set done')
        except:
            trainings.append([])

    for node in Node.objects.all():
        caps.append(cv2.VideoCapture(node.camera))
        nodes.append(node.pk)


def get_currnt_trainings():
    s = []
    # print('trainings', trainings)
    for i, elm in enumerate(ids):
        s.append((elm, usernames[i], len(trainings[i])))
    return s


def csv2string(si, data):
    cw = csv.writer(si)
    for elm in data:
        cw.writerow(elm)


def string2csv(si):
    cw = csv.reader(si, delimiter=',')
    data = []
    for i, row in enumerate(cw):
        data.append([])
        for j in range(128):
            data[i].append(float(row[j]))
    return data


set_currnt_trainings()