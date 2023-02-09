import time

from bson.objectid import ObjectId
from pymongo import MongoClient, ReadPreference, read_concern, write_concern

'''
Monotonic Read 시나리오
0. 비어있는 콜렉션이라 가정
1. 클라이언트1, 클라이언트2 연결을 만든다.
2. 클라이언트1이 새로운 다큐먼트를 콜렉션에 추가한다.
3. 클라이언트2가 각각 프라이머리, 세컨더리로 부터 2번 과정에서 클라이언트1이 적은 값을 읽어온다.
4. 두 값이 같은지 비교한다
5. 위의 과정을 3초동안 반복한다
'''

def MR_fail():
    try:
        print('start')

        # connect to Mongo
        client1 = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo', replicaSet = 'rs0')
        client2 = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo', replicaSet = 'rs0')

        # get collection
        collection1 = client1['test'].get_collection('collection').with_options(read_preference= ReadPreference.PRIMARY)

        collection2 = client2['test'].get_collection('collection').with_options(read_preference= ReadPreference.PRIMARY)
        collection3 = client2['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY)
        
        # For 3 sec, write to Primary and get from Secondary
        start_time = time.time()
        while(time.time() - start_time < 3):
            # insert new element 
            new_document = collection1.insert_one({'합격기': 1})
            found_document1 = list(collection2.find({'_id': ObjectId(new_document.inserted_id)}))
            found_document2 = list(collection3.find({'_id': ObjectId(new_document.inserted_id)}))

            #이게 실패해야하는데 성공함 ㅋㅋ.. 아래의 경우에서 시나리오대로 잘 작동하는거보면 내가 뭔가 놓쳤다고 믿고싶음
            # print(f'len1 {len(found_document1)}, len2 {len(found_document2)}')
            if(len(found_document1) != len(found_document2)):
                raise Exception('Document not found - Fail to get document from Secondary')
                    
        print('Success')
    except ValueError:
        print('error Occurred', ValueError)

def MR_fail_with_majority():
    try:
        print('start')

        # connect to Mongo
        client1 = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo', replicaSet = 'rs0')
        client2 = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo', replicaSet = 'rs0')

        # get collection
        collection1 = client1['test'].get_collection('collection')
        collection2 = client2['test'].get_collection('collection').with_options(read_preference= ReadPreference.PRIMARY, write_concern= write_concern.WriteConcern(w = 2), read_concern= read_concern.ReadConcern(level='majority'))
        collection3 = client2['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY, write_concern= write_concern.WriteConcern(w = 2), read_concern= read_concern.ReadConcern(level='majority'))

        # For 3 sec, write to Primary and get from Secondary
        start_time = time.time()
        while(time.time() - start_time < 3):
            # insert new element 
            new_document = collection1.insert_one({'합격기': 1})
            found_document1 = list(collection2.find({'_id': ObjectId(new_document.inserted_id)}))
            found_document2 = list(collection3.find({'_id': ObjectId(new_document.inserted_id)}))

            # 돌려보면 개수가 다를때가 있어서 걸림. 의도한것처럼 majority 걸어주도라도 시간차가 생기는 경우가 있는듯
            # print(f'len1 {len(found_document1)}, len2 {len(found_document2)}')
            if(len(found_document1) != len(found_document2)):
                raise Exception('Document not found - Fail to get document from Secondary')
                    
        print('Success')
    except ValueError:
        print('error Occurred', ValueError)

def MR_with_majority_session():
    try:
        print('start')

        # connect to Mongo
        client1 = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo', replicaSet = 'rs0')
        client2 = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo', replicaSet = 'rs0')
        
        # start session
        session = client1.start_session(causal_consistency= True)

        # get collection
        collection1 = client1['test'].get_collection('collection')
        collection2 = client2['test'].get_collection('collection').with_options(read_preference= ReadPreference.PRIMARY, write_concern= write_concern.WriteConcern(w = 2), read_concern= read_concern.ReadConcern(level='majority'))
        collection3 = client2['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY, write_concern= write_concern.WriteConcern(w = 2), read_concern= read_concern.ReadConcern(level='majority'))

        # For 3 sec, write to Primary and get from Secondary
        start_time = time.time()
        while(time.time() - start_time < 3):
            # insert new element 
            new_document = collection1.insert_one({'합격기': 1})
            found_document1 = list(collection1.find({'_id': ObjectId(new_document.inserted_id)}, session=session))
            found_document2 = list(collection2.find({'_id': ObjectId(new_document.inserted_id)}, session=session))

            # 세션까지 더해주면 개수가 다른일이 안생김
            # print(f'len1 {len(found_document1)}, len2 {len(found_document2)}')
            if(len(found_document1) != len(found_document2)):
                raise Exception('Document not found - Fail to get document from Secondary')
                    
        print('Success')
    except ValueError:
        print('error Occurred', ValueError)

MR_fail()
# MR_fail_with_majority()
# MR_with_majority_session()