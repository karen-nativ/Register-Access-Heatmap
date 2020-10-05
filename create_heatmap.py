import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.widgets import RadioButtons
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
import random
import math
from collections import namedtuple

# NEEDS Matplotlib Version >= 3.1 (orientation)

# CONSTS
INTERPOLATION_DICT = {'Gradient': 'bilinear', 'Sharp': 'none'}
DUMMY_REGISTERS = {"LONG_REGISTER_NAME_"+ str(num) : (random.randrange(1,10), random.randrange(1, 10)) for num in range(1,100000)}
PAGE_DISPLAY_AMOUNT = 5




class reg_use:
    pass


def draw_heatmap(all_reg_info):
    reg_dict = {reg.name : (reg.read_count, reg.write_count) for reg in all_reg_info}
    reg_names = reg_dict.keys()
    if len(reg_names) == 0:
        print(">>>No accesses to registers found")
        return
    fig, ax = plt.subplots()
    
    display_amount = min(len(reg_names), PAGE_DISPLAY_AMOUNT)
    all_vals = [item for sublist in reg_dict.values() for item in sublist]
    img = ax.imshow([[min(all_vals)], [max(all_vals)]], aspect='auto', cmap='Greens', interpolation='bilinear', origin='upper') # First param is dummy data before it is updated
    


    # DRAW X LABELS
    x_label_list = ['Read', 'Write']
    ax.set_xticks([-0.5, 0.5])
    ax.set_xticklabels(x_label_list, fontsize=10)
    
    update_scroll(plt, 0, img, ax, list(reg_dict.values()), list(reg_names), display_amount)
    
    fig.colorbar(img)
    img.set_clim(vmin=0)
    
    
    
    # DISPLAY VALUE ON HOVER
    _Event = namedtuple('_Event', 'xdata ydata')
    ax.format_coord = lambda x, y : 'Value = ' + str(img.get_cursor_data(_Event(x, y)))
    img.format_cursor_data = lambda val : ''
    
    
    # DRAW RADIO BUTTONS
    radio_ax = plt.axes([0, 0, 1, 1], facecolor='lightgoldenrodyellow') #[posx, posy, width, height]
    radio_pos = InsetPosition(ax, [0, 1.02, 0.3, 0.14])
    radio_ax.set_axes_locator(radio_pos)
    radio = RadioButtons(radio_ax, ('Gradient', 'Sharp'))
    
    def radio_func(label):
        current_interpolation = INTERPOLATION_DICT[label]
        img.set_interpolation(current_interpolation)
        plt.draw()
    
    radio.on_clicked(radio_func)     
             
    
    
    # DRAW SCROLLBAR
    if len(reg_names) > PAGE_DISPLAY_AMOUNT:
        axpos = plt.axes([0.95, 0.01, 0.03, 0.9], facecolor='darkgrey')
        max_val = 2*(len(reg_names) - PAGE_DISPLAY_AMOUNT)
        spos = Slider(axpos, 'Scroll', 0, max_val, valinit=2*(len(reg_names) - PAGE_DISPLAY_AMOUNT), valstep=2, orientation='vertical', color='lightgrey')
        spos.valtext.set_visible(False)
        
        def update(val): # val is always a positive even integer
            update_scroll(plt, int(max_val-val), img, ax, list(reg_dict.values()), list(reg_names)) #The slider is backwards so reverse val
            plt.draw()
    
        spos.on_changed(update)
        
        def mouse_scroll(event):
            new_val = spos.val + event.step
            if new_val > max_val:
                new_val = max_val
            if new_val < 0:
                new_val = 0
            spos.set_val(new_val)
                
        fig.canvas.mpl_connect('scroll_event', mouse_scroll)
    
    plt.show()



def update_scroll(plt, val, img, ax, graph_data, reg_names, display_amount=PAGE_DISPLAY_AMOUNT):
    ax.axis([-1, 1, val + 2*display_amount, val])
    data_index = int(val / 2)
    current_display_data = graph_data[data_index:data_index + display_amount]
    current_display_data.reverse() # Reversed to show the original list first values at the top of the heatmap
    img.set_data(current_display_data) 
    img.set_extent([-1, 1, val, val + 2*display_amount])
    
    
    #ax.invert_yaxis() #Change origin to upper left
    y_label_list = reg_names[int(val/2):int(val/2) + display_amount]
    ax.set_yticks(range(val + 1, val + 2*display_amount, 2))
    ax.set_yticklabels(y_label_list)
    plt.tight_layout(rect=[0,0,1,0.9])
         

if __name__ == "__main__":
    print("This file is intended to be imported from specman module")


