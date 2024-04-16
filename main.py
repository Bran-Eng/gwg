import cv2
import numpy as np
import pyautogui
import time
import keyboard

# Disable the fail-safe
pyautogui.FAILSAFE = False

# Areas Coordinates
inventory_area = (0, 0, 2350, 2160)
bank_area = (2840, 1125, 3840, 2160)
tp_area = (2430, 60, 3840, 1090)
tp_price_area = () # Rectangle of silver and gold price area

compact = (2229, 176)
take_all = (2615, 1025)

rune_crafter = (481, 287)
rune_crafter_salvage_green = (503, 378) 
rune_crafter_confirm_button = (1811, 1415)

silver_fed = (566, 285)
silver_fed_salvage_rare = (588, 417) 
silver_fed_confirm_button = (1811, 1247)
silver_fed_confirm_button_2 = (1811, 1219)
silver_fed_confirm_button_3 = (1811, 1286)
silver_fed_confirm_button_4 = (1811, 1327)
silver_fed_salvage_stack = (587, 453)
silver_fed_salvage_stack_accept = (1900, 1155) 

# Trading Post Sell Areas
sellers_list = (3163, 746)
maximum_amount = (3280, 358)
list_item = (3002, 556)


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
        pyautogui.moveTo(3280, 1800)        
        for _ in range(5):
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

            find_and_click(step=2)                                
                    
            return False        
        
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
    time.sleep(0.25)
    pyautogui.click(rune_crafter_salvage_green[0], rune_crafter_salvage_green[1])
    time.sleep(0.5)
    pyautogui.click(rune_crafter_confirm_button[0], rune_crafter_confirm_button[1])
    pyautogui.moveTo(1200, 170)
    time.sleep(25.5)

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
    pyautogui.moveTo(silver_fed[0], silver_fed[1])
    pyautogui.rightClick()
    time.sleep(0.25)
    pyautogui.click(silver_fed_salvage_stack[0], silver_fed_salvage_stack[1]) 
    time.sleep(0.5)

    # Identify ectos by image to salvage
    image_path = './items-to-sell/globs_of_ectoplasm.png'  
    loc, w, h = search_for_item(image_path, 0.7)
    if loc is not None:
        for pt in zip(*loc[::-1]):
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
            pyautogui.click(list_item[0], list_item[1]) # List
            time.sleep(5) #! Time after sell
            break 
        
def consume_purple_luck():
    # Identify purple_luck
    image_path = './items-to-sell/purple_luck.png'  
    loc, w, h = search_for_item(image_path, 0.9)
    if loc is not None:
        for pt in zip(*loc[::-1]):
            pyautogui.click(pt[0] + w/2, pt[1] + h/2)  # Click on the identified purple luck
            pyautogui.rightClick()   
            break         
        
def consume_purple_luck_click_button():
    image_path = './items-to-sell/consume_all.png'  
    loc, w, h = search_for_item(image_path, 0.95)
    if loc is not None:
        for pt in zip(*loc[::-1]):
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
        time.sleep(5) #! Time after sell

def delete_dark_matter():
    # Identify dark matter
    image_path = './items-to-sell/globs_of_dark_matter.png'  
    loc, w, h = search_for_item(image_path, 0.7)
    if loc is not None:
        for pt in zip(*loc[::-1]):
            pyautogui.click(pt[0] + w/2, pt[1] + h/2)  # Click on the identified dark matter
            pyautogui.rightClick()
            time.sleep(0.25)
            pyautogui.move(16, 87) #! Destroy dark matter
            pyautogui.click()
            time.sleep(0.25)
            pyautogui.click(1939, 1153) # Accept
            time.sleep(0.25) 
            break    

def sell_lucent_motes():
    # Identify lucent motes by image to sell
    image_path = './items-to-sell/lucent_motes.png'
    loc, w, h = search_for_item(image_path, 0.8)
    if loc is not None:
        for pt in zip(*loc[::-1]):
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
            time.sleep(5) #! Time after sell
            break


