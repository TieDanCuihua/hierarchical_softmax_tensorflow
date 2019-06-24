# hierarchical_softmax_tensorflow
#整理一下自己学过的东西，借鉴了https://github.com/BUAAQingYuan/fasttext，在他的代码上加了自己的注释和理解，以及适当的修改。

分层softmax技术，解决了当分类的种类过多时，计算量太大的问题。在fasttext中，就是用了此技术。

核心思想是根据label构建huffman树.叶子节点就是各个label，它们的权重就是此label在数据中出现的次数。把每个label根据huffman树编码。
huffman 树中的非叶子节点也要编码，编码的方法就是简单地embeding：假设label数为n，则非叶节点的个数为n-1,于是构建嵌入矩阵shape=[n-1,embedding_size],
接着用tf.nn.embedding_lookup得到每个非叶节点的嵌入向量patch.

假设隐藏层向量为h（隐藏层向量为每个输入单词embeding后按行相加后的结果。），则logits = tf.nn.sigmoid(tf.matmul(patch,tf.expand_dims(hidden,-1)))
而loss = tf.negative(tf.log(tf.multiply(flag,则logits) + tf.multiply(1-flag,1-则logits)))，这就是hierarchical_softmax的loss。
