import time

from bson.objectid import ObjectId
from pymongo import MongoClient, ReadPreference, read_concern, write_concern


def RYW_fail():
    try:
        print('start')

        # connect to Mongo
        # client = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo')
        client = MongoClient('mongodb://localhost:27017,localhost:27018,localhost:27019', replicaSet = 'rs0', readPreference = 'secondary', readPreferenceTags= 'usage:read', maxStalenessSeconds = 120, username = 'mongo', password='mongo')
        # print(client)

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
        # print(client)
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
        # print(client)
        
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



# 요기도 이상하게 2,3번은 의도대로 잘 작동하는데, 1번에서 실패하는게 안보임. 아마 내 로컬쪽 환경문제인듯함.
# RYW_fail()
# RYW_fail_with_majority()
RYW_with_majority_session()