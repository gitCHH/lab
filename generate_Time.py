# encoding=utf-8

def profile_cal(queue_size, v_c, v_g, init_size, grain):
    '''

    :param queue_size:数据总量
    :param v_c: 单位是 时间每1%数据
    :param v_g:
    :param init_size:用于计算各处理器速度的数据量
    :param grain:单位数据量
    :return:总时间
    '''
    time = 0
    time = time + max(v_c, v_g) * init_size
    new_ratio_remain = int(v_g / (v_c + v_g) * (100 - 2 * init_size))
    if new_ratio_remain % grain != 0:
        if v_g > v_c:
            new_ratio_remain = new_ratio_remain - new_ratio_remain % grain + grain
        else:
            new_ratio_remain = new_ratio_remain - new_ratio_remain % grain
    return time + max(new_ratio_remain * v_c, (100 - init_size * 2 - new_ratio_remain) * v_g)


def share_cal(queue_size, v_c, v_g, grain):
    '''

    :param queue_size: 数据总量
    :param v_c: 单位是 时间每1%数据量
    :param v_g:
    :param grain: 单位数据量
    :return: 总时间
    '''
    time = 0
    new_ratio = v_c / (v_c + v_g)
    remainder = new_ratio % grain
    if new_ratio % grain != 0:
        gpu_ratio = 100 - new_ratio - (100 - new_ratio) * (remainder / new_ratio)
