import execjs
# 如果需要逆向的js函数的实现出现在一个闭包中，那么直接将闭包的整个代码块拷贝进行调试就行
node = execjs.get()
ctx = node.compile(open('./fangkewang.js',encoding='utf-8').read())
funcName = "md5('{0}')".format('123456')
pwd = ctx.eval(funcName)
print(pwd)

