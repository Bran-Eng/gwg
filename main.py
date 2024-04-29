import cv2
import numpy as np
import pyautogui
import time
import keyboard
from pynput.mouse import Controller, Button
import pyautogui

# Disable the fail-safe
pyautogui.FAILSAFE = False

# Areas Coordinates
inventory_area = (0, 0, 2350, 2160)
bank_area = (2840, 1125, 3840, 2160)
tp_area = (2430, 60, 3840, 1090)
sell_search_area = (76, 1219, 2829, 2075)

compact = (2240, 184)
take_all = (2615, 1025)

rune_crafter = (937, 1540)
rune_crafter_salvage_green = (959, 1631) 

rune_crafter_confirm_button = (1811, 1415) # 
rune_crafter_confirm_button_1 = (1811, 1221) # Row 1
rune_crafter_confirm_button_2 = (1811, 1247) # Row 2
rune_crafter_confirm_button_3 = (1811, 1286) # Row 3
rune_crafter_confirm_button_4 = (1811, 1326) # Row 4
rune_crafter_confirm_button_5 = (1811, 1363) # Row 5
rune_crafter_confirm_button_6 = (1811, 1400) # Row 6


silver_fed = (1017, 1542)
silver_fed_use = (1040, 1558)
silver_fed_salvage_rare = (1040, 1670) 
silver_fed_salvage_stack = (1040, 1706)

silver_fed_confirm_button = (1811, 1247)
silver_fed_confirm_button_2 = (1811, 1219)
silver_fed_confirm_button_3 = (1811, 1286)
silver_fed_confirm_button_4 = (1811, 1327)
silver_fed_salvage_stack_accept = (1900, 1155) 

# Trading Post Sell Areas
sellers_list = (3163, 746)
maximum_amount = (3280, 358)
minus_one = (2986, 362)
minus_one_copper = (3240, 423)
list_item = (3002, 556)

mistlock = (744, 1535)
dragon_fall = (837, 1535)


def capture_game_screen():
    monitor_1_region = (0, 0, 3840, 2160)
    game_screenshot = pyautogui.screenshot(region=monitor_1_region)
    game_screenshot_np = np.array(game_screenshot)
    game_screenshot_processed = cv2.cvtColor(game_screenshot_np, cv2.COLOR_BGR2GRAY)
    return game_screenshot_processed

def search_for_item(image_path, threshold):      
    screenshot_gray = capture_game_screen() 
    itemImage = cv2.imread(image_path, 0)
    w, h = itemImage.shape[::-1]
    res = cv2.matchTemplate(screenshot_gray, itemImage, cv2.TM_CCOEFF_NORMED)    
    loc = np.where(res >= threshold)

    # Check if any match was found
    if np.any(res >= threshold):
        return loc, w, h
    else:
        return None, None, None
    
def use_all_green_gear(center_x, center_y):    
    pyautogui.moveTo(center_x, center_y)
    pyautogui.rightClick()
    time.sleep(0.25)
    pyautogui.move(85, 205)  # Move to "Use All"
    pyautogui.click()    

def find_and_click(step=0):
    image_path = './items-to-sell/green.png'
    threshold=0.55
    
    if step == 1 or step == 2:
        loc, w, h = search_for_item(image_path, threshold)
        if loc is not None:
            for pt in zip(*loc[::-1]):
                center_x, center_y = pt[0] + w/2, pt[1] + h/2
                
                if step == 1 and inventory_area[0] <= center_x <= inventory_area[0] + inventory_area[2] and inventory_area[1] <= center_y <= inventory_area[1] + inventory_area[3]:
                    use_all_green_gear(center_x, center_y)
                    return True
                
                elif step == 2 and bank_area[0] <= center_x <= bank_area[0] + bank_area[2] and bank_area[1] <= center_y <= bank_area[1] + bank_area[3]:
                    pyautogui.moveTo(center_x, center_y)
                    pyautogui.doubleClick()
                    time.sleep(0.25)
                    find_and_click(step=1)
                    return True   
    
    elif step == 3:
        attempt = 0
        max_attempts = 10
        while attempt < max_attempts:
            pyautogui.moveTo(3280, 1800) # Move to a position to initiate scroll
            for _ in range(10):
                pyautogui.scroll(-500)
            time.sleep(0.25)
            
            # Attempt to execute step 2
            if find_and_click(step=2):
                return True
            attempt += 1  # Increment the attempt counter

        return False  # If after 10 attempts it fails, return False
        
    # if step == 3: ...
    # if step == 4: ...

