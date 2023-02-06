import time

from bson.objectid import ObjectId
from pymongo import MongoClient, ReadPreference, read_concern, write_concern


def RYW_fail():
    try:
        print('start')

        # connect to Mongo
        client = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo')

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
        client = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo')

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
        client = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo')
        
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


def MR_fail():
    try:
        print('start')

        # connect to Mongo
        client = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo')

        # get collection
        collection1 = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.PRIMARY)
        collection2 = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY)
        
        # For 3 sec, write to Primary and get from Secondary
        start_time = time.time()
        while(time.time() - start_time < 3):
            # insert new element 
            new_document = collection1.insert_one({'합격기': 1})
            found_document1 = list(collection1.find({'_id': ObjectId(new_document.inserted_id)}))
            found_document2 = list(collection2.find({'_id': ObjectId(new_document.inserted_id)}))

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
        client = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo')

        # get collection
        collection1 = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.PRIMARY, write_concern= write_concern.WriteConcern(w = 2), read_concern= read_concern.ReadConcern(level='majority'))
        collection2 = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY, write_concern= write_concern.WriteConcern(w = 2), read_concern= read_concern.ReadConcern(level='majority'))

        # For 3 sec, write to Primary and get from Secondary
        start_time = time.time()
        while(time.time() - start_time < 3):
            # insert new element 
            new_document = collection1.insert_one({'합격기': 1})
            found_document1 = list(collection1.find({'_id': ObjectId(new_document.inserted_id)}))
            found_document2 = list(collection2.find({'_id': ObjectId(new_document.inserted_id)}))

            # 돌려보면 개수가 다를때가 있어서 걸림. 의도한것처럼 majority 걸어주도라도 시간차가 생기는 경우가 있는듯
            print(f'len1 {len(found_document1)}, len2 {len(found_document2)}')
            if(len(found_document1) != len(found_document2)):
                raise Exception('Document not found - Fail to get document from Secondary')
                    
        print('Success')
    except ValueError:
        print('error Occurred', ValueError)

def MR_with_majority_session():
    try:
        print('start')

        # connect to Mongo
        client = MongoClient('mongodb://localhost:27018', username = 'mongo', password='mongo')
        
        # start session
        session = client.start_session(causal_consistency= True)

        # get collection
        collection1 = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.PRIMARY, write_concern= write_concern.WriteConcern(w = 2), read_concern= read_concern.ReadConcern(level='majority'))
        collection2 = client['test'].get_collection('collection').with_options(read_preference= ReadPreference.SECONDARY, write_concern= write_concern.WriteConcern(w = 2), read_concern= read_concern.ReadConcern(level='majority'))

        # For 3 sec, write to Primary and get from Secondary
        start_time = time.time()
        while(time.time() - start_time < 3):
            # insert new element 
            new_document = collection1.insert_one({'합격기': 1}, session=session)
            found_document1 = list(collection1.find({'_id': ObjectId(new_document.inserted_id)}, session=session))
            found_document2 = list(collection2.find({'_id': ObjectId(new_document.inserted_id)}, session=session))

            # 세션까지 더해주면 개수가 다른일이 안생김
            # print(f'len1 {len(found_document1)}, len2 {len(found_document2)}')
            if(len(found_document1) != len(found_document2)):
                raise Exception('Document not found - Fail to get document from Secondary')
                    
        print('Success')
    except ValueError:
        print('error Occurred', ValueError)





# 요기도 이상하게 2,3번은 의도대로 잘 작동하는데, 1번에서 실패하는게 안보임. 아마 내 로컬쪽 환경문제인듯함.
# RYW_fail()
# RYW_fail_with_majority()
# RYW_with_majority_session()

# 2, 3번 의도대로 잘 작동. 1번이 잘 안먹히는데 확인필요
# MR_fail()
# MR_fail_with_majority()
# MR_with_majority_session()