def sell_mithril_ore():
    # Identify mithril ore by image to sell
    image_path = './items-to-sell/mithril_ore.png'
    loc, w, h = search_for_item(image_path, 0.85)
    if loc is not None:
        for pt in zip(*loc[::-1]):
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
            time.sleep(5) #! Time after sell
            break

def sell_elder_wood_logs():
    # Identify elder wood logs by image to sell
    image_path = './items-to-sell/elder_wood_logs.png'
    loc, w, h = search_for_item(image_path, 0.7)
    if loc is not None:
        for pt in zip(*loc[::-1]):
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
            time.sleep(5) #! Time after sell
            break

def sell_thick_leather_sections():
    # Identify thick leather sections by image to sell
    image_path = './items-to-sell/thick_leather_sections.png'
    loc, w, h = search_for_item(image_path, 0.7)
    if loc is not None:
        for pt in zip(*loc[::-1]):
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
            time.sleep(5) #! Time after sell
            break

def sell_silk_scraps():
    # Identify silk scraps by image to sell
    image_path = './items-to-sell/silk_scraps.png'
    loc, w, h = search_for_item(image_path, 0.7)
    if loc is not None:
        for pt in zip(*loc[::-1]):
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
            time.sleep(5) #! Time after sell
            break
        
def handle_errors():
    # Press cancel buttons
    err_buttons_coords_list = [
        (2119, 1156),  
        (2129, 1181),
        (2118, 1154)
    ]

    for coords in err_buttons_coords_list:
        time.sleep(0.25)
        pyautogui.click(coords[0], coords[1])

def restart_game():
    pyautogui.click(1800, 500)

     # Coordinates for game icon, login, start game, and character selection
    game_icon_coords = (180, 2122)
    login_button_coords = (1203, 1327)
    character_coords = (1600, 2015)
    volunteer = (78, 1176)

    # Close windows to volunteer
    pyautogui.hotkey('esc')
    time.sleep(0.25)
    pyautogui.hotkey('esc')
    time.sleep(0.25)
    pyautogui.hotkey('esc')
    time.sleep(0.25)
    pyautogui.hotkey('esc')
    time.sleep(0.25)

    pyautogui.click(volunteer[0], volunteer[1])

    pyautogui.hotkey('alt', 'f4')
    time.sleep(0.5)  # Short delay to ensure the first press is registered
    pyautogui.hotkey('alt', 'f4')
    time.sleep(3)  # Wait for the game to close

   

    # Click on the game icon to start the game
    pyautogui.click(game_icon_coords[0], game_icon_coords[1])
    time.sleep(10)  # Wait for the game to load.

    # Click on the login button
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

def open_menus():
    # Ensure the game window is active by clicking into the game area
    pyautogui.click(1800, 1050)

    mistlock = (126, 281)

    # Restart Position
    pyautogui.click(mistlock[0], mistlock[1])
    time.sleep(15)
    keyboard.press_and_release('ctrl+z')
    pyautogui.click(mistlock[0], mistlock[1])
    time.sleep(15)

    # Walk to NPC's
    press_and_hold('3', hold_time=4)

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


def salvage_restant_exotics():    
    pyautogui.click(1800, 1050)
    # Compact Inventory
    pyautogui.click(compact[0], compact[1])
    time.sleep(0.25)

    silver_fed_use = (587, 304)
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
        (2248, 385),

    ]

    for coords in salvage_exotics_coords_list:
        pyautogui.moveTo(coords[0], coords[1])
        pyautogui.click()
        time.sleep(0.25)
        pyautogui.click(accept_button[0], accept_button[1]) # Accept salvage
        time.sleep(0.25)

def main():
    open_menus()
    # delete_dark_matter()
    # salvage_restant_exotics()
    sell_all_items()

    for i in range(1, 93):  
        print(f"Starting iteration {i}")
        
        #? Test
        # open_menus()

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

            consume_luck()
            handle_errors()

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

            sell_all_items()
            handle_errors()
        
        if i % 30 == 0:  
            restart_game()
            open_menus()
        
        # Add a short sleep time if needed between iterations to avoid overwhelming the application
        time.sleep(2)

if __name__ == "__main__":
    main()
