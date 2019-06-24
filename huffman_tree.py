#定义一个树的类。
class Tree:
    def __init__(self, parent=-1,left=-1,right=-1,count=1e15,binary=0):
        self.parent = parent #父节点索引
        self.left = left    #左子树索引
        self.right = right  #右子树索引
        self.count = count  #权重，大小为每个label在数据集中出现的总次数。
        self.binary = binary #记录编码，在fasttext中，每个label被编码了（huffman编码）。

#找到权重最小的两个节点。
def find_2_min_node(huffman_tree,flag):
    #flag中记录了已经组合成树的节点，防止重复构建。
    mini = [0,1]
    #从第三个节点开始，循环选择权重小的节点，类似冒泡排序法。
    for i in range(2,len(huffman_tree)):
        if i in flag:
            continue
        else:
            if huffman_tree[i].count < max([huffman_tree[mini[0]].count,huffman_tree[mini[1]].count]):
                pos = 0 if huffman_tree[mini[0]].count > huffman_tree[mini[1]].count else 1
                mini[pos] = i
    return sorted(mini)

#padding数据的函数。
def pad_sequences(y,max_len):
	lengths = []
	for y_ in y:
		lengths.append(len(y_))
	if max_len == None:
		max_len = np.max(lengths)
	num_samples = len(y)
	sample_shape=tuple()
	for y_ in y:
		if not len(y_):
			continue
		sample_shape = np.asarray(y_).shape[1:]
		break
	result = (np.ones((num_samples,max_len)+sample_shape) * 0).astype('int32')

	for i,y_ in enumerate(y):
		if not len(y_):
			continue
		result_tmp = y_[:max_len]
		result_tmp = np.asarray(result_tmp,dtype='int32')
		result[i,:len(result_tmp)] = result_tmp
	return result
#构建huaffman树
def build_huffman_tree(counts):
# 参数counts为一个一维数组，索引位置代表每个label，值为此label的权重，即此label在数据集中出现的次数。
    label_num = len(counts)
    huffman_tree = []
    #huffman树的叶子节点为每个label,共label_num个。
    for i in range(0,label_num):
        huffman_tree.append(Tree(count=counts[i]))
    flag = []
    #huffman树的非叶子节点为label_num-1个。总节点数为2*label_num个。
    for i in range(label_num,2*label_num - 1):
        mini = find_2_min_node(huffman_tree, flag)
        flag.append(mini[0])
        flag.append(mini[1])
        #计算新节点的权重
        count = huffman_tree[mini[0]].count + huffman_tree[mini[1]].count

        node = Tree(left=mini[0],right=mini[1],count=count)
        #把新节点加入到列表中，列表中的节点为huffman树中的子树。
        huffman_tree.append(node)
        huffman_tree[mini[0]].parent = len(huffman_tree) - 1
        huffman_tree[mini[1]].parent = len(huffman_tree) - 1
        #右子树的编码为1。
        huffman_tree[mini[1]].binary = 1

    # 记录路径和每个label的编码。
    paths = []
    codes = []
    # 记录根节点到叶子节点的距离。
    path_length = []
    max_legth = 0
    for i in range(0,label_num):
        path = []
        code = []
        j = i
        while huffman_tree[j].parent != -1:
            path.append(huffman_tree[j].parent - label_num)

            code.append(int(huffman_tree[j].binary))
            j = huffman_tree[j].parent
        if len(patch)>max_legth:
            max_legth = len(patch)
        path_length.append(len(path))
        paths.append(path)
        codes.append(code)
    #padding一下。
    patch_padding = pad_sequences(paths,max_legth)
    codes_padding = pad_sequences(codes,max_legth)
    return huffman_tree, patch_padding, codes_padding, path_length
