import os
path_ffmpeg = r'C:\软件安装\ffmpeg-N-104495-g945b2dcc63-win64-lgpl\ffmpeg-N-104495-g945b2dcc63-win64-lgpl\bin'
os.chdir(path_ffmpeg)
def fanhao_zhangma(path_dir):
    list_file = os.listdir(path_dir)
    list_ts = [path_dir+"\\"+i for i in list_file if ".ts" in i]
    for path_ts in list_ts:
        # print(path_ts)
        if os.path.exists(path_ts) and os.path.exists(path_ts.replace(".ts",".mp4")):
            os.remove(path_ts)
            print("{}已存在，删除ts".format(path_ts.replace(".ts",".mp4")))
        elif os.path.exists(path_ts) and not os.path.exists(path_ts.replace(".ts",".mp4")):
            os.system("ffmpeg -i \"{}\" -acodec copy -vcodec copy -f mp4 \"{}\"".
                      format(path_ts, path_ts.replace(".ts", '.mp4')))
            if os.path.exists(path_ts.replace(".ts", '.mp4')) and os.path.exists(path_ts):
                os.remove(path_ts)
                print("文件{}转换成mp4完成，删除ts完成".format(path_ts))
    # os.chdir(path_ffmpeg)
    #     os.system("ffmpeg -i \'{}\' -acodec copy -vcodec copy -f mp4 \'{}\'".
    #               format(path_mp4, path_mp4.replace(".ts", '.mp4')))
    #     if os.path.exists(path_mp4.replace(".ts", '.mp4')) and os.path.exists(path_mp4):
    #         os.remove(path_mp4)
    #         print("文件转换成mp4完成，删除ts完成")
if __name__ == '__main__':
    # fanhao_zhangma("E:\番号")
    # fanhao_zhangma(r'D:\hhh\\国产\\Miohot')
    fanhao_zhangma(r'C:\\番号')
    fanhao_zhangma(r'G:\\番号')
    fanhao_zhangma(r'F:\\番号')
    # fanhao_zhangma()
