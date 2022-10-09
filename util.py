# Author: Bao Jx
from calendar import month
import re


def string_to_yuan(string, base_unit='y', right_side=False,normalize = True):
    """
    Convert the traditional expression of price to the numerical
    value in the measurement unit of yuan.
    e.g.
        >>  a = '4佰零七万9仟一百26元'
            b = '409万八千零71'
            c = '23万6.2千503'
            d = '23.1千802元'

        <<  4079126.0
            4098071.0
            236703.0
            23902.0

        >>  %timeit string_to_yuan('一百1拾九万3千零2拾3亿83.2万零三')
        <<  280 µs ± 14.2 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

    :param string: traditional expression of price
    :param base_unit:
    :param right_side:
    :return: numerical data
    """
    
    string = re.sub('两', '二', string)
    
    def normal(string):
        string = re.sub('億', '亿', string)
        string = re.sub('萬', '万', string)
        string = re.sub('仟', '千', string)
        string = re.sub('佰', '百', string)
        string = re.sub('拾', '十', string)
        string = re.sub('〇', '零', string)
        string = re.sub('壹', '一', string)
        string = re.sub('貳', '二', string)
        string = re.sub('叁', '三', string)
        string = re.sub('肆', '四', string)
        string = re.sub('伍', '五', string)
        string = re.sub('陆', '六', string)
        string = re.sub('柒', '七', string)
        string = re.sub('捌', '八', string)
        string = re.sub('玖', '九', string)
        string = re.sub('元|圓|圆', '', string)
        
        for i,n1 in enumerate(['一', '二','两', '三', '四', '五', '六', '七', '八', '九']):
            for j,n2 in enumerate(['一', '二','两', '三', '四', '五', '六', '七', '八', '九']):
                string = re.sub(n1 + n2, str(round((i+j)/2,1)), string)
                
        return string

    UNIT_SEQ = 'gsbqwy'
    BASE_UNIT = {'g': None, 's': '十', 'b': '百', 'q': '千', 'w': '万', 'y': '亿'}
    LEVEL_MAPPING = {'g': 10 ** 0, 's': 10 ** 1, 'b': 10 **
                     2, 'q': 10 ** 3, 'w': 10 ** 4, 'y': 10 ** 8}
    SINGLE_CHAR = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10 ** 1, '百': 10 ** 2,
                   '千': 10 ** 3, '万': 10 ** 4, '亿': 10 ** 8}

    if base_unit == 'y' and normalize:
        string = normal(string)

    if re.match('^\d+(\.\d*)?$', string):
        return float(string)

    if len(string) == 1 and string in SINGLE_CHAR.keys():
        if right_side:
            return SINGLE_CHAR[string] * LEVEL_MAPPING[base_unit]
        else:
            return SINGLE_CHAR[string]

    if right_side:
        return string_to_yuan(re.sub('^零', '', string))

    if string == '':
        return 0

    if len(re.split(BASE_UNIT[base_unit], string)) == 1:
        return string_to_yuan(string, UNIT_SEQ[UNIT_SEQ.index(base_unit) - 1])
    else:
        cur, odd = re.split(BASE_UNIT[base_unit], string)
        return LEVEL_MAPPING[base_unit] * string_to_yuan(cur, UNIT_SEQ[UNIT_SEQ.index(base_unit) - 1]) \
            + string_to_yuan(odd, UNIT_SEQ[UNIT_SEQ.index(base_unit) - 1], right_side=True)



def string_to_month(string:str)->int:
    has_year = string.find('年') != -1
    has_month = string.find('月') != -1
    string = re.sub('个', '', string)
    string = re.sub('零', '', string)
    year_month = re.split("[年月]", string)
    
    
    if has_year and has_month:
        return string_to_yuan(year_month[0],normalize=False) * 12 + string_to_yuan(year_month[1],normalize=False)
    elif has_year:
        return string_to_yuan(year_month[0],normalize=False) * 12
    else:
        return string_to_yuan(year_month[0],normalize=False)
        
if __name__=='__main__':
    print(string_to_yuan('三千元'))
    print(string_to_month('十五年五个月'))