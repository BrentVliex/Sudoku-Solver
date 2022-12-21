import pygame
import numpy as np
import time
import copy

pygame.font.init()
Window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("SUDOKU SOLVER")

row = 0
col = 0
diff = 500 / 9
value = 0
default_grid =[
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 3, 1, 0, 9, 0, 0, 0, 0],
            [0, 6, 5, 0, 0, 3, 1, 0, 0],
            [0, 0, 8, 9, 2, 4, 0, 0, 0],
            [1, 0, 0, 0, 5, 0, 0, 0, 6],
            [0, 0, 0, 1, 3, 6, 7, 0, 0],
            [0, 0, 9, 3, 0, 0, 5, 7, 0],
            [0, 0, 0, 0, 1, 0, 8, 4, 3],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
checked_pairs = []
checked_triples = []
font = pygame.font.SysFont("comicsans", 40)
font1 = pygame.font.SysFont("comicsans", 20)


def cord(pos):
    global row, col
    row = pos[1] // diff
    col = pos[0] // diff

def highlight_box():
    for k in range(2):
        pygame.draw.line(Window, (0, 0, 0), (int(col * diff - 3), int((row + k) * diff)), (int(col * diff + diff + 3), int((row + k) * diff)), 7)
        pygame.draw.line(Window, (0, 0, 0), (int((col + k) * diff), int(row * diff )), (int((col + k) * diff), int(row * diff + diff)), 7)  
       
def draw_lines():
    for fill_row in range (9):
        for fill_col in range (9):
            if default_grid[fill_row][fill_col] != 0:
                pygame.draw.rect(Window, (255, 255, 0), (int(fill_col * diff), int(fill_row * diff), int(diff + 1), int(diff + 1)))
                text1 = font.render(str(default_grid[fill_row][fill_col]), 1, (0, 0, 0))
                Window.blit(text1, (int(fill_col * diff + 15), int(fill_row * diff + 15)))

    for l in range(10):
        if l % 3 == 0 :
            thick = 7
        else:
            thick = 1

        pygame.draw.line(Window, (0, 0, 0), (0, int(l * diff)), (500, int(l * diff)), thick)
        pygame.draw.line(Window, (0, 0, 0), (int(l * diff), 0), (int(l * diff), 500), thick)     
 
    
def fill_value(value):
    text1 = font.render(str(value), 1, (0, 0, 0))
    Window.blit(text1, (int(col * diff + 15), int(row * diff + 15)))
 
def raise_error():
    text1 = font.render("wrong!", 1, (0, 0, 0))
    Window.blit(text1, (20, 570))

def raise_error1():
    text1 = font.render("wrong! enter a valid key for the game", 1, (0, 0, 0))
    Window.blit(text1, (20, 570)) 
 
def valid_value(grid, k, l, value, diagonal_constraint):
    for it in range(9):
        if grid[k][it] == value:
            return False
        if grid[it][l] == value:
            return False

    it = k // 3
    jt = l // 3

    for k in range(it * 3, it * 3 + 3):
        for l in range (jt * 3, jt * 3 + 3):
            if grid[k][l] == value:
                return False
    
    if diagonal_constraint:
        if k == l:
            for it in range(9):
                if grid[it][it] == value:
                    return False
        elif k + l == 8:
            for it in range(9):
                if grid[it][8 - it] == value:
                    return False

    return True

def update_options(grid, options, diagonal_constraint):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                key_name = str(f'r{r}c{c}')

                for num in range(1, 10):
                    if not valid_value(grid, r, c, num, diagonal_constraint):
                        if num in options[key_name]:
                            options[key_name].remove(num)

    return options

