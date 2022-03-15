import os

a = os.listdir(r'G:\ghs\91porn')
for user in a:
    path_root = r'G:\ghs\91porn' + '\\' + user
    b = os.listdir(path_root)
    if len(b) >0:
        for file in b:
            if user not in file:
                test_file = path_root + '\\'+user+file
                if os.path.exists(test_file):
                    print('存在')
                    print(test_file)
                    os.remove(path_root+'\\'+file)
                    print('删除重复{}'.format(path_root+'\\'+file))
                else:
                    os.rename(path_root+'\\'+file,test_file)