# 对象序列化
import pickle

# read obj from file
def readbunchobj(path):
    file_obj = open(path, 'rb')
    bunch = pickle.load(file_obj)
    file_obj.close()
    return bunch

# write obj to file
def writeBunchobj(path, obj):
    file_obj = open(path, 'wb')
    pickle.dump(obj, file_obj)
    file_obj.close()