def solve_pencilmark(pencilmark_grid, diagonal_constraint, options = {},):
    print(10 * '=', "Solving with pencilmarks", 10 * '=')
    #Get all options for the empty cells
    if options == {}:
        for r in range(9):
            for c in range(9):
                if pencilmark_grid[r][c] == 0:
                    key_name = str(f'r{r}c{c}')
                    options[key_name] = []
                    for num in range(1, 10):
                        if valid_value(pencilmark_grid, r, c, num, diagonal_constraint):
                            options[key_name].append(num)

    #Sort dictionary from low to high
    key_list = list(sorted(options, key = lambda key: len(options[key])))

    for key in range(len(key_list)):
        #If there is only one option for a cell, fill it in
        if len(options[key_list[key]]) == 1:
            r = int(key_list[key][1])
            c = int(key_list[key][3])
            if valid_value(pencilmark_grid, r, c, options[key_list[key]][0], diagonal_constraint):
                global row, col
                row = r
                col = c
                fill_value(options[key_list[key]][0])
                print(f'{options[key_list[key]][0]} at r{row}c{col}')
                pencilmark_grid[row][col] = options[key_list[key]][0]
                Window.fill((255,182,193))
                draw_lines()
                highlight_box()
                pygame.display.update()
                pygame.time.delay(20)
                options.pop(key_list[key])
                options = update_options(pencilmark_grid, options, diagonal_constraint)
            
            if key != len(key_list) - 1:
                if len(options[key_list[key + 1]]) == 2:
                    solve_pencilmark(pencilmark_grid, diagonal_constraint, options)
                    return
    
    #Solving the sudoku with hidden singles
    times = sum([row.count(0) for row in pencilmark_grid])
    if times == 0:
        return True
    
    copy_grid = copy.deepcopy(pencilmark_grid)
    copy_options = copy.deepcopy(options)
    new_grid, new_options = hidden_singles(pencilmark_grid, options, diagonal_constraint)

    pencilmark_grid = new_grid
    options = new_options

    if new_grid != copy_grid or new_options != copy_options:
        solve_pencilmark(pencilmark_grid, diagonal_constraint, options)
        return

    #Solving the sudoku with naked pairs
    times = sum([row.count(0) for row in pencilmark_grid])
    if times == 0:
        return True

    copy_grid = copy.deepcopy(pencilmark_grid)
    copy_options = copy.deepcopy(options)
    new_grid, new_options = naked_pairs(pencilmark_grid, options, diagonal_constraint)
    
    pencilmark_grid = new_grid
    options = new_options

    if new_grid != copy_grid or new_options != copy_options:
        solve_pencilmark(pencilmark_grid, diagonal_constraint, options)
        return

    #Solving the sudoku with naked triples
    times = sum([row.count(0) for row in pencilmark_grid])
    if times == 0:
        return True

    copy_grid = copy.deepcopy(pencilmark_grid)
    copy_options = copy.deepcopy(options)
    new_grid, new_options = naked_triples(pencilmark_grid, options, diagonal_constraint)

    pencilmark_grid = new_grid
    options = new_options

    if new_grid != copy_grid or new_options != copy_options:
        solve_pencilmark(pencilmark_grid, diagonal_constraint, options)
        return

    #Solving the sudoku with hidden pairs
    times = sum([row.count(0) for row in pencilmark_grid])
    if times == 0:
        return True

    copy_options = copy.deepcopy(options)
    new_options = hidden_pairs(options, diagonal_constraint)

    options = new_options

    if new_options != copy_options:
        solve_pencilmark(pencilmark_grid, diagonal_constraint, options)
        return

    #Solving the sudoku with hidden triples
    times = sum([row.count(0) for row in pencilmark_grid])
    if times == 0:
        return True

    copy_options = copy.deepcopy(options)
    new_options = hidden_triples(options, diagonal_constraint)

    options = new_options

    if new_options != copy_options:
        solve_pencilmark(pencilmark_grid, diagonal_constraint, options)
        return

    #Solving the sudoku with pointing pairs
    times = sum([row.count(0) for row in pencilmark_grid])
    if times == 0:
        return True

    '''
    TO DO:
    - Pointing pairs
    - Box/line reduction
    '''

    return False

