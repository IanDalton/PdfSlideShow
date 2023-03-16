from screeninfo import get_monitors,Monitor

def get_largest_screen():
    dmax:Monitor = Monitor(0,0,0,0,0,0)
    
    for m in get_monitors():
        if dmax.height_mm*dmax.width_mm <= m.height_mm*m.width_mm:
            dmax=m
                
    return dmax

if __name__ == "__main__":
    for i in get_monitors():
        print(i)
    print(get_largest_screen())
