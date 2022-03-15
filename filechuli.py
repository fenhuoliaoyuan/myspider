import os

path_dir = r'G:\ghs\91porn'
pathDirList = [path_dir+ '\\'+i for i in os.listdir(path_dir)]
# print(pathDirList)
for D in pathDirList:
    dir_ = D.split('\\')[-1]
    files = os.listdir(D)
    if len(files) > 0:
        for i in files:
            if dir_ + ' ' not in i:
                path_old = D + '\\' + i
                print(path_old)
                path_new = D + '\\'+i.replace(dir_,dir_+' ')
                if not os.path.exists(path_new) :
                    os.renames(path_old,path_new)
                if '.ts' in path_old and os.path.exists(path_new):
                    os.remove(path_new)
                    print(path_old)
    # print()