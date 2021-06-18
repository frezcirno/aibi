import rdflib

# 创建一个空图谱
g = rdflib.Graph()

# 解析一个在线RDF文件
result = g.parse("OpenPermID/industry.ttl", format='turtle')

# 循环遍历图谱中每一个三元组
for subj, pred, obj in g:
    # 空图谱检查
    print(subj.__str__(), pred.__str__(), obj.__str__())


# 打印三元组个数
print("graph has {} statements.".format(len(g)))
# prints graph has 86 statements.
