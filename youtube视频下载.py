import os
# https://www.youtube.com/playlist?list=PLRyK_3dr0fGPS0iudVio2kJvFiY7mMTiX
# 虎牙骚舞
url = input('例如https://www.youtube.com/playlist?list=PLCAkpCGSoO0WR_80vk7eCi_k9VjOSOcBa\n输入你要下载的用户视频列表地址  ：')
# dir_name = input("例如'D:\\ghs\\猫的二十二'\n输入你要存储视频的目录路径 ：")
dir_name = r'G:\ghs\斗鱼虎牙'
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
os.chdir(dir_name)
os.system('yt-dlp -f \"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best\" ' + '\"'+url+'\"')