def manage_unidentified_gear():
    # Attempt to find Unidentified Gear Masterwork in the inventory and use all.
    if not find_and_click(step=1):
        if not find_and_click(step=2):
            if not find_and_click(step=3):
                pass    
            
# ---------------------------------------------------------------------------- #
#                                    Part 2                                    #
# ---------------------------------------------------------------------------- #
            
def use_salvage_kits():
    # Use Runecrafter for salvaging greens
    pyautogui.moveTo(rune_crafter[0], rune_crafter[1])
    pyautogui.rightClick() 
    time.sleep(0.5)
    pyautogui.click(rune_crafter_salvage_green[0], rune_crafter_salvage_green[1])
    time.sleep(0.5)
    pyautogui.click(rune_crafter_confirm_button[0], rune_crafter_confirm_button[1])
    pyautogui.click(rune_crafter_confirm_button_1[0], rune_crafter_confirm_button_1[1])
    pyautogui.click(rune_crafter_confirm_button_2[0], rune_crafter_confirm_button_2[1])
    pyautogui.click(rune_crafter_confirm_button_3[0], rune_crafter_confirm_button_3[1])
    pyautogui.click(rune_crafter_confirm_button_4[0], rune_crafter_confirm_button_4[1])
    pyautogui.click(rune_crafter_confirm_button_5[0], rune_crafter_confirm_button_5[1])
    pyautogui.click(rune_crafter_confirm_button_6[0], rune_crafter_confirm_button_6[1])
    pyautogui.moveTo(1200, 170)
    time.sleep(24)

    # Use Silver Fed for salvaging rares
    pyautogui.moveTo(silver_fed[0], silver_fed[1])
    pyautogui.rightClick()
    time.sleep(0.25)
    pyautogui.click(silver_fed_salvage_rare[0], silver_fed_salvage_rare[1])
    time.sleep(0.5)
    # Press confirm button using 3 coordinates for tackling possible placements
    pyautogui.click(silver_fed_confirm_button[0], silver_fed_confirm_button[1])
    pyautogui.click(silver_fed_confirm_button_2[0], silver_fed_confirm_button_2[1])
    pyautogui.click(silver_fed_confirm_button_3[0], silver_fed_confirm_button_3[1])
    pyautogui.click(silver_fed_confirm_button_4[0], silver_fed_confirm_button_4[1])
    pyautogui.moveTo(1200, 170)
    time.sleep(2.2)    
    pyautogui.click(compact[0], compact[1])
    
def manage_ectos():
    # Identify ectos by image to salvage
    image_path = './items-to-sell/globs_of_ectoplasm.png'  
    loc, w, h = search_for_item(image_path, 0.7)

    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template

            # Check if the center of the found item is within the defined area
            if inventory_area[0] <= center_x <= inventory_area[0] + inventory_area[2] and inventory_area[1] <= center_y <= inventory_area[1] + inventory_area[3]:
                pyautogui.moveTo(silver_fed[0], silver_fed[1])
                pyautogui.rightClick()
                time.sleep(0.5)
                pyautogui.click(silver_fed_salvage_stack[0], silver_fed_salvage_stack[1]) 
                time.sleep(0.5)

                pyautogui.moveTo(pt[0] + w/2, pt[1] + h/2)  # Click on the identified ecto
                pyautogui.click()
                time.sleep(0.5)
                pyautogui.click(silver_fed_salvage_stack_accept[0], silver_fed_salvage_stack_accept[1])
                time.sleep(9)
                break  
        
def manage_cristallyne_dust():   
    # Identify drystalline dust by image to sell
    image_path = './items-to-sell/pile_of_cristallyne_dust.png'  
    loc, w, h = search_for_item(image_path, 0.85)

    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template
            
            # Check if the center of the found item is within the defined area
            if sell_search_area[0] <= center_x <= sell_search_area[0] + sell_search_area[2] and sell_search_area[1] <= center_y <= sell_search_area[1] + sell_search_area[3]:
                pyautogui.click(pt[0] + w/2, pt[1] + h/2)  # Click on the identified crystallyne
                pyautogui.rightClick()
                time.sleep(0.5)
                pyautogui.move(53, 125) 
                pyautogui.click()
                time.sleep(4) 

                pyautogui.click(sellers_list[0], sellers_list[1]) # Add to sell list
                time.sleep(0.25)
                pyautogui.click(maximum_amount[0], maximum_amount[1]) # Maximum Amount
                time.sleep(0.25)
                pyautogui.click(minus_one_copper[0], minus_one_copper[1])  # Minus One Copper
                time.sleep(0.25)
                pyautogui.click(list_item[0], list_item[1]) # List
                time.sleep(5) # Time after sell
                break 
        
