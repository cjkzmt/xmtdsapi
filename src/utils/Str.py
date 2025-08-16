import re
num_map = {
    '0': '零', '1': '一', '2': '二', '3': '三', '4': '四',
    '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'
}
def 无单位(num): return ''.join(num_map[digit] for digit in num)
def 四位数(num):
    unit_map = ['', '十', '百', '千', '万', '亿']
    if num == '0': return num_map['0']
    num = num[::-1]
    result = []
    zero_flag = False
    
    for i, digit in enumerate(num):
        if digit == '0': zero_flag = True
        else:
            if zero_flag:
                result.append(num_map['0'])
                zero_flag = False
            if i == 1 and digit == '1' and not result: result.append(unit_map[i])
            else:
                if i > 0: result.append(unit_map[i])                
                if digit == '2' and i > 0 and unit_map[i] in ['百', '千' ]: result.append('两' if unit_map[i] in '百千' else '二')
                else: result.append(num_map[digit])
    result.reverse()
    if len(result) > 1 and result[0] == '一' and result[1] == '十':  result.pop(0)
    if result and result[-1] == '零': result.pop()
    q = ''.join(result)
    return  q 
def 有单位(num):
    dw=['', '万','亿',]
    reversed_str = num[::-1]
    parts = [reversed_str[i:i+4] for i in range(0, len(reversed_str), 4)]
    parts = [part[::-1] for part in parts]  # 反转每个部分
    parts.reverse()  # 反转整个列表
    s=len(parts)
    result=''
    for i, n in enumerate(parts):
        result+=四位数(n)+dw[(s-i-1)]
    return result

def 数转汉(num, unit):
    if len(num) == 4 and unit == "年": 
        return 无单位(num)
    if '.' in num:
        q, h = num.split('.')
        r= 有单位(q)+'点'+无单位(h)
    else: r=有单位(num)
    return r

def RemovePunctuation(t):
    if not isinstance(t, str):
        return ""
    t = t.strip()
    if not t:  # 处理空字符串
        return ""
    l = re.split(r'[\u3000-\u303F\uff00-\uff0b\uff0d-\uffef》《▶：…,，「」——~‘’“”"]#*', t) 
    b = [m.strip() for m in l if m.strip()]
    return ' '.join(b)


x='次翻新我就认三个死理：冬天不用抖'
print(RemovePunctuation(x))