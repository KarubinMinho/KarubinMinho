class SingleListNode:
    def __init__(self, _data, _next=None):
        """
        :param _data: 传入的Node数据
        Node设置两个属性 data: 访问自己内容 next: 指向下一个Node
        """
        self.data = _data
        self.next = _next

    def __repr__(self):
        return "<Node data:{} next:{}>".format(self.data, self.next)


class SingleLinkedList:
    """
    获取、删除head节点 末尾追加节点效率优化
    如果有其他方法的效率需求 继承此类并重写对应方法
    """
    def __init__(self):
        """初始化 头尾节点为空"""
        self.head = None
        self.tail = None

    def __len__(self):
        cur = self.head
        count = 0
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def __repr__(self):
        """用列表表示链接表元素 方便可视化"""
        cur = self.head
        human_readable = []
        while cur is not None:
            human_readable.append(cur.data)
            cur = cur.next
        return "<{}: {}>".format(__class__.__name__, str(human_readable))

    def is_empty(self):
        """判断是否为空链表"""
        return self.head is None

    def add(self, data):
        """添加节点 添加的data节点作为新的头节点"""
        node = SingleListNode(data, _next=self.head)
        self.head = node
        if node.next is None:
            self.tail = node

    def append(self, data):
        """向链表末尾追加节点"""
        node = SingleListNode(data)
        if self.is_empty():
            self.head = node
            self.tail = self.head
        else:
            self.tail.next = node
            self.tail = node

    def insert(self, pos, data):
        """将data插入pos位置之后"""
        if pos <= 0:
            self.add(data)
        elif pos > len(self) - 1:
            self.append(data)
        else:
            node = SingleListNode(data)
            cur = self.head
            count = 0
            while count < pos - 1:
                count += 1
                cur = cur.next
            node.next = cur.next
            cur.next = node

    def search(self, data):
        """从单链表中查找data节点"""
        cur = self.head  # 从头节点开始查询
        while cur is not None:  # 如果self不是空链表
            if cur.data == data:
                return True
            cur = cur.next
        return False  # 找到最后一个值(cur.next==None) 也没找到 返回False

    def remove(self, data):
        """从单链表中删除所有的data节点"""
        cur = self.head
        prev = None  # 记录前一个节点 head节点的前一个节点为None
        while cur is not None:
            if cur.data == data:
                if prev is None:  # 如果要删除的节点的为head节点
                    self.head = cur.next  # 直接更改head节点为head.next
                else:
                    prev.next = cur.next
                # break  # 只删除第一个找到的data节点 第一个找到之后 直接break
                # 如果要删除全部值为data的节点 删除完第一个找到的 继续判断下一个
                # 这样的话 数据量大的时候 效率非常低
                cur = cur.next
            else:
                prev = cur
                cur = cur.next
        self.tail = prev

    def remove_head(self):
        """删除head节点并返回 然后重设head节点"""
        cur = self.head
        self.head = cur.next
        return cur

