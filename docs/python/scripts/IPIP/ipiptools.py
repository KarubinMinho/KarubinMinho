from functools import wraps
from datetime import datetime
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

from netaddr import iprange_to_cidrs
from netaddr import cidr_merge


def time_logger(wrapped):
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        ret = wrapped(*args, **kwargs)
        delta = (datetime.now() - start).total_seconds()
        print(
            "{} {} took {:.2f}s".format(
                args[0].code,
                wrapped.__name__,
                delta))
        return ret
    return wrapper


IPIPFILE = Path('D:/PythonProjects/Project01/IPIP') / 'ipv4_china2_cn.txt'


class IPIPTools:
    def __init__(self, code, cidr=None):
        self.code = code
        self.__cidr = cidr

    def __repr__(self):
        return '<IPIPTools code: {}>'.format(self.code)

    def __gt__(self, other):
        return self.nums > other.nums

    def __eq__(self, other):
        return self.nums == other.nums

    def __ge__(self, other):
        return self.nums >= other.nums

    def __add__(self, other):
        return IPIPTools(self.code + other.code,
                         cidr_merge(self.merge2cidr() + other.merge2cidr()))

    @property
    def cidr(self):
        """
        :return: cidr of self.code
        """
        return self.__cidr

    @cidr.setter
    def cidr(self, value):
        self.__cidr = value

    @time_logger
    def merge2cidr(self):
        """
        :return: list of cidr
        """
        if self.cidr is None:
            cidr_lst = []
            with open(IPIPFILE, encoding='utf8') as file:
                for line in file:
                    if line.split()[-2] == self.code:
                        cidr_lst.extend(iprange_to_cidrs(*line.split()[:2]))
                    elif self.code == 'EU':
                        if line.split()[-1] == 'EU' and line.split()[-2] != 'RU':
                            cidr_lst.extend(iprange_to_cidrs(*line.split()[:2]))
            self.cidr = cidr_merge(cidr_lst)
        return self.cidr

    def write2file(self, dstpath=None):
        """
        :param dstpath: save_path of ipset file
        :return: None
        """
        if dstpath is None:
            save_path = Path(IPIPFILE).parent / 'ForeignSet'
            save_name = '{}.set'.format(self.code.lower())
        else:
            save_path = Path(dstpath).parent
            save_name = Path(dstpath).name
        if not save_path.exists():
            save_path.mkdir(parents=True, exist_ok=True)
        with open(save_path / save_name, 'w', encoding='utf8') as file:
            if self.cidr is None:
                merged = self.merge2cidr()
            else:
                merged = self.cidr
            lines = '\n'.join(map(str, merged))
            file.write(lines)

    def set_ipset_format(self, srcfile):
        """
        :param srcfile: file_path that need to be converted
        :return: None
        """
        # create ipset head
        maxelem = 65536
        prefix = 'add {}'.format(self.code.lower())
        if self.code in ('US', 'EU'):
            maxelem = 150528
        lines = [
            'create {} hash:net maxelem {}\n'.format(
                self.code.lower(), maxelem)]
        # rewrite format
        with open(srcfile, encoding='utf8') as file:
            line = map(lambda x: '{} {}'.format(prefix, x), file)
            lines.extend(line)
        with open(srcfile, 'w', encoding='utf8') as file:
            file.writelines(lines)

    @classmethod
    def get_codes(cls):
        """
        :return: all country iso code
        """
        with open(IPIPFILE, encoding='utf8') as file:
            all_codes = sorted({(line.split()[-2], line.split()[2])
                                for line in file}, key=lambda x: x[0])
            for k, v in all_codes:
                if k != '*':
                    print(k, v)

    @classmethod
    def get_isp(cls, limit=10):
        """
        :return: top limit isp
        """
        isp_dict = {}
        with open(IPIPFILE, encoding='utf8') as file:
            for line in file:
                key = line.split()[-3]
                if key in isp_dict:
                    isp_dict[key] += 1
                else:
                    isp_dict[key] = 1
        temp_lst = list(filter(lambda x: x[0] != '*',
                               sorted(isp_dict.items(), key=lambda x: x[1])))
        for i in range(1, limit + 1):
            print("{1:<10} {0}".format(*temp_lst[-i]))

    @property
    def nums(self):
        """
        :return: cidr length of merged
        """
        if self.cidr is None:
            return len(self.merge2cidr())
        return len(self.cidr)

    @classmethod
    def cidr2ban(cls):
        """
        :return: list of ban_cidr
        """
        ban_cidr = []
        ban_ips = ('GOOGLE.COM', 'FACEBOOK.COM', 'TWITTER.COM')
        with open(IPIPFILE, encoding='utf8') as file:
            for line in file:
                if line.split()[-3].upper() in ban_ips or \
                        line.split()[2].upper() in ban_ips:
                    ban_cidr.extend(iprange_to_cidrs(*line.split()[:2]))
        return cls('BANList', cidr_merge(ban_cidr))


if __name__ == '__main__':
    start = datetime.now()
    codes = ('HK', 'CN', 'SG', 'TW', 'JP', 'KR', 'RU', 'VN', 'AU', 'TH', 'IN',
             'CA', 'US', 'EU')
    # IPIPTools.cidr2ban()

    # sequenceExec 31.896s
    # for code in codes:
    #     ins = IPIPTools(code)
    #     ins.write2file()

    # MultiThreads 31.697s GIL
    # executor = ThreadPoolExecutor(max_workers=14)
    # with executor:
    #     for code in codes:
    #         ins = IPIPTools(code)
    #         future = executor.submit(ins.merge2cidr)

    # MultiProcess 13.937s
    executor = ProcessPoolExecutor(max_workers=8)
    with executor:
        for code in codes:
            ins = IPIPTools(code)
            future = executor.submit(ins.write2file)
    # convert to IPset Format
    for code in codes:
        ins = IPIPTools(code)
        ins.set_ipset_format(
            Path(IPIPFILE).parent /
            'ForeignSet' /
            f'{code}.set')
    delta = (datetime.now() - start).total_seconds()
    print('total took {}s'.format(delta))
