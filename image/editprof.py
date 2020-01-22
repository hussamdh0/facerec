from rec import osstuff as of


def meta():
    train_meta = of.get_currnt_trainings()
    total_users_with_no_train = 0
    for id, username, num_train in train_meta:
        print('ID:', id, ', ', username, ': \thas', num_train, 'trainings')
        if num_train == 0:
            total_users_with_no_train += 1

    print('Total users with no trainings:', total_users_with_no_train)

def user_with_few_trainings(how_much_is_few):
    train_meta = of.get_currnt_trainings()
    total_users_with_few_train = 0
    for id, username, num_train in train_meta:
        if (num_train <= how_much_is_few):
            print('ID:', id, ', ', username, 'has', num_train, 'trainings')
            total_users_with_few_train += 1

    print('Total users with less than or equal to', how_much_is_few,
                            'trainings:', total_users_with_few_train)


def get_a_user_id():
    try:
        in_id = int(input())
        for id, _, __ in of.get_currnt_trainings():
           if id == in_id:
               return id
        return -1
    except:
        print('Bad input!')
        return -1



while True:
    print('1. Refresh User Info')
    print('2. Print Information About Trainings')
    print('3. Print Users with No Trainings')
    print('4. Updata User Trainings')
    print('5. Predict')
    print('10. EXIT')

    try:
        choice = int(input())
    except:
        print('Bad input!')
        continue

    if choice < 1:
        print('Enter an Integer > 0')
    if choice > 10:
        print('No such choice available!')
    if choice == 1:
        of.set_currnt_trainings()
    if choice == 2:
        meta()
    if choice == 3:
        user_with_few_trainings(0)
    if choice == 4:
        id = get_a_user_id()
        if(id == -1):
            print ('No user with such ID!')
        else:
            of.set_trainings(id)
    if choice == 5:
        of.predict()
    if choice == 10:
        break



