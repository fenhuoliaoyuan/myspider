import os, subprocess
from time import sleep

def change_91():
    f1 = [r'D:\hhh\已找到文件\KESU (G)\ghs\91porn' + '\\' + i for i in os.listdir(r'D:\hhh\已找到文件\KESU (G)\ghs\91porn')]
    for j in f1:
        old_file_list = [j + '\\' + i for i in os.listdir(j)]
        for old_file_name in old_file_list:
            if '.ts' in old_file_name:
                new_file_name = old_file_name.replace('.ts', '.mp4')
                os.renames(old_file_name, new_file_name)
                print(new_file_name)
def delect_mp4():
    f1 = [r'G:\ghs\91porn' + '\\' + i for i in os.listdir(r'G:\ghs\91porn')]
    for j in f1:
        old_file_list = [j + '\\' + i for i in os.listdir(j)]
        for old_file_name in old_file_list:
            if '.ts' in old_file_name:
                if old_file_name.replace('.ts','.mp4') in old_file_list:
                    os.remove(old_file_name)
                    print(old_file_name)
def delect_yuanchuang():
    f1 = [r'G:\ghs\91porn' + '\\' + i for i in os.listdir(r'G:\ghs\91porn')]
    for j in f1:
        old_file_list = [j + '\\' + i for i in os.listdir(j)]
        for old_file_name in old_file_list:
            if '[原创]' in old_file_name:
                new_file_name = old_file_name.replace('[原创]','')
                os.renames(old_file_name,new_file_name)
                print(old_file_name)
def change_fanhao():
    old_file_list = [r'E:\番号' + '\\' + i for i in os.listdir(r'E:\番号')]
    for old_file_name in old_file_list:
        new_file_name = old_file_name.replace('mp4', 'ts')
        os.renames(old_file_name, new_file_name)
        print(new_file_name)


def change_91houru():
    f1 = [r'G:\ghs\91' + '\\' + i for i in os.listdir(r'G:\ghs\91')]
    for j in f1:
        old_file_list = [j + '\\' + i for i in os.listdir(j)]
        for old_file_name in old_file_list:
            new_file_name = old_file_name.replace('mp4', 'ts')
            if not os.path.exists(new_file_name):
                os.renames(old_file_name, new_file_name)
                print(new_file_name)


ffmpeg = r'C:\软件安装\ffmpeg-N-104495-g945b2dcc63-win64-lgpl\ffmpeg-N-104495-g945b2dcc63-win64-lgpl\bin\ffmpeg.exe'


def ts_change_to_mp4():
    f1 = [fr"G:\ghs\91porn" + "\\" + i for i in os.listdir(fr"G:\ghs\91porn")]
    for j in f1:
        f2 = [j + '\\' + i for i in os.listdir(j)]
        for old_file_name in f2:
            if ".ts" in old_file_name:
                new_file_name = old_file_name.replace("ts", "mp4")
                # subprocess.run(['ffmpeg', '-i', old_file_name, new_file_name])
                # print(new_file_name+'转换完成')
                cmd = ffmpeg + " -i " + old_file_name + " -c copy " + new_file_name
                try:
                    os.system(cmd)
                except:
                    pass
                else:
                    sleep(2)
                    if os.path.exists(new_file_name):
                        print("{}已存在".format(new_file_name))
                        os.remove(old_file_name)


def av_ts_change_to_mp4():
    f2 = [fr"E:\番号" + "\\" + i for i in os.listdir(fr"E:\番号")]
    for old_file_name in f2:
        if ".ts" in old_file_name:
            new_file_name = old_file_name.replace("ts", "mp4")
            # subprocess.run(['ffmpeg', '-i', old_file_name, new_file_name])
            # print(new_file_name+'转换完成')
            cmd = ffmpeg + " -i " + old_file_name + " -c copy " + new_file_name
            try:
                os.system(cmd)
            except:
                pass
            else:
                os.remove(old_file_name)

#
if __name__ == '__main__':
    # change_91()
    # change_fanhao()
    # change_91houru()
    # ts_change_to_mp4()
    # av_ts_change_to_mp4()
    # delect_mp4()
    delect_yuanchuang()