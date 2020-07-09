import pymongo 
import json
## input data ##
Host_port = input("insert prot number (default is '27017') : ")
if Host_port == '':
    Host_port = '27017'
dbName = input("insert db name (default is 'instances') : ")
if dbName == '':
    dbName = 'instances'
instances_train = input("isert name of train file (default is 'instances_train.json') : ")
if instances_train == '':
    instances_train = 'instances_train.json'
instances_val = input("isert name of val file (default is 'instances_val.json') : ")
if instances_val == '':
    instances_val = 'instances_val.json'
## connect mongo ##
myclient = pymongo.MongoClient("mongodb://localhost:{}/".format(int(Host_port))) 
myclient.test_database
db = myclient["{}".format(dbName)]
trains = open('{}'.format(instances_train)) 
vals = open('{}'.format(instances_val)) 
Trains = json.load(trains)
Vals = json.load(vals)
## insert Trains Data ##
for key in Trains:
    col = db[key]
    col.drop()
    insert_Data = Trains[key]
    if isinstance(insert_Data,list):
        for data in insert_Data:
            Add = data
            if key in ['images','annotations']:
                Add['source'] = instances_train
            col.insert_one(Add)
    elif isinstance(insert_Data,dict):
        Add = insert_Data
        if key in ['images','annotations']:
            Add['source'] = instances_train
        col.insert_one(Add)
    else:
        col = db['more']
        insert_Data = {key:Trains[key]}
        col.insert_one(insert_Data)
## insert Vals Data only from  ['images','annotations'] ##
for key in ['images','annotations']:
    col = db[key]
    insert_Data = Vals[key]
    if isinstance(insert_Data,list):
        for data in insert_Data:
            Add = data
            Add['source'] = instances_val
            col.insert_one(Add)
    elif isinstance(insert_Data,dict):
        Add = insert_Data
        Add['source'] = instances_val
        col.insert_one(Add)
    else:
        col = db['more']
        insert_Data = {key:Vals[key]}
        col.insert_one(insert_Data)
print("Done : db of {} created with from {} and {} files using port number of {}".format(dbName,instances_train,instances_val,Host_port))
    
        
