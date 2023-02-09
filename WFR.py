from bson.objectid import ObjectId
from pymongo import MongoClient, ReadPreference, read_concern, write_concern

'''
Write Follow Read 시나리오
0. 비어있는 콜렉션이라 가정
1. W1을 적는다
2. W1에서 적은값을 R1에서 읽는다
3. fail over가 발생해서 세컨더리 노드가 프라이머리로 올라온다
4. W2를 적는다
5. 콜렉션을 읽어왔을때 W1, W2에서 적었던 내용이 다 있는지 확인한다.
'''
def WFR_fail():
    try:
        print('start')

        # connect to Mongo
        client = MongoClient('mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019', replicaSet = 'rs0', username = 'mongo', password='mongo')

        # get collection
        collection = client['test'].get_collection('collection')

        # write1
        w1 = collection.insert_one({'w1': 1})
        print('w1', w1)

        # read1
        r1 = list(collection.find({'_id': ObjectId(w1.inserted_id)}))
        print('r1', r1)

        # write2
        w2 = collection.insert_one({'w2': 2})
        print('w2', w2)

        # w1, w2가 둘다 나오면 성공. 아니면 실패
        r2 = collection.find()
        for doc in r2:
            print(doc)

    except ValueError:
        print('error Occurred', ValueError)

def WFR_fail_with_majority():
    try:
        print('start')

        # connect to Mongo
        client = MongoClient('mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019', replicaSet = 'rs0', username = 'mongo', password='mongo')

        # get collection
        collection = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY, write_concern= write_concern.WriteConcern(w = 1), read_concern= read_concern.ReadConcern(level='majority'))
        
        # write1
        w1 = collection.insert_one({'w1': 1})
        print('w1', w1)
        # read1
        r1 = list(collection.find({'_id': ObjectId(w1.inserted_id)}))
        print('r1', r1)

        # write2
        w2 = collection.insert_one({'w2': 2})
        print('w2', w2)

        # w1, w2가 둘다 나오면 성공. 아니면 실패
        r2 = collection.find()
        for doc in r2:
            print(doc)

    except ValueError:
        print('error Occurred', ValueError)

def WFR_with_majority_session():
    try:
        print('start')

        # connect to Mongo
        client = MongoClient('mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019', replicaSet = 'rs0', username = 'mongo', password='mongo')

       # start session
        session = client.start_session(causal_consistency= True)

        # get collection
        collection = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY, write_concern= write_concern.WriteConcern(w = 1), read_concern= read_concern.ReadConcern(level='majority'))
        
        # write1
        w1 = collection.insert_one({'w1': 1}, session=session)
        print('w1', w1)

        # read1
        r1 = list(collection.find({'_id': ObjectId(w1.inserted_id)}, session=session))
        print('r1', r1)

        # write2
        w2 = collection.insert_one({'w2': 2}, session=session)
        print('w2', w2)

        # w1, w2가 둘다 나오면 성공. 아니면 실패
        r2 = collection.find()
        for doc in r2:
            print(doc)

    except ValueError:
        print('error Occurred', ValueError)



# WFR_fail()
# WFR_fail_with_majority()
# WFR_with_majority_session()