def hidden_singles(hidden_singels_grid, hidden_singels_options, diagonal_constraint):
    print('Solving with hidden singels')
    key_list = list(hidden_singels_options.keys())

    def check_list(check_list, grid, options, other_list1, other_list2):
        for num in range(1, 10):
            times = sum([cell[1].count(num) for cell in check_list])
            
            if times == 1:
                for cell in check_list:
                    if cell[1].count(num) == 1:
                        r = int(cell[0][1])
                        c = int(cell[0][3])

                        if grid[r][c] == 0:
                            if valid_value(grid, r, c, num, diagonal_constraint):
                                global row, col
                                row = r
                                col = c                                
                                fill_value(num)
                                print(f'{num} in cell {cell[0]}')
                                grid[row][col] = num
                                Window.fill((255,182,193))
                                draw_lines()
                                highlight_box()
                                pygame.display.update()
                                pygame.time.delay(20)
                                options.pop(cell[0])
                                options = update_options(grid, options, diagonal_constraint)

                                for other_cell in other_list1:
                                    if other_cell[0] == cell[0]:
                                        other_list1.remove(other_cell)

                                for other_cell in other_list2:
                                    if other_cell[0] == cell[0]:
                                        other_list2.remove(other_cell)

                        break
        return grid, options, other_list1, other_list2

    for i in range(9):
        key_list = list(hidden_singels_options.keys())
        row_list = []
        col_list = []
        box_list = []

        for key in key_list:
            if key[1] == str(i):
                row_list.append((key, hidden_singels_options[key]))
            if key[3] == str(i):
                col_list.append((key, hidden_singels_options[key]))
            if (int(key[1]) // 3) * 3 + (int(key[3]) // 3) == i:
                box_list.append((key, hidden_singels_options[key]))

        copy_grid = copy.deepcopy(hidden_singels_grid)
        copy_options = copy.deepcopy(hidden_singels_options)

        new_grid, new_options, col_list, box_list = check_list(row_list, hidden_singels_grid, hidden_singels_options, col_list, box_list)

        if new_grid != copy_grid or new_options != copy_options:
            hidden_singels_grid == new_grid
            hidden_singels_options == new_options

        copy_grid = copy.deepcopy(hidden_singels_grid)
        copy_options = copy.deepcopy(hidden_singels_options)

        new_grid, new_options, row_list, box_list = check_list(col_list, hidden_singels_grid, hidden_singels_options, row_list, box_list)

        if new_grid != copy_grid or new_options != copy_options:
            hidden_singels_grid == new_grid
            hidden_singels_options == new_options

        copy_grid = copy.deepcopy(hidden_singels_grid)
        copy_options = copy.deepcopy(hidden_singels_options)

        new_grid, new_options, row_list, col_list = check_list(box_list, hidden_singels_grid, hidden_singels_options, row_list, col_list)

        if hidden_singels_grid != copy_grid or hidden_singels_options != copy_options:
            hidden_singels_grid == new_grid
            hidden_singels_options == new_options

    return hidden_singels_grid, hidden_singels_options        

def naked_pairs(naked_pairs_grid, naked_pairs_options, diagonal_constraint):
    print('Solving with naked pairs')
    global row, col, checked_pairs
    pair_list = []
    key_list = list(sorted(naked_pairs_options, key = lambda key: len(naked_pairs_options[key])))

    for key1 in range(len(key_list) - 1):
        if len(naked_pairs_options[key_list[key1]]) == 2:
            for key2 in range(key1 + 1, len(key_list)):
                if naked_pairs_options[key_list[key1]] == naked_pairs_options[key_list[key2]] and (key_list[key1][1] == key_list[key2][1] or key_list[key1][3] == key_list[key2][3] or (int(key_list[key1][1]) // 3 == int(key_list[key2][1]) // 3 and int(key_list[key1][3]) // 3 == int(key_list[key2][3]) // 3)):
                    pair_list.append((key_list[key1], key_list[key2]))

                if key_list[key2] != key_list[-1]:
                    if len(naked_pairs_options[key_list[key2 + 1]]) > 2:
                        break

        if len(naked_pairs_options[key_list[key1 + 1]]) > 2:
            break

    for pair in pair_list:
        if pair not in checked_pairs:
            checked_pairs.append(pair)
            #Remove the pair from the other cells in the same row
            if pair[0][1] == pair[1][1]:
                for key in range(len(key_list)):
                    if key_list[key][1] == pair[0][1] and key_list[key] != pair[0] and key_list[key] != pair[1]:
                        for num in naked_pairs_options[pair[0]]:
                            if num in naked_pairs_options[key_list[key]]:
                                print(f'Removing {num} from cell {key_list[key]}, because of {pair[0]} and {pair[1]} in row {pair[0][1]}')
                                naked_pairs_options[key_list[key]].remove(num)

                                if len(naked_pairs_options[key_list[key]]) == 1:
                                    r = int(key_list[key][1])
                                    c = int(key_list[key][3])

                                    if naked_pairs_grid[r][c] == 0:
                                        if valid_value(naked_pairs_grid, r, c, naked_pairs_options[key_list[key]][0], diagonal_constraint):
                                            row = r
                                            col = c                                
                                            fill_value(num)
                                            print(f'{naked_pairs_options[key_list[key]][0]} in cell {key_list[key]}')
                                            naked_pairs_grid[row][col] = naked_pairs_options[key_list[key]][0]
                                            Window.fill((255,182,193))
                                            draw_lines()
                                            highlight_box()
                                            pygame.display.update()
                                            pygame.time.delay(20)
                                            naked_pairs_options.pop(key_list[key])
                                            naked_pairs_options = update_options(naked_pairs_grid, naked_pairs_options, diagonal_constraint)

            #Remove the pair from the other cells in the same column
            if pair[0][3] == pair[1][3]:
                for key in range(len(key_list)):
                    if key_list[key][3] == pair[0][3] and key_list[key] != pair[0] and key_list[key] != pair[1]:
                        for num in naked_pairs_options[pair[0]]:
                            if num in naked_pairs_options[key_list[key]]:
                                print(f'Removing {num} from {key_list[key]}, because of {pair[0]} and {pair[1]} in column {pair[0][3]}')
                                naked_pairs_options[key_list[key]].remove(num)

                                if len(naked_pairs_options[key_list[key]]) == 1:
                                    r = int(key_list[key][1])
                                    c = int(key_list[key][3])

                                    if naked_pairs_grid[r][c] == 0:
                                        if valid_value(naked_pairs_grid, r, c, naked_pairs_options[key_list[key]][0], diagonal_constraint):
                                            row = r
                                            col = c                                
                                            fill_value(num)
                                            print(f'{naked_pairs_options[key_list[key]][0]} in cell {key_list[key]}')
                                            naked_pairs_grid[row][col] = naked_pairs_options[key_list[key]][0]
                                            Window.fill((255,182,193))
                                            draw_lines()
                                            highlight_box()
                                            pygame.display.update()
                                            pygame.time.delay(20)
                                            naked_pairs_options.pop(key_list[key])
                                            naked_pairs_options = update_options(naked_pairs_grid, naked_pairs_options, diagonal_constraint)

            #Remove the pair from the other cells in the same box
            if int(pair[0][1]) // 3 == int(pair[1][1]) // 3 and int(pair[0][3]) // 3 == int(pair[1][3]) // 3:
                for key in range(len(key_list)):
                    if int(key_list[key][1]) // 3 == int(pair[0][1]) // 3 and int(key_list[key][3]) // 3 == int(pair[0][3]) // 3 and key_list[key] != pair[0] and key_list[key] != pair[1]:
                        for num in naked_pairs_options[pair[0]]:
                            if num in naked_pairs_options[key_list[key]]:
                                box_row = int(pair[0][1]) // 3
                                box_col = int(pair[0][3]) // 3

                                if box_row == 0:
                                    if box_col == 0:
                                        box_num = 0
                                    elif box_col == 1:
                                        box_num = 1
                                    else:
                                        box_num = 2
                                elif box_row == 1:
                                    if box_col == 0:
                                        box_num = 3
                                    elif box_col == 1:
                                        box_num = 4
                                    else:
                                        box_num = 5
                                else:
                                    if box_col == 0:
                                        box_num = 6
                                    elif box_col == 1:
                                        box_num = 7
                                    else:
                                        box_num = 8

                                print(f'Removing {num} from {key_list[key]}, because of {pair[0]} and {pair[1]} in box {box_num}')
                                naked_pairs_options[key_list[key]].remove(num)

                                if len(naked_pairs_options[key_list[key]]) == 1:
                                    r = int(key_list[key][1])
                                    c = int(key_list[key][3])

                                    if naked_pairs_grid[r][c] == 0:
                                        if valid_value(naked_pairs_grid, r, c, naked_pairs_options[key_list[key]][0], diagonal_constraint):
                                            row = r
                                            col = c                                
                                            fill_value(num)
                                            print(f'{naked_pairs_options[key_list[key]][0]} in cell {key_list[key]}')
                                            naked_pairs_grid[row][col] = naked_pairs_options[key_list[key]][0]
                                            Window.fill((255,182,193))
                                            draw_lines()
                                            highlight_box()
                                            pygame.display.update()
                                            pygame.time.delay(20)
                                            naked_pairs_options.pop(key_list[key])
                                            naked_pairs_options = update_options(naked_pairs_grid, naked_pairs_options, diagonal_constraint)

    return naked_pairs_grid, naked_pairs_options

def naked_triples(naked_triples_grid, naked_triples_options, diagonal_constraint):
    print('Solving with naked triples')
    global row, col, checked_triples
    triples_list = []
    key_list = list(sorted(naked_triples_options, key = lambda key: len(naked_triples_options[key])))

    for key1 in range(len(key_list) - 2):
        if len(naked_triples_options[key_list[key1]]) <= 3:
            for key2 in range(key1 + 1, len(key_list) - 1):
                if len(naked_triples_options[key_list[key2]]) <= 3 and (key_list[key1][1] == key_list[key2][1] or key_list[key1][3] == key_list[key2][3] or (int(key_list[key1][1]) // 3 == int(key_list[key2][1]) // 3 and int(key_list[key1][3]) // 3 == int(key_list[key2][3]) // 3)):
                    for key3 in range(key2 + 1, len(key_list)):
                        if len(naked_triples_options[key_list[key3]]) <= 3:
                            #Check if triple is in the same row
                            if key_list[key1][1] == key_list[key2][1]:
                                if key_list[key1][1] == key_list[key3][1]:
                                    candidates = list(set(naked_triples_options[key_list[key1]] + naked_triples_options[key_list[key2]] + naked_triples_options[key_list[key3]]))

                                    if len(candidates) == 3:
                                        triples_list.append([key_list[key1], key_list[key2], key_list[key3]])

                            #Check if triple is in the same column
                            if key_list[key1][3] == key_list[key2][3]:
                                if key_list[key1][3] == key_list[key3][3]:
                                    candidates = list(set(naked_triples_options[key_list[key1]] + naked_triples_options[key_list[key2]] + naked_triples_options[key_list[key3]]))

                                    if len(candidates) == 3:
                                        triples_list.append([key_list[key1], key_list[key2], key_list[key3]])

                            #Check if triple is in the same box
                            if int(key_list[key1][1]) // 3 == int(key_list[key2][1]) // 3 and int(key_list[key1][3]) // 3 == int(key_list[key2][3]) // 3:
                                if int(key_list[key1][1]) // 3 == int(key_list[key3][1]) // 3 and int(key_list[key1][3]) // 3 == int(key_list[key3][3]) // 3:
                                    candidates = list(set(naked_triples_options[key_list[key1]] + naked_triples_options[key_list[key2]] + naked_triples_options[key_list[key3]]))

                                    if len(candidates) == 3:
                                        triples_list.append([key_list[key1], key_list[key2], key_list[key3]])

                        if key_list[key3] != key_list[-1]:
                            if len(naked_triples_options[key_list[key3 + 1]]) > 3:
                                break

                if len(naked_triples_options[key_list[key2 + 1]]) > 3:
                    break
        
        if len(naked_triples_options[key_list[key1 + 1]]) > 3:
            break

    for triple in triples_list:
        if triple not in checked_triples:
            checked_triples.append(triple)
            nums = list(set(naked_triples_options[triple[0]] + naked_triples_options[triple[1]] + naked_triples_options[triple[2]]))

            #Remove the triple from the other cells in the same row
            if triple[0][1] == triple[1][1] and triple[0][1] == triple[2][1]:
                for key in range(len(key_list)):
                    if key_list[key][1] == triple[0][1] and key_list[key] != triple[0] and key_list[key] != triple[1] and key_list[key] != triple[2]:
                        for num in nums:
                            if num in naked_triples_options[key_list[key]]:
                                print(f'Removing {num} from {key_list[key]}, because of {triple[0]}, {triple[1]} and {triple[2]} in row {triple[0][1]}')
                                naked_triples_options[key_list[key]].remove(num)

                                if len(naked_triples_options[key_list[key]]) == 1:
                                    r = int(key_list[key][1])
                                    c = int(key_list[key][3])

                                    if naked_triples_grid[r][c] == 0:
                                        if valid_value(naked_triples_grid, r, c, naked_triples_options[key_list[key]][0], diagonal_constraint):
                                            row = r
                                            col = c                                
                                            fill_value(num)
                                            print(f'{naked_triples_options[key_list[key]][0]} in cell {key_list[key]}')
                                            naked_triples_grid[row][col] = naked_triples_options[key_list[key]][0]
                                            Window.fill((255,182,193))
                                            draw_lines()
                                            highlight_box()
                                            pygame.display.update()
                                            pygame.time.delay(20)
                                            naked_triples_options.pop(key_list[key])
                                            naked_triples_options = update_options(naked_triples_grid, naked_triples_options, diagonal_constraint)

            #Remove the triple from the other cells in the same column
            if triple[0][3] == triple[1][3] and triple[0][3] == triple[2][3]:
                for key in range(len(key_list)):
                    if key_list[key][3] == triple[0][3] and key_list[key] != triple[0] and key_list[key] != triple[1] and key_list[key] != triple[2]:
                        for num in nums:
                            if num in naked_triples_options[key_list[key]]:
                                print(f'Removing {num} from {key_list[key]}, because of {triple[0]}, {triple[1]} and {triple[2]} in column {triple[0][3]}')
                                naked_triples_options[key_list[key]].remove(num)

                                if len(naked_triples_options[key_list[key]]) == 1:
                                    r = int(key_list[key][1])
                                    c = int(key_list[key][3])

                                    if naked_triples_grid[r][c] == 0:
                                        if valid_value(naked_triples_grid, r, c, naked_triples_options[key_list[key]][0], diagonal_constraint):
                                            row = r
                                            col = c                                
                                            fill_value(num)
                                            print(f'{naked_triples_options[key_list[key]][0]} in cell {key_list[key]}')
                                            naked_triples_grid[row][col] = naked_triples_options[key_list[key]][0]
                                            Window.fill((255,182,193))
                                            draw_lines()
                                            highlight_box()
                                            pygame.display.update()
                                            pygame.time.delay(20)
                                            naked_triples_options.pop(key_list[key])
                                            naked_triples_options = update_options(naked_triples_grid, naked_triples_options, diagonal_constraint)

            #Remove the triple from the other cells in the same box
            if int(triple[0][1]) // 3 == int(triple[1][1]) // 3 and int(triple[0][3]) // 3 == int(triple[1][3]) // 3 and int(triple[0][1]) // 3 == int(triple[2][1]) // 3 and int(triple[0][3]) // 3 == int(triple[2][3]) // 3:
                for key in range(len(key_list)):
                    if int(key_list[key][1]) // 3 == int(triple[0][1]) // 3 and int(key_list[key][3]) // 3 == int(triple[0][3]) // 3 and key_list[key] != triple[0] and key_list[key] != triple[1] and key_list[key] != triple[2]:
                        for num in nums:
                            if num in naked_triples_options[key_list[key]]:
                                box_row = int(triple[0][1]) // 3
                                box_col = int(triple[0][3]) // 3

                                if box_row == 0:
                                    if box_col == 0:
                                        box_num = 0
                                    elif box_col == 1:
                                        box_num = 1
                                    else:
                                        box_num = 2
                                elif box_row == 1:
                                    if box_col == 0:
                                        box_num = 3
                                    elif box_col == 1:
                                        box_num = 4
                                    else:
                                        box_num = 5
                                else:
                                    if box_col == 0:
                                        box_num = 6
                                    elif box_col == 1:
                                        box_num = 7
                                    else:
                                        box_num = 8

                                print(f'Removing {num} from {key_list[key]}, because of {triple[0]}, {triple[1]} and {triple[2]} in box {box_num}')
                                naked_triples_options[key_list[key]].remove(num)

                                if len(naked_triples_options[key_list[key]]) == 1:
                                    r = int(key_list[key][1])
                                    c = int(key_list[key][3])

                                    if naked_triples_grid[r][c] == 0:
                                        if valid_value(naked_triples_grid, r, c, naked_triples_options[key_list[key]][0], diagonal_constraint):
                                            row = r
                                            col = c                                
                                            fill_value(num)
                                            print(f'{naked_triples_options[key_list[key]][0]} in cell {key_list[key]}')
                                            naked_triples_grid[row][col] = naked_triples_options[key_list[key]][0]
                                            Window.fill((255,182,193))
                                            draw_lines()
                                            highlight_box()
                                            pygame.display.update()
                                            pygame.time.delay(20)
                                            naked_triples_options.pop(key_list[key])
                                            naked_triples_options = update_options(naked_triples_grid, naked_triples_options, diagonal_constraint)

    return naked_triples_grid, naked_triples_options

def hidden_pairs(hidden_pairs_options, diagonal_constraint):
    print('Solving with hidden pairs')
    key_list = list(hidden_pairs_options.keys())

    def check_list(check_list, options):
        appearances = {}
        
        for i in range(1, 10):
            times = sum([cell[1].count(i) for cell in check_list])

            if times == 2:
                appearances[i] = []
                for cell in check_list:
                    if i in cell[1]:
                        appearances[i].append(cell[0])

        appearances_keys = list(appearances.keys())
        
        for key in appearances_keys:
            appearances[key] = list(sorted(appearances[key]))

        for key1 in range(len(appearances_keys) - 1):
            for key2 in range(key1 + 1, len(appearances_keys)):
                if appearances[appearances_keys[key1]] == appearances[appearances_keys[key2]]:
                    for cell in appearances[appearances_keys[key1]]:
                        #Remove the options for the first cell
                        cell_options = list(options[cell])

                        for num in cell_options:
                            if num != appearances_keys[key1] and num != appearances_keys[key2]:
                                print(f'Removing {num} from {cell}, because of hidden pair {appearances_keys[key1]} and {appearances_keys[key2]} in cells {appearances[appearances_keys[key1]][0]} and {appearances[appearances_keys[key1]][1]}')
                                options[cell].remove(num)

        return options

    for i in range(9):
        key_list = list(hidden_pairs_options.keys())
        row_list = []
        col_list = []
        box_list = []

        for key in key_list:
            if key[1] == str(i):
                row_list.append((key, hidden_pairs_options[key]))
            if key[3] == str(i):
                col_list.append((key, hidden_pairs_options[key]))
            if (int(key[1]) // 3) * 3 + (int(key[3]) // 3) == i:
                box_list.append((key, hidden_pairs_options[key]))

        copy_options = copy.deepcopy(hidden_pairs_options)   

        new_options = check_list(row_list, hidden_pairs_options)

        if new_options != copy_options:
            hidden_pairs_options == new_options

        copy_options = copy.deepcopy(hidden_pairs_options)

        new_options = check_list(col_list, hidden_pairs_options)

        if new_options != copy_options:
            hidden_pairs_options == new_options

        copy_options = copy.deepcopy(hidden_pairs_options)

        new_options= check_list(box_list, hidden_pairs_options)

        if new_options != copy_options:
            hidden_pairs_options == new_options

    return hidden_pairs_options

def hidden_triples(hidden_triples_options, diagonal_constraint):
    print('Solving with hidden triples')
    key_list = list(hidden_triples_options.keys())

    def check_list(check_list, options):
        print('Check_list:\n', check_list)
        appearances = {}
        
        for i in range(1, 10):
            times = sum([cell[1].count(i) for cell in check_list])

            if 2 <= times <= 3:
                appearances[i] = []
                for cell in check_list:
                    if i in cell[1]:
                        appearances[i].append(cell[0])
                
                if times == 2:
                    print(f'{i} appears in cells {appearances[i][0]} and {appearances[i][1]}')
                elif times == 3:
                    print(f'{i} appears in cells {appearances[i][0]}, {appearances[i][1]} and {appearances[i][2]}')

        print(appearances)

        appearances_keys = list(appearances.keys())
        
        for key in appearances_keys:
            appearances[key] = list(sorted(appearances[key]))

        for key1 in range(len(appearances_keys) - 2):
            for key2 in range(key1 + 1, len(appearances_keys)):
                for key3 in range(key2 + 1, len(appearances_keys)):
                    cells = list(set(appearances[appearances_keys[key1]] + appearances[appearances_keys[key2]] + appearances[appearances_keys[key3]]))

                    if len(cells) == 3:
                        if 'r8c3' in cells and 'r8c4' in cells and 'r8c5' in cells:
                            a = 1
                            pass

                        for cell in cells:
                            #Remove the options for the cells
                            cell_options = list(options[cell])

                            for num in cell_options:
                                if num != appearances_keys[key1] and num != appearances_keys[key2] and num != appearances_keys[key3]:
                                    print(f'Removing {num} from {cell}, because of hidden triple {appearances_keys[key1]}, {appearances_keys[key2]} and {appearances_keys[key3]} in cells {cells[0]}, {cells[1]} and {cells[2]}')
                                    options[cell].remove(num)

                            print(options[cell])

        return options

    for i in range(9):
        key_list = list(hidden_triples_options.keys())
        row_list = []
        col_list = []
        box_list = []

        for key in key_list:
            if key[1] == str(i):
                row_list.append((key, hidden_triples_options[key]))
            if key[3] == str(i):
                col_list.append((key, hidden_triples_options[key]))
            if (int(key[1]) // 3) * 3 + (int(key[3]) // 3) == i:
                box_list.append((key, hidden_triples_options[key]))

        copy_options = copy.deepcopy(hidden_triples_options)   

        print('row_list', i)

        new_options = check_list(row_list, hidden_triples_options)

        if new_options != copy_options:
            hidden_triples_options == new_options

        copy_options = copy.deepcopy(hidden_triples_options)

        print('col_list', i )

        new_options = check_list(col_list, hidden_triples_options)

        if new_options != copy_options:
            hidden_triples_options == new_options

        copy_options = copy.deepcopy(hidden_triples_options)

        print('box_list', i)

        new_options = check_list(box_list, hidden_triples_options)

        if new_options != copy_options:
            hidden_triples_options == new_options

    return hidden_triples_options

def solve_brute_force(brute_force_grid, i, j, line, diagonal_constraint):
    if line == 'r':
        while brute_force_grid[i][j] != 0:
            if j < 8:
                j += 1
            elif j == 8 and i < 8:
                j = 0
                i += 1
            elif i == 8 and j == 8:
                return True
    elif line == 'c':
        while brute_force_grid[i][j] != 0:
            if i < 8:
                i += 1
            elif i == 8 and j < 8:
                i = 0
                j += 1
            elif i == 8 and j == 8:
                return True

    pygame.event.pump()

    for it in range(1, 10):
        if valid_value(brute_force_grid, i, j, it, diagonal_constraint) == True:
            brute_force_grid[i][j] = it
            global row, col
            row = i
            col = j
            Window.fill((255,182,193))
            draw_lines()
            highlight_box()
            pygame.display.update()
            pygame.time.delay(20)

            if solve_brute_force(brute_force_grid, i, j, line, diagonal_constraint) == 1:
                return True
            else:
                brute_force_grid[i][j] = 0

            Window.fill((255,182,193))
         
            draw_lines()
            highlight_box()
            pygame.display.update()
            pygame.time.delay(50)

    return False

def game_result():
    text1 = font.render("game finished", 1, (0, 0, 0))
    Window.blit(text1, (20, 570)) 


flag = True  
flag1 = 0
flag2 = 0
rs = 0
error = 0

while flag:
    Window.fill((255,182,193))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False   
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()
            cord(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                col -= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                col += 1
                flag1 = 1
            if event.key == pygame.K_UP:
                row -= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                row += 1
                flag1 = 1   
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                value = 1
            if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                value = 2   
            if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                value = 3
            if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                value = 4
            if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                value = 5
            if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                value = 6
            if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                value = 7
            if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                value = 8
            if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                value = 9 
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                brute_force = input('Solve the sudoku with brute force? (y/n): ')
                if brute_force == 'y':
                    col_or_row = input('Solve via rows or columns? (r/c): ')

                diagonal = input('Solve the sudoku with diagonal constraints? (y/n): ')
                if diagonal == 'y':
                    diagonal = True
                else:
                    diagonal = False
                flag2 = 1  

            if event.key == pygame.K_z:
                rs = 0
                error = 0
                flag2 = 0
                checked_pairs = []
                #003
                default_grid = [
                    [0, 0, 3, 0, 0, 0, 6, 0, 0],
                    [0, 7, 0, 0, 0, 3, 0, 5, 8],
                    [0, 0, 0, 1, 0, 0, 0, 7, 0],
                    [7, 2, 0, 0, 0, 1, 9, 0, 0],
                    [8, 0, 0, 0, 0, 0, 0, 0, 5],
                    [0, 0, 6, 9, 0, 0, 0, 8, 4],
                    [0, 5, 0, 0, 0, 7, 0, 0, 0],
                    [3, 4, 0, 6, 0, 0, 0, 2, 0],
                    [0, 0, 2, 0, 0, 0, 8, 0, 0]
                ]
            if event.key == pygame.K_x:
                rs = 0
                error = 0
                flag2 = 0
                checked_pairs = []
                #004
                default_grid = [
                    [8, 0, 0, 0, 0, 4, 0, 0, 1],
                    [2, 6, 0, 0, 1, 0, 8, 0, 0],
                    [0, 0, 0, 0, 0, 0, 3, 2, 0],
                    [4, 0, 6, 5, 2, 0, 0, 0, 0],
                    [9, 0, 0, 0, 0, 0, 0, 0, 6],
                    [0, 0, 0, 0, 8, 6, 2, 0, 4],
                    [0, 1, 5, 0, 0, 0, 0, 0, 0],
                    [0, 0, 8, 0, 7, 0, 0, 1, 3],
                    [3, 0, 0, 6, 0, 0, 0, 0, 8]
                ]
            if event.key == pygame.K_c:
                rs = 0
                error = 0
                flag2 = 0
                checked_pairs = []
                #005
                default_grid = [
                    [0, 0, 0, 0, 0, 4, 7, 0, 5],
                    [4, 0, 0, 9, 0, 0, 2, 0, 0],
                    [0, 7, 0, 0, 3, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 6, 0, 0, 4],
                    [0, 0, 5, 0, 4, 0, 3, 0, 0],
                    [2, 0, 0, 5, 0, 0, 0, 0, 0],
                    [0, 8, 0, 0, 1, 0, 0, 2, 0],
                    [0, 0, 3, 0, 0, 9, 0, 0, 7],
                    [9, 0, 1, 3, 0, 0, 0, 0, 0]
                ]
            if event.key == pygame.K_v:
                rs = 0
                error = 0
                flag2 = 0
                checked_pairs = []
                #006
                default_grid = [
                    [0, 0, 6, 1, 4, 9, 0, 0, 0],
                    [0, 0, 0, 2, 0, 0, 0, 8, 0],
                    [4, 0, 1, 0, 7, 0, 0, 2, 0],
                    [3, 8, 0, 0, 0, 0, 1, 0, 0],
                    [0, 6, 0, 0, 0, 0, 0, 4, 0],
                    [0, 0, 2, 0, 0, 0, 0, 5, 6],
                    [0, 5, 0, 0, 2, 0, 9, 0, 3],
                    [0, 7, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 5, 6, 3, 8, 0, 0]
                ]

            if event.key == pygame.K_r:
                rs = 0
                error = 0
                flag2 = 0
                checked_pairs = []
                default_grid = [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
            if event.key == pygame.K_d:
                rs = 0
                error = 0
                flag2 = 0
                checked_pairs = []
                default_grid =[
                    [0, 7, 0, 0, 0, 8, 0, 2, 9],
                    [0, 0, 2, 0, 0, 0, 0, 0, 4],
                    [8, 5, 4, 0, 2, 0, 0, 0, 0],
                    [0, 0, 8, 3, 7, 4, 2, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 3, 2, 6, 1, 7, 0, 0],
                    [0, 0, 0, 0, 9, 0, 6, 1, 2],
                    [2, 0, 0, 0, 0, 0, 4, 0, 0],
                    [1, 3, 0, 6, 0, 0, 0, 7, 0]
                ]
    if flag2 == 1:
        start_time = time.time()
        solved = False

        if brute_force == 'y':
            if solve_brute_force(default_grid , 0, 0, col_or_row, diagonal) == False:
                error = 1
            else:
                solved = True
                rs = 1
        else:
            if solve_pencilmark(default_grid, diagonal) == False:
                error = 1
            else:
                solved = True
                rs = 1
            
        flag2 = 0
        if solved:
            end_time = time.time()
            total_time = (end_time - start_time)
            print('It took ' + str(total_time) + ' seconds to solve the game')
        else:
            print('No solution found')

    if value != 0:           
        fill_value(value)
        if valid_value(default_grid, int(row), int(col), value, diagonal_constraint = False) == True:
            default_grid[int(row)][int(col)] = value
            flag1 = 0
        else:
            default_grid[int(row)][int(col)] = 0
            raise_error1()  
        value = 0   
    if error == 1:
        raise_error() 
    if rs == 1:
        game_result()       
    draw_lines() 
    if flag1 == 1:
        highlight_box()
             
    pygame.display.update() 

pygame.quit()
