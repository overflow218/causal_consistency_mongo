import time

from bson.objectid import ObjectId
from pymongo import MongoClient, ReadPreference, read_concern, write_concern

'''
Read Your Write 시나리오
0. 비어있는 콜렉션이라 가정
1. 새로운 다큐먼트를 콜렉션에 추가한다.
2. 세컨더리에서 해당 다큐먼트를 읽을 수 있는지 체크한다
4. 1-2의 과정을 3초동안 반복한다
'''

def RYW_fail():
    try:
        print('start')

        # connect to Mongo
        # client = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo')
        client = MongoClient('mongodb://localhost:27017,localhost:27018,localhost:27019', replicaSet = 'rs0', readPreference = 'secondary', readPreferenceTags= 'usage:read', maxStalenessSeconds = 120, username = 'mongo', password='mongo')

        # get collection
        collection = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY)
        
        # For 3 sec, write to Primary and get from Secondary
        start_time = time.time()
        while(time.time() - start_time < 3):
            # insert new element 
            new_document = collection.insert_one({'합격기': 1})
            found_document = list(collection.find({'_id': ObjectId(new_document.inserted_id)}))

            # print(f'len -> {len(found_document)}')
            if(found_document == []):
                raise Exception('Document not found - Fail to get document from Secondary')
                    
        print('Success: insert to Primary, read from Secondary')
    except ValueError:
        print('error Occurred', ValueError)

def RYW_fail_with_majority():
    try:
        print('start')

        # connect to Mongo
        # client = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo')
        client = MongoClient('mongodb://localhost:27017,localhost:27018,localhost:27019', replicaSet = 'rs0', readPreference = 'secondary', readPreferenceTags= 'usage:read', maxStalenessSeconds = 120, username = 'mongo', password='mongo')

        # get collection
        collection = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY, write_concern= write_concern.WriteConcern(w = 2), read_concern= read_concern.ReadConcern(level='majority'))
        # collection = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY_PREFERRED, write_concern= write_concern.WriteConcern(w = 2))

        # For 3 sec, write to Primary and get from Secondary
        start_time = time.time()
        while(time.time() - start_time < 3):
            # insert new element 
            new_document = collection.insert_one({'합격기': 1})
            found_document = list(collection.find({'_id': ObjectId(new_document.inserted_id)}))

            # print(f'len -> {len(found_document)}')
            if(found_document == []):
                raise Exception('Document not found - Fail to get document from Secondary')
                    
        print('Success: insert to Primary, read from Secondary with read,write "majority"')
    except ValueError:
        print('error Occurred', ValueError)

def RYW_with_majority_session():
    try:
        print('start')

        # connect to Mongo
        # client = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo')
        client = MongoClient('mongodb://localhost:27017,localhost:27018,localhost:27019', replicaSet = 'rs0', readPreference = 'secondary', readPreferenceTags= 'usage:read', maxStalenessSeconds = 120, username = 'mongo', password='mongo')
        
        # start session
        session = client.start_session(causal_consistency= True)

        # get collection
        collection = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY, write_concern= write_concern.WriteConcern(w = 2), read_concern= read_concern.ReadConcern(level='majority'))

        # For 3 sec, write to Primary and get from Secondary
        start_time = time.time()
        while(time.time() - start_time < 3):
            # insert new element 
            new_document = collection.insert_one(document= {'합격기': 1}, session = session)
            found_document = list(collection.find({'_id': ObjectId(new_document.inserted_id)}, session = session))

            # print(f'len -> {len(found_document)}')
            if(found_document == []):
                raise Exception('Document not found - Fail to get document from Secondary')
                    
        print('Success: insert to Primary, read from Secondary with read,write "majority" and "session"')
    except ValueError:
        print('error Occurred', ValueError)


# RYW_fail()
# RYW_fail_with_majority()
# RYW_with_majority_session()