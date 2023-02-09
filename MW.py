from bson.objectid import ObjectId
from pymongo import MongoClient, ReadPreference, read_concern, write_concern

'''
Monotonic Write 시나리오
0. 비어있는 콜렉션이라 가정
1. W1을 적는다 {'W1': 1}
3. fail over가 발생해서 세컨더리 노드가 프라이머리로 올라온다
4. w1을 적었던 다큐먼트에 대해서 update를 시도한다 {'W2': 2} 추가
5. W1 연산후 받았던 키로 다큐먼트를 찾아왔을때 다큐먼트가 없거나 'W1': 1이 누락되고 'W2': 2만 있는지 확인한다
'''

def MW_fail():
    try:
        print('start')

        # connect to Mongo
        client = MongoClient('mongodb://127.0.0.1:27017,127.0.0.1:27018', replicaSet = 'rs0', readPreference = 'secondary', maxStalenessSeconds = 120, username = 'mongo', password='mongo')

        # get collection
        collection = client['test'].get_collection('collection')

        # W1
        w1 = collection.insert_one({'W1': 1})
        print('w1', w1)

        # W2
        collection.update_one({'_id': ObjectId(w1.inserted_id)}, update={'$set': {'W2': 2}})

        # x, y 가 모두 들어있으면 w1, w2가 잘 반영된거임. x 없이 y만 있거나 w2 자체를 못찾으면 실패~
        w2 = list(collection.find({'_id': ObjectId(w1.inserted_id)}))
        print('w2', w2)
        print('done')
    except ValueError:
        print('error Occurred', ValueError)

def MW_fail_with_majority():
    try:
        print('start')

        # connect to Mongo
        client = MongoClient('mongodb://127.0.0.1:27017,127.0.0.1:27018', replicaSet = 'rs0', readPreference = 'secondary', maxStalenessSeconds = 120, username = 'mongo', password='mongo')

        # get collection
        # 근데 프라이머리, 세컨더리 총 노드 2개에서 S 꺼진 상태에서 쓰는데 write majority 하는 의미가 없는거 같음.
        collection = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY, write_concern= write_concern.WriteConcern(w = 1), read_concern= read_concern.ReadConcern(level='majority'))

        # W1
        w1 = collection.insert_one({'W1': 1})
        print('w1', w1)

        # W2
        collection.update_one({'_id': ObjectId(w1.inserted_id)}, update={'$set': {'W2': 2}})

        # x, y 가 모두 들어있으면 w1, w2가 잘 반영된거임. x 없이 y만 있거나 w2 자체를 못찾으면 실패~
        w2 = list(collection.find({'_id': ObjectId(w1.inserted_id)}))
        print('w2', w2)

        print('done')
    except ValueError:
        print('error Occurred', ValueError)

def MW_with_majority_session():

    try:
        print('start')

        # connect to Mongo
        client = MongoClient('mongodb://127.0.0.1:27017,127.0.0.1:27018', replicaSet = 'rs0', readPreference = 'secondary', maxStalenessSeconds = 120, username = 'mongo', password='mongo')

        # start session
        session = client.start_session(causal_consistency= True)

        # get collection
        collection = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY, write_concern= write_concern.WriteConcern(w = 1), read_concern= read_concern.ReadConcern(level='majority'))

        # W1
        w1 = collection.insert_one({'W1': 1}, session=session)
        print('w1', w1)

        # W2
        collection.update_one({'_id': ObjectId(w1.inserted_id)}, update={'$set': {'W2': 2}}, session=session)

        # x, y 가 모두 들어있으면 w1, w2가 잘 반영된거임. x 없이 y만 있거나 w2 자체를 못찾으면 실패~
        w2 = list(collection.find({'_id': ObjectId(w1.inserted_id)}, session= session))
        print('w2', w2)
        print('done')
    except ValueError:
        print('error Occurred', ValueError)

# MW_fail()
# MW_fail_with_majority()
# MW_with_majority_session()
