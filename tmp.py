import time

from bson import BSON
from bson.objectid import ObjectId
from pymongo import MongoClient, ReadPreference, read_concern, write_concern

# def main():
#     try:
#         # master = MongoClient(host = 'localhost', port = 27017, directConnection=True)
#         # 아마 초기에 설정할때는 필요할둡.
#         # config = {
#         #     '_id': "rs0",
#         #     'members': [
#         #         {'_id': 0, 'host': "mongo1"}, // 태그셋도 같이 넣어줘야함. 
#         #         {'_id': 1, 'host': "mongo2"},
#         #         {'_id': 2, 'host': "mongo3"}
#         #     ]
#         # }
#         # master.admin.command("replSetInitiate", config)

#         # connect
#         client = MongoClient('mongodb://localhost:27017,localhost:27018,localhost:27019', replicaSet = 'rs0', readPreference = 'secondary', readPreferenceTags= 'usage:read', maxStalenessSeconds = 120, username = 'mongo', password='mongo')
#         print(client.admin.command('ismaster'))

#         #write 
#         collection = client['test'].get_collection('test')
#         # new_document = collection.insert_one({'z': 3})

#         # find
#         # print(new_document)
#         x = list(collection.find({}))

#         # start_time = time.time()
#         # while(time.time() - start_time < 3):
#         #     id = collection.insert_one({'x': 1})
#         #     found_document = collection.find_one()
#         #     print(id)
#     except ValueError:
#         print('error발생', ValueError)

# main()
