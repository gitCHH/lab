# encoding=utf-8

def profile_cal(queue_size,v_c,v_g,init_size,grain):
    time=0
    time=time+max(v_c,v_g)*init_size
    new_ratio=int(v_c/(v_c+v_g)*(100-2*init_size))
    if new_ratio%grain!=0:
        if v_c>v_g:
            new_ratio=new_ratio-new_ratio%grain+grain
        else:
            new_ratio=new_ratio-new_ratio%grain
    return time+max(new_ratio*v_c,(100-init_size*2-new_ratio)*v_g)

def share_cal(queue_size,v_c,v_g,init_size,grain):
    time=0
    c_u_time=v_c*grain
    g_u_time=v_g*grain




