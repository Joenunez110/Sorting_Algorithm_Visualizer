import pygame
import random
import math
pygame.init()

class draw_Information: #This class will give the basic information to display the sorting
    BLACK = 0,0,0
    WHITE = 255, 255, 255
    GREEN = 0, 255,0
    RED = 255, 0 ,0
    BCKGROUND_COLOR = WHITE
    
    GRADIENTS = [
        (128,128,128),
        (160,160,160),
        (192,192,192)
    ]
    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)
    SIDE_PAD = 100
    TOP_PAD = 100
    
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm")
        self.set_list(lst)
        
    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info): #This function will allow a window to pop up giving options and aesthetics
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    
    controls = draw_info.FONT.render("R - reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1 , draw_info)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2,5))
    
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort ", 1 , draw_info)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2,5))
    
    draw_list(draw_info)
    pygame.display.update()
    

def draw_list(draw_info, color_position = {}, clear_bg = False): #draws the list of values as blocks on the screen
    lst = draw_info.lst
    
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD, 
                      draw_info.height - draw_info.TOP_PAD)
    pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
    
    if clear_bg:
        pygame.display.update()
        
    for i,val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        
        color = draw_Information.GRADIENTS[ i % 3]
        
        if i in color_position:
            color = color_position[i]
            
        pygame.draw.rect(draw_info.window, color(x, y, draw_info.block_width, draw_info.height))
        
    
def generate_starting_list(n, min_val, max_val): #creates a list of values to be sorted
    lst = []
    
    for i in range(n):
        val = random.randint(min_val,max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info, ascending =  True): #bubble sorting algorithm
    lst = draw_info.lst
    for i in range(len(lst - 1)):
        for j in (range(len(lst) - 1 - 1)):
            num1 = lst[j]
            num2 = lst[j + 1]
            
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j +1], lst[j]
                draw_list(draw_info, {
                                    j : draw_info.GREEN,
                                    j + 1 : draw_info.RED
                                     }, True)
                yield True
                
    return lst

def insertion_sort(): #insertion sorting algorithm
    pass

def main(): #main function that will run all of the visuals and algorithms
    run = True
    clock = pygame.time.Clock()
        
    n = 50
    min_val = 0
    max_val = 100
    
    lst = generate_starting_list(n, min_val,max_val)
    draw_info = draw_Information(800, 600, lst)
    sorting = False
    ascending = True
    
    sorting_algorithm = bubble_sort
    sorting_algo_name = 'Bubble sort'
    sorting_algo_generator = None
    
    while run:
        clock.tick(120)
        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
            
        draw(draw_info)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
                
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val,max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_SPACE and not sorting:
                ascending = False
                
    pygame.quit()            
    

if __name__ == "__main__":
    main()
    