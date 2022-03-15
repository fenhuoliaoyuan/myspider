import os

path_ffmpeg = r'C:\软件安装\ffmpeg-N-104495-g945b2dcc63-win64-lgpl\ffmpeg-N-104495-g945b2dcc63-win64-lgpl\bin'
def fanhao_zhangma(path_dir):
    os.chdir(path_ffmpeg)
    list_file = os.listdir(path_dir)
    list_ts = [path_dir + "\\" + i for i in list_file if ".avi" in i]
    for path_ts in list_ts:
        # print(path_ts)
        if os.path.exists(path_ts) and os.path.exists(path_ts.replace(".avi", ".mp4")):
            os.remove(path_ts)
            print("{}已存在，删除avi".format(path_ts.replace(".avi", ".mp4")))
        elif os.path.exists(path_ts) and not os.path.exists(path_ts.replace(".avi", ".mp4")):
            os.system("ffmpeg -i \"{}\" -c copy -map 0 \"{}\"".format(path_ts, path_ts.replace(".avi", '.mp4')))
            if os.path.exists(path_ts.replace(".ts", '.mp4')) and os.path.exists(path_ts):
                os.remove(path_ts)
                print("文件{}转换成mp4完成，删除ts完成".format(path_ts))
if __name__ == '__main__':
    fanhao_zhangma(r'F:\ghs\《震撼 泄密》推特极品长腿蜂腰翘臀美女yinqiqiqi付费欣赏视频41部 极度反差婊 呻吟声特勾魂87P+41V\V')