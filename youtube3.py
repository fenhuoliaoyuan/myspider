# https://www.youtube.com/playlist?list=PLq02Ac8xtP-Dzuwz9B-IQKRz7Y9iWFu_C
import os
# https://www.youtube.com/playlist?list=PLRyK_3dr0fGPS0iudVio2kJvFiY7mMTiX
# 虎牙骚舞
url = input('例如https://www.youtube.com/playlist?list=PLCAkpCGSoO0WR_80vk7eCi_k9VjOSOcBa\n输入你要下载的用户视频列表地址  ：')
dir_name = input("例如'D:\\ghs\\猫的二十二'\n输入你要存储视频的目录路径 ：")
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
os.chdir(dir_name)
os.system('you-get ' + url)