def consume_purple_luck():
    # Identify purple_luck
    image_path = './items-to-sell/purple_luck.png'  
    loc, w, h = search_for_item(image_path, 0.9)
    if loc is not None:
        for pt in zip(*loc[::-1]):
            pyautogui.rightClick(pt[0] + w/2, pt[1] + h/2)  # Click on the identified purple luck
            # pyautogui.rightClick()
            time.sleep(0.35)   
            break         
        
def consume_purple_luck_click_button():
    image_path = './items-to-sell/consume_all.png'  
    loc, w, h = search_for_item(image_path, 0.95)
    if loc is not None:
        for pt in zip(*loc[::-1]):
            pyautogui.click(pt[0] + w/2, pt[1] + h/2)  # Click on the consume all
            time.sleep(0.25)
            pyautogui.click(pt[0] + w/2, pt[1] + h/2)  # Click on the consume all
            break

def consume_luck():
    # Consume All Luck from multiple locations
    consume_luck_coords_list = [
        (1101, 1535),  
        (1191, 1535),  
        (1278, 1535),
        (1366, 1535),
        (1453, 1535),
        (1547, 1535),
        (1631, 1535)
    ]

    for coords in consume_luck_coords_list:
        pyautogui.moveTo(coords[0], coords[1])
        pyautogui.rightClick()
        time.sleep(0.25)
        pyautogui.move(16, 125) # Consume All
        # pyautogui.move(16, 164) # purple one
        pyautogui.click()
        time.sleep(0.25)

def sell_all_items():
    sell_items_coords_list = [
        (1717, 1620),
        (1812, 1620),
        (1897, 1620),
        (1985, 1620),
        (2077, 1620),
        (2163, 1620),
        (2250, 1620),
        (124, 1712),
        (215, 1712),
        (305, 1712),
        (392, 1712),
        (482, 1712),
        (570, 1712),
        (658, 1712),
        (744, 1712),
        (833, 1712),
        (924, 1712)
    ]

    for coords in sell_items_coords_list:
        pyautogui.moveTo(coords[0], coords[1])
        pyautogui.rightClick()
        time.sleep(0.25)
        pyautogui.move(16, 88) 
        pyautogui.click()
        time.sleep(3)        

        pyautogui.click(sellers_list[0], sellers_list[1]) # Add to sell list
        time.sleep(0.25)
        pyautogui.click(maximum_amount[0], maximum_amount[1]) # Maximum Amount
        time.sleep(0.25)
        pyautogui.click(list_item[0], list_item[1]) # List
        time.sleep(5) # Time after sell

def delete_dark_matter():
    # Identify dark matter
    image_path = './items-to-sell/globs_of_dark_matter.png'  
    loc, w, h = search_for_item(image_path, 0.7)
    if loc is not None:
        for pt in zip(*loc[::-1]):
            pyautogui.click(pt[0] + w/2, pt[1] + h/2)  # Click on the identified dark matter
            pyautogui.rightClick()
            time.sleep(0.25)
            pyautogui.move(16, 87) # Destroy dark matter
            pyautogui.click()
            time.sleep(0.25)
            pyautogui.click(1939, 1153) # Accept
            time.sleep(0.25) 
            break    

def sell_lucent_motes():
    # Identify lucent motes by image to sell
    image_path = './items-to-sell/lucent_motes.png'
    loc, w, h = search_for_item(image_path, 0.8)

    # Proceed if there are matches found
    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template
            
            # Check if the center of the found item is within the defined area
            if sell_search_area[0] <= center_x <= sell_search_area[0] + sell_search_area[2] and sell_search_area[1] <= center_y <= sell_search_area[1] + sell_search_area[3]:
                pyautogui.rightClick(center_x, center_y)  # Right-click on the identified lucent mote
                time.sleep(0.5)
                pyautogui.move(16, 88)  # Move cursor to "Sell" option
                pyautogui.click()
                time.sleep(3)  # Delay to allow UI to respond

                # Interact with the selling interface
                pyautogui.click(sellers_list[0], sellers_list[1])  # Click on add to sell list
                time.sleep(0.25)
                pyautogui.click(maximum_amount[0], maximum_amount[1])  # Click to set maximum amount
                time.sleep(0.25)
                pyautogui.click(list_item[0], list_item[1])  # Click to list the item for sale
                time.sleep(5)  # Wait for the transaction to process

                break  # Exit after processing the first valid item



def sell_mithril_ore():
    # Identify mithril ore by image to sell
    image_path = './items-to-sell/mithril_ore.png'
    loc, w, h = search_for_item(image_path, 0.85)
    
    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template

            # Check if the center of the found item is within the defined area
            if sell_search_area[0] <= center_x <= sell_search_area[0] + sell_search_area[2] and sell_search_area[1] <= center_y <= sell_search_area[1] + sell_search_area[3]:
                pyautogui.rightClick(pt[0] + w/2, pt[1] + h/2)  # Click on the identified crystallyne
                time.sleep(0.4)
                pyautogui.move(16, 88)
                pyautogui.click()
                time.sleep(2.6) 

                pyautogui.click(sellers_list[0], sellers_list[1]) # Add to sell list
                time.sleep(0.25)
                pyautogui.click(maximum_amount[0], maximum_amount[1]) # Maximum Amount
                time.sleep(0.25)
                pyautogui.click(list_item[0], list_item[1]) # List
                handle_errors()
                time.sleep(5) # Time after sell
                break

def sell_elder_wood_logs():
    # Identify elder wood logs by image to sell
    image_path = './items-to-sell/elder_wood_logs.png'
    loc, w, h = search_for_item(image_path, 0.7)

    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template

            # Check if the center of the found item is within the defined area
            if sell_search_area[0] <= center_x <= sell_search_area[0] + sell_search_area[2] and sell_search_area[1] <= center_y <= sell_search_area[1] + sell_search_area[3]:
                pyautogui.rightClick(pt[0] + w/2, pt[1] + h/2)  # Click on the identified crystallyne
                time.sleep(0.25)
                pyautogui.move(16, 88)
                pyautogui.click()
                time.sleep(2.6) 

                pyautogui.click(sellers_list[0], sellers_list[1]) # Add to sell list
                time.sleep(0.25)
                pyautogui.click(maximum_amount[0], maximum_amount[1]) # Maximum Amount
                time.sleep(0.25)
                pyautogui.click(list_item[0], list_item[1]) # List
                time.sleep(5) # Time after sell
                break

def sell_thick_leather_sections():
    # Identify thick leather sections by image to sell
    image_path = './items-to-sell/thick_leather_sections.png'
    loc, w, h = search_for_item(image_path, 0.7)

    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template

            # Check if the center of the found item is within the defined area
            if sell_search_area[0] <= center_x <= sell_search_area[0] + sell_search_area[2] and sell_search_area[1] <= center_y <= sell_search_area[1] + sell_search_area[3]:
                pyautogui.rightClick(pt[0] + w/2, pt[1] + h/2)  # Click on the identified crystallyne
                time.sleep(0.25)
                pyautogui.move(16, 88)
                pyautogui.click()
                time.sleep(2.6) 

                pyautogui.click(sellers_list[0], sellers_list[1]) # Add to sell list
                time.sleep(0.25)
                pyautogui.click(maximum_amount[0], maximum_amount[1]) # Maximum Amount
                time.sleep(0.25)
                pyautogui.click(list_item[0], list_item[1]) # List
                time.sleep(5) # Time after sell
                break

def sell_silk_scraps():
    # Identify silk scraps by image to sell
    image_path = './items-to-sell/silk_scraps.png'
    loc, w, h = search_for_item(image_path, 0.7)


    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template

            # Check if the center of the found item is within the defined area
            if sell_search_area[0] <= center_x <= sell_search_area[0] + sell_search_area[2] and sell_search_area[1] <= center_y <= sell_search_area[1] + sell_search_area[3]:
                pyautogui.rightClick(pt[0] + w/2, pt[1] + h/2)  # Click on the identified crystallyne
                time.sleep(0.25)
                pyautogui.move(16, 88)
                pyautogui.click()
                time.sleep(2.6) 

                pyautogui.click(sellers_list[0], sellers_list[1]) # Add to sell list
                time.sleep(0.25)
                pyautogui.click(maximum_amount[0], maximum_amount[1]) # Maximum Amount
                time.sleep(0.25)
                pyautogui.click(list_item[0], list_item[1]) # List
                time.sleep(5) # Time after sell
                break
        
def handle_errors():
    # Press cancel buttons
    err_buttons_coords_list = [
        (2119, 1156),  
        (2129, 1181),        
    ]

    for coords in err_buttons_coords_list:
        pyautogui.click(coords[0], coords[1])
        time.sleep(0.25)

def restart_game():
    pyautogui.click(1800, 500)

    # Coordinates for game icon, login, start game, and character selection
    game_icon_coords = (180, 2122)
    login_button_coords = (1203, 1327)
    character_coords = (1600, 2015)
    volunteer = (78, 1176)

    # Close windows to volunteer    
    keyboard.press_and_release('esc')
    time.sleep(0.25)
    keyboard.press_and_release('esc')
    time.sleep(0.25)
    keyboard.press_and_release('esc')
    time.sleep(0.25)
    keyboard.press_and_release('esc')
    time.sleep(0.7)
    # Volunteer before closing
    pyautogui.click(volunteer[0], volunteer[1])
    time.sleep(0.25)
    pyautogui.click(volunteer[0], volunteer[1])

    # Close the game through icon
    keyboard.press_and_release('win')
    time.sleep(4)
    pyautogui.rightClick(180, 2123)
    time.sleep(1)
    pyautogui.click(141, 2040)

    # pyautogui.hotkey('alt', 'f4')
    # time.sleep(0.5)  # Short delay to ensure the first press is registered
    # pyautogui.hotkey('alt', 'f4')
    # time.sleep(3)  # Wait for the game to close

    # Click on the game icon to start the game
    time.sleep(2)
    pyautogui.click(game_icon_coords[0], game_icon_coords[1])
    time.sleep(10)  # Wait for the game to load.

    # Click on the login button
    pyautogui.click(login_button_coords[0], login_button_coords[1])
    time.sleep(.5)
    pyautogui.click(login_button_coords[0], login_button_coords[1])
    time.sleep(14)  # Wait for login to process and auto start game

    # Double-click on the character to start playing
    pyautogui.doubleClick(character_coords[0], character_coords[1])
    time.sleep(22)  # Wait for the game to enter into playing mode

def press_and_hold(key, hold_time=0.1):
    keyboard.press(key)
    time.sleep(hold_time)
    keyboard.release(key)

def drag_window(start_coords, end_coords):
    pyautogui.moveTo(start_coords[0], start_coords[1])
    pyautogui.mouseDown()
    time.sleep(0.5)  # Short delay to ensure the drag is registered
    pyautogui.moveTo(end_coords[0], end_coords[1], duration=1)
    pyautogui.mouseUp()

def does_it_match(image_path, similarity_threshold=0.7):
    screen = capture_game_screen()
    template_color = cv2.imread(image_path)  # Read the image in color
    template = cv2.cvtColor(template_color, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    # Perform template matching
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    # Check if the maximum match value is greater than the similarity threshold
    return max_val >= similarity_threshold   

def handle_direction(direction):
    if direction == 'top':
        press_and_hold('3', hold_time=4.5)

    elif direction == 'right':
        press_and_hold('w', hold_time=1)
        press_and_hold('k', hold_time=.78)   

        press_and_hold('3', hold_time=4.5)

    elif direction == 'left':
        press_and_hold('w', hold_time=1)
        press_and_hold('l', hold_time=.75)

        press_and_hold('3', hold_time=4.5) 
        press_and_hold('q', hold_time=.15)

    elif direction == 'bot':
        press_and_hold('w', hold_time=1.1)
        press_and_hold('o')

        press_and_hold('3', hold_time=4.5)

def reset_position():
    # Make sure Inventory is Open
    inventory_close = (2289, 110)
    pyautogui.click(inventory_close[0], inventory_close[1])
    time.sleep(1)
    keyboard.press_and_release('ctrl+z')
    time.sleep(1)
  
    pyautogui.doubleClick(dragon_fall[0], dragon_fall[1])
    time.sleep(25)

    keyboard.press_and_release('ctrl+z')
    time.sleep(1)
    pyautogui.doubleClick(mistlock[0], mistlock[1])
    time.sleep(20)

def walk_and_center_npc():
    # Reset Position by clicking Mistlock pass
    reset_position() 

    # Paths to images for each direction
    direction_images = [
        './center_character/Top-1.png',
        './center_character/Right-1.png',
        './center_character/Left-1.png',
        './center_character/Bot-1.png'
    ]

    # Descriptions for each direction (for logging purposes)
    directions = ['top', 'right', 'left', 'bot']

    # Continue trying until a match is found
    while True:
        for idx, image_path in enumerate(direction_images):
            if does_it_match(image_path, 0.65):
                # Execute direction-specific actions
                handle_direction(directions[idx])
                return  # Exit after successful handling
            else:
                print(f"No match facing {directions[idx]}.")

        # If no matches found after trying all directions, reset and try again
        print("No directions matched, resetting...")
              
        restart_game()
        reset_position()
            

# def does_it_match_menus(image_paths, similarity_threshold=0.7):
#     screen = capture_game_screen()  # Capture a screenshot of the current game screen
#     matches_found = 0  # Counter for the number of matches found

#     for image_path in image_paths:
#         template_color = cv2.imread(image_path)  # Read the image in color
#         template = cv2.cvtColor(template_color, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

#         # Perform template matching
#         result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
#         _, max_val, _, _ = cv2.minMaxLoc(result)

#         # Check if the maximum match value is greater than the similarity threshold
#         if max_val >= similarity_threshold:
#             matches_found += 1

#     # Return True only if all provided images are matched successfully
#     return matches_found == len(image_paths)   

def open_menus():
    # menus_confirm = ['./center_character/correct_inventory.png', './center_character/correct_tpbank.png']

    # Ensure the game window is active by clicking into the game area
    pyautogui.click(1800, 1050)

    # Close Inventory in case is open
    pyautogui.click(2288, 109)
    time.sleep(.5)

    keyboard.press_and_release('ctrl+z')
    time.sleep(1)

    # Open Trading Post with Tab (assuming the NPC is in front)
    keyboard.press_and_release('tab')
    time.sleep(1)

    # Walk slightly to the right to the bank NPC and open it
    press_and_hold('e', hold_time=1)  # Adjust hold_time as needed for walking duration
    keyboard.press_and_release('tab')
    time.sleep(1)

    # Walk back to the initial place
    press_and_hold('q', hold_time=1)  # Match the hold time with 'e' to walk back

    # Drag Bank tab to a specific coordinate
    start_coords = (1960, 544)
    end_coords = (3141, 1086)
    drag_window(start_coords, end_coords)

    # Open map for a white background using Shift + Z
    keyboard.press_and_release('shift+z')
    time.sleep(1)

    # Scroll completely for better image recognition
    pyautogui.moveTo(2622, 1640)        
    
    pyautogui.scroll(-500)  
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)   
    time.sleep(0.25)

    pyautogui.scroll(-500)  
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    time.sleep(0.25) 

    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    time.sleep(0.25)

    pyautogui.scroll(-500)  
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)   
    time.sleep(0.25)

    pyautogui.scroll(-500)  
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    time.sleep(0.25) 

    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    time.sleep(0.25)

    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    time.sleep(0.25)

    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    pyautogui.scroll(-500)
    time.sleep(0.25)

    # Check if the menus are set up correctly
    while not does_it_match('./center_character/correct_tpbank.png', 0.8):
        print("Menus are not correctly set up, re-centering NPC...")
        restart_game()
        walk_and_center_npc()
        open_menus()
    print("Menus are correctly set up.")

def sell_most_expensive_exotics(iterations): 
    # Close last sell
    pyautogui.click(3517, 186)
    time.sleep(1.5)

    # Sell items section
    pyautogui.click(3450, 125)
    time.sleep(1.5)

    # Sort by Price
    price = (3714, 236)
    pyautogui.click(price[0], price[1])
    time.sleep(.5)
    pyautogui.click(price[0], price[1])
    time.sleep(1.5)

    # Sell Exotics
    for _ in range(iterations):
        pyautogui.click(2871, 304)
        time.sleep(2)
        # Sell
        pyautogui.click(3007, 555)
        pyautogui.click(3007, 595)
        time.sleep(7)
        # Close last sell
        pyautogui.click(3517, 186)
        time.sleep(1.5)


