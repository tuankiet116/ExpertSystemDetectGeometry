
id_count = 0


class Rule:
    def __init__(self, ants, con, desc=None):
        self.id = None
        self.antecedent = ants
        self.consequent = con
        self.description = desc
        self.__calculate_id__()

    #Tăng giá trị id để gán cho các luật
    def __calculate_id__(self):
        global id_count
        self.id = id_count
        id_count += 1

    def __str__(self):
        s = ''
        s += ('Rule: #%d\n' % self.id)
        if self.description:
            s += ('Description: %s\n' % self.description)
        s += 'IF\t\t'
        for ant in self.antecedent:
            s += ('%s\n' % ant)
            if ant != self.antecedent[-1]:
                s += ('\tand\t')
        s += ('THEN\t%s\n' % self.consequent)
        return s

if __name__ == '__main__':
    # r = Rule(['Tổng của hai cạnh lớn hơn cạnh thứ ba', 'Tôi là một phép thử'], "Phép thử là một tam giác", "Phép thử")
    # print(r)
    # rr = Rule(['Các cạnh đối diện song song', 'Các cạnh đối diện bằng nhau'], 'Kiểm tra là hình chữ nhật', 'Kiểm tra lại'
    # print(rr)
    pass
