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
    if v_c>v_g:
        print('vc>vg(time/data) wait time: ',time-v_g*init_size)
    else:
        print('vg>vc(time/data) wait time: ',time-v_c*init_size)
    new_ratio_remain = int(v_g / (v_c + v_g) * (100 - 2 * init_size))
    if new_ratio_remain % grain != 0:
        if v_g > v_c:
            new_ratio_remain = new_ratio_remain - new_ratio_remain % grain + grain
        else:
            new_ratio_remain = new_ratio_remain - new_ratio_remain % grain
    return time + max(new_ratio_remain * v_c, (100 - init_size * 2 - new_ratio_remain) * v_g)


def share_cal(queue_size, v_c, v_g, grain):
    '''
    数据块作为双端队列
    :param queue_size: 数据总量
    :param v_c: 单位是 时间每1%数据量
    :param v_g:
    :param grain: 单位数据量
    :return: 总时间
    '''
    time = 0
    new_ratio = int(v_g / (v_c + v_g))
    if v_c>v_g:
        print('vc>vg(time/data)')
    else:
        print('vg>vc(time/data)')
    remainder = new_ratio % grain
    if remainder != 0:
        new_ratio=new_ratio-remainder
        gpu_ratio = 100-new_ratio-grain
    c_elapse=v_c*new_ratio
    g_elapse=v_g*gpu_ratio
    if c_elapse>g_elapse:
        print('last is gpu: ',v_g*grain)
        return time+max(c_elapse,g_elapse)+v_g*grain
    else:
        print('last is cpu: ',v_c*grain)
        return time+max(c_elapse,g_elapse)+v_c*grain

def aware(queue_size,v_c,c_g,grain):