def salvage_restant_exotics():    
    # Compact Inventory
    pyautogui.click(compact[0], compact[1])
    time.sleep(0.25)

    accept_button = (1896, 1156)    

    # Setup Silver Fed
    pyautogui.moveTo(silver_fed[0], silver_fed[1])
    pyautogui.rightClick()
    time.sleep(0.25)
    pyautogui.click(silver_fed_use[0], silver_fed_use[1]) 
    time.sleep(0.5)

    # Consume All Luck from multiple locations
    salvage_exotics_coords_list = [
        (126, 385),  
        (216, 385),  
        (305, 385),
        (391, 385),
        (482, 385),
        (569, 385),
        (657, 385),
        (746, 385),
        (837, 385),
        (918, 385),

        (1011, 385),
        (1100, 385),
        (1188, 385),
        (1279, 385),
        (1368, 385),
        (1451, 385),
        (1542, 385),
        (1631, 385),
        (1720, 385),
        (1806, 385),

        (1896, 385),
        (1982, 385),
        (2073, 385),
        (2155, 385),
        (2248, 385)
        
    ]

    for coords in salvage_exotics_coords_list:
        pyautogui.moveTo(coords[0], coords[1])
        pyautogui.click()
        time.sleep(0.25)
        pyautogui.click(accept_button[0], accept_button[1]) # Accept salvage
        time.sleep(0.25)

def take_all_and_storage(storage_number = 1):    
    for _ in range(storage_number):
        # Close last sell
        pyautogui.click(3517, 186)
        time.sleep(1.5)

        # Take all
        pyautogui.click(2619, 1025) 
        time.sleep(1)

        # Make Sure is Scrolled Down by clicking
        pyautogui.click(2817, 1991)
        time.sleep(3)
        pyautogui.click(2817, 1991)  
        time.sleep(1)

        # Scroll Up by Clicking
        pyautogui.click(2816, 1725)
        time.sleep(3)
        pyautogui.click(2816, 1725)

        # Greens Coords
        greens_coords_list = [
            (2491, 1340),  
            (2575, 1340),  
            (2669, 1340),
            (2756, 1340),

            (2491, 1430),
            (2575, 1430),
            (2669, 1430),
            (2756, 1430),

            (2491, 1520),  
            (2575, 1520),  
            (2669, 1520),
            (2756, 1520),

            (2491, 1610),  
            (2575, 1610),  
            (2669, 1610),
            (2756, 1610),

            (2491, 1700),  
            (2575, 1700),  
            (2669, 1700),
            (2756, 1700),

            (2491, 1790),  
            (2575, 1790),  
            (2669, 1790),
            (2756, 1790),

            (2491, 1880),  
            (2575, 1880),  
            (2669, 1880),
            (2756, 1880),

            (2491, 1970),  
            (2575, 1970),  
            (2669, 1970),
            (2756, 1970),
        ]

        for coords in greens_coords_list:
            pyautogui.moveTo(coords[0], coords[1])
            pyautogui.doubleClick()
            time.sleep(0.25)

        # Scroll Down by Clicking
        pyautogui.click(2817, 1991)
        time.sleep(3)
        pyautogui.click(2817, 1991)  

def place_10_orders():
    # Close last sell
    pyautogui.click(3517, 186)
    time.sleep(2.5)

    # Click Home
    pyautogui.click(2948, 136)
    time.sleep(2)
  
    # Click search
    pyautogui.click(2498, 242)
    time.sleep(0.5)

    # Type piece of unidentified gear
    pyautogui.write('piece of unidentified gear', interval=0.1)
    time.sleep(2)

    # Click gear
    pyautogui.click(2873, 356)
    time.sleep(5)

    # Click on order
    pyautogui.click(2733, 746)
    time.sleep(3)

    # 250
    pyautogui.click(3284, 356)
    time.sleep(1)
    
    # Place order
    for _ in range(10):
        pyautogui.click(3007, 555)
        time.sleep(1.5)
        pyautogui.click(3007, 555)  
        time.sleep(5)

def buy_10_orders():
    # Close last sell
    pyautogui.click(3517, 186)
    time.sleep(2.5)

    # Click Home
    pyautogui.click(2948, 136)
    time.sleep(2)
  
    # Click search
    pyautogui.click(2498, 242)
    time.sleep(0.5)

    # Type piece of unidentified gear
    pyautogui.write('piece of unidentified gear', interval=0.1)
    time.sleep(2)

    # Click gear
    pyautogui.click(2873, 356)
    time.sleep(5)

    # 250
    pyautogui.click(3284, 356)
    time.sleep(1)
    
    # Place order
    for _ in range(10):
        pyautogui.click(3007, 555)
        time.sleep(1.5)
        pyautogui.click(3007, 555)  
        time.sleep(5)
            
