import os

from 转码 import fanhao_zhangma

path_name = '激情丛林 Tarzan-X_ Shame of Jane (1995).ts'
pathTsRoot = 'C:\\ts\\xsela_xyz'
path_root = 'G:\\ghs\\三级'
list_ts_file = os.listdir(pathTsRoot)
with open(path_name, 'ab') as ab:
    for row in ['dan' + j + '.ts' for j in sorted([i.replace('.ts', '').replace('dan', '') for i in list_ts_file])]:
        print(row)
        with open(pathTsRoot + '\\' + row, 'rb') as rb:
            ab.write(rb.read())
    print(path_name + '合并完成')
for j in [pathTsRoot + '\\' + i for i in list_ts_file]:
    # print(j)
    os.remove(j)
print('ts删除完成')
fanhao_zhangma(path_root)