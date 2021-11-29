class Binomial:
    def __init__(self, size):
        self.size = size
        self.address = []
        self.tree = []
        self.data = None

        # make address model
        length = 2 ** size - 1
        cnt = 0
        for i in range(size):
            if i == 0:
                n = 0
                while n < length:
                    self.address.append([0])
                    n += 1
                cnt += 1
                continue
            for j in range(2**(i-1)):
                for k in range(2):
                    self.address[cnt].append(k)
                    cnt += 1
            n = cnt
            t = i+1
            while n < length:
                if n < cnt + 2**t / 2:
                    self.address[n].append(0)
                else:
                    self.address[n].append(1)
                n += 1
                if n == cnt + 2**t:
                    t += 1

    def __str__(self):
        if not self.tree:
            tree = 'Not append data'
        else:
            tree = self.tree
        return f'Binomial Object {super().__str__()}\n' + \
               f'Size: {self.size}\n' + \
               f'Address List: {str(self.address)}\n' + \
               f'Length: {len(self.address)}\n' + \
               f'Tree Form: {tree}'

    def append(self, data, simplify=False):
        if len(data) != self.size:
            raise MemoryError
        if simplify:
            self.data = _simplify(data)
        else:
            self.data = data
        node_cnt = 0
        cnt = 0
        for arr in self.data:
            if cnt == 0:
                try:
                    self.tree.append([self.address[cnt], arr[0]])
                except TypeError:
                    self.tree.append([self.address[cnt], arr])
                cnt += 1
                node_cnt += 1
                continue
            if 2**node_cnt != len(arr):
                raise MemoryError
            for i in arr:
                self.tree.append([self.address[cnt], i])
                cnt += 1
            node_cnt += 1
        return 1

    def path(self, node, index):
        if index >= 2**node:
            raise IndexError
        address_idx = 2**node-1+index
        return self.address[address_idx]

    def value(self, node, index):
        address = self.path(node, index)
        for i in self.tree:
            if i[0] == address:
                return i[1]
        return None

    def child(self, node, index):
        parent = self.path(node, index)
        path1 = parent.append(0)
        path2 = parent.append(1)
        children = []
        for i in self.tree:
            if i[0] == path1 or i[0] == path2:
                children.append(i[1])
        return children

    def exchange(self, node, index, value):
        address = self.path(node, index)
        i = 0
        while i < len(self.tree):
            if self.tree[i][0] == address:
                self.tree[i][1] = value
                self.data[node][index] = value
                return
            i += 1

    def change_model(self, func, *args, **kwargs):
        nd = 0
        for i in self.as_list():
            idx = 0
            for j in i:
                self.exchange(nd, idx, func(j, *args, **kwargs))
                idx += 1
            nd += 1
        return self

    def as_list(self):
        l_data = []
        for i in range(self.size):
            node_data = []
            for j in range(2**i):
                node_data.append(self.value(i, j))
            l_data.append(node_data)
        return l_data

    def beautify(self, __round=4):
        string = "| "
        layer = 0
        indent = 2
        size = self.size
        value_list = []

        cnt = 1
        for li in self.as_list():
            append_list = [li[0]]
            i = 1
            while i < len(li):
                if li[i] != li[i - 1]:
                    append_list.append(li[i])
                i += 1
            while len(append_list) < cnt:
                append_list.append(append_list[0])
            cnt += 1
            value_list.append(append_list)

        while layer < size:
            step = layer
            while step < size:
                value = str(round(value_list[step][layer], __round))
                if step == layer:
                    indent += len(value)
                string += value
                string += " | "
                step += 1

            if layer < size - 1:
                string += "\n" + (" " * indent) + " | "
            layer += 1
        return string


def model(tree, simplify=False):
    bi = Binomial(len(tree))
    bi.append(tree, simplify=simplify)
    return bi


def _simplify(data):
    if len(data) < 3:
        return data
    i = 1
    while i < len(data)-1:
        replace = []
        j = i+1
        k = 0
        n = k
        while k < len(data[i]):
            replace.append(data[j][n])
            replace.append(data[j][n+1])
            if k+1 == len(data[i]):
                break
            if data[i][k] != data[i][k+1]:
                n += 1
            k += 1
        data[j] = replace
        i += 1
    return data


if __name__ == "__main__":
    irm = [
        [0.0174],
        [0.0339, 0.0095],
        [0.05, 0.0256, 0.0011]
    ]
    b = Binomial(3)
    print(b)
    a = model(irm, simplify=True)
    c = a.as_list()[-1]
    print(c)
    a.change_model(round, 2)
    print(a.as_list())