def manage_charms(): 
    # List of image paths for different charms
    charm_images = [
        './items-to-sell/little_charms_of_skill.png',
        './items-to-sell/little_symbols_of_control.png', 
        './items-to-sell/little_charms_of_potence.png',
        './items-to-sell/little_charms_of_briliance.png',
        './items-to-sell/little_symbols_of_pain.png',
        './items-to-sell/little_symbols_of_enhancement.png'
    ]

    for image_path in charm_images:
        loc, w, h = search_for_item(image_path, 0.91)
        if loc is not None:
            for pt in zip(*loc[::-1]):
                center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template
                
                # Check if the center of the found item is within the defined area
                if sell_search_area[0] <= center_x <= sell_search_area[0] + sell_search_area[2] and sell_search_area[1] <= center_y <= sell_search_area[1] + sell_search_area[3]:
                    pyautogui.rightClick(center_x, center_y)  # Click on the identified charm
                    time.sleep(0.5)
                    pyautogui.move(16, 88)  # Move to "Sell" option
                    pyautogui.click()
                    time.sleep(4) 

                    # pyautogui.click(sellers_list[0], sellers_list[1])  # Add to sell list
                    # time.sleep(0.25)
                    pyautogui.click(maximum_amount[0], maximum_amount[1])  # Set Maximum Amount
                    time.sleep(0.25)
                    # pyautogui.click(minus_one_copper[0], minus_one_copper[1])  # Minus One Copper
                    # time.sleep(0.25)
                    pyautogui.click(list_item[0], list_item[1])  # List the item for sale
                    time.sleep(5)  # Wait for the transaction to process
                    break  # Break after processing the first valid charm

            time.sleep(1)  # Sleep between processing different charms to manage screen updates and avoid rapid-fire actions

def click_game():
    pyautogui.click(78, 700)
    time.sleep(0.5)

def main():
    # click_game()
    manage_charms()
    # sell_all_items()
    # salvage_restant_exotics()
    # take_all_and_storage(2)

    # walk_and_center_npc()
    # open_menus()

    # consume_purple_luck()
    # consume_purple_luck_click_button()
    # handle_errors()

    # manage_ectos() 
    # consume_purple_luck()  
    # consume_purple_luck_click_button()
    # handle_errors()

    # consume_luck()
    # handle_errors()

    # delete_dark_matter()
    # manage_cristallyne_dust()
    # handle_errors()

    # buy_10_orders()

    for i in range(1, 31):  
        print(f"Starting iteration {i}")

        handle_errors()
        manage_unidentified_gear()
        time.sleep(11)
        use_salvage_kits()
        sell_lucent_motes()

        manage_cristallyne_dust()

        if i % 2 == 0: 
            consume_purple_luck()
            consume_purple_luck_click_button()
            handle_errors()
            # consume_purple_luck()
            # consume_purple_luck_click_button() #? Here add normal corrdinates instead
            # handle_errors()

            consume_luck()

            sell_mithril_ore() 
            handle_errors() 

            sell_elder_wood_logs() 

        if i % 3 == 0:  
            sell_silk_scraps() 
            sell_thick_leather_sections() 

        if i % 10 == 0:  
            manage_ectos() 
            consume_purple_luck()  
            consume_purple_luck_click_button()
            handle_errors()

            consume_luck()
            handle_errors()

            delete_dark_matter()
            manage_cristallyne_dust()
            handle_errors()

            manage_charms()
            manage_charms()
            manage_charms()
            manage_charms()
            sell_all_items()
            handle_errors()

            # place_10_orders()
            # buy_10_orders()

        if i % 24 == 0:
            consume_purple_luck()  
            consume_purple_luck_click_button()
            handle_errors()

            consume_luck()
            handle_errors()

            take_all_and_storage(1)
        
        if i % 30 == 0:  
            sell_most_expensive_exotics(5)
            salvage_restant_exotics()

            restart_game()
            walk_and_center_npc()
            open_menus()
        
        # Add a short sleep time if needed between iterations to avoid overwhelming the application
        time.sleep(2)

if __name__ == "__main__":
    main()
