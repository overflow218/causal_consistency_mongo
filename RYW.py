import time

from bson import raw_bson
from pymongo import MongoClient, ReadPreference, collection


def main():
    try:
        # master = MongoClient(host = 'localhost', port = 27017, directConnection=True)
        # 아마 초기에 설정할때는 필요할둡.
        # config = {
        #     '_id': "rs0",
        #     'members': [
        #         {'_id': 0, 'host': "mongo1"},
        #         {'_id': 1, 'host': "mongo2"},
        #         {'_id': 2, 'host': "mongo3"}
        #     ]
        # }
        # master.admin.command("replSetInitiate", config)

        client = MongoClient('mongodb://localhost:27017,localhost:27018,localhost:27019', replicaSet = 'rs0', readPreference = 'secondaryPreferred', username = 'test', password='test')
        print(client.read_preference)
        print('client', client)
        collection = client.get_database('test-db').get_collection('test-collection', read_preference=ReadPreference.SECONDARY)
        print(collection)

        # 아래의 동작시 에러발생
        # print(client.list_database_names()) 
        start_time = time.time()
        # while(time.time() - start_time < 3):
        #     id = collection.insert_one({'x': 1})
        #     print(id)
    except ValueError:
        print('error발생', ValueError)

main()
'''
    while (sw.ElapsedMilliseconds < 5000)
    {
        var newDocument = new BsonDocument();
        collection.InsertOne(newDocument);
        var foundDocument = collection.Find(Builders<BsonDocument>.Filter.Eq(x => x["_id"], newDocument["_id"]))
            .FirstOrDefault();
        if (foundDocument == null)
            throw new Exception("Document not found");
    }
    
    Console.WriteLine("Success!");
'''