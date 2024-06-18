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
# sell_search_area = (76, 1219, 2829, 2075)
sell_search_area = (0, 0, 2350, 2160)
item_tp_area = (2758, 202, 2842, 284)

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

silver_fed = (1017, 1540)
silver_fed_use = (1040, 1558)
silver_fed_salvage_rare = (1040, 1670) 
silver_fed_salvage_stack = (1040, 1706)

silver_fed_confirm_button = (1811, 1247)
silver_fed_confirm_button_1 = (1811, 1219) # Row 1
silver_fed_confirm_button_2 = (1811, 1286) # Row 2
silver_fed_confirm_button_3 = (1811, 1327) # Row 3
silver_fed_confirm_button_4 = (1811, 1326) # Row 4
silver_fed_confirm_button_5 = (1811, 1363) # Row 5
silver_fed_confirm_button_6 = (1811, 1400) # Row 6

silver_fed_salvage_stack_accept = (1900, 1155) 

copper_fed = (132, 1540)
copper_fed_salvage_common = (150, 1593) 

# Trading Post Sell Areas
sellers_list = (3163, 746)
maximum_amount = (3280, 358)
minus_one = (2986, 362)
minus_one_copper = (3240, 423)
plus_one_copper = (3240, 406)
list_item = (3002, 556)

mistlock = (744, 1535)
portal_scroll = (837, 1535)

volunteer = (78, 1176)

# Paths to images for each direction
direction_images = [
    './center_character/Top-1.png',
    './center_character/Right-1.png',
    './center_character/Left-1.png',
    './center_character/Bot-1.png'
]

# Descriptions for each direction (for logging purposes)
directions = ['top', 'right', 'left', 'bot']


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
    time.sleep(0.45)
    pyautogui.move(85, 205)  # Move to "Use All"
    pyautogui.click()    

def find_and_click(step=0):
    image_path = './items-to-sell/green.png'
    threshold=0.70
    
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

                # If after 10 attempts it fails, return False

                elif step == 4:
                    # Scroll Up
                    pyautogui.moveTo(3280, 1800) # Move to a position to initiate scroll
                    for _ in range(10):
                        pyautogui.scroll(500)
                    time.sleep(0.25)
                    
                    # Attempt to execute step 2
                    if find_and_click(step=2):
                        return True

                    # If after 10 attempts it fails, return False

def manage_unidentified_gear():
    # Attempt to find Unidentified Gear Masterwork in the inventory and use all.
    if not find_and_click(step=1):
        if not find_and_click(step=2):
            if not find_and_click(step=3):
                pass    
            
def manage_rare_gear():    
    if not find_and_click_rare(step=1):
        if not find_and_click_rare(step=2):
            pass
        
def manage_common_gear():    
    if not find_and_click_common(step=1):
        if not find_and_click_common(step=2):
            if not find_and_click_common(step=3):
                pass
        
def find_and_click_common(step=0):
    image_path = './items-to-sell/blue.png'
    threshold=0.8
    
    if step == 1 or step == 2:
        loc, w, h = search_for_item(image_path, threshold)
        if loc is not None:
            for pt in zip(*loc[::-1]):
                center_x, center_y = pt[0] + w/2, pt[1] + h/2
                
                if step == 1 and  inventory_area[0] <= center_x <= inventory_area[0] + inventory_area[2] and inventory_area[1] <= center_y <= inventory_area[1] + inventory_area[3]:
                    use_all_common_gear(center_x, center_y)
                    return True
                
                elif step == 2 and bank_area[0] <= center_x <= bank_area[0] + bank_area[2] and bank_area[1] <= center_y <= bank_area[1] + bank_area[3]:
                    pyautogui.moveTo(center_x, center_y)
                    pyautogui.doubleClick()
                    time.sleep(0.25)
                    find_and_click_common(step=1)
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

    elif step == 4:
        # Scroll Up
        pyautogui.moveTo(3280, 1800) # Move to a position to initiate scroll
        for _ in range(10):
            pyautogui.scroll(500)
        time.sleep(0.25)
        
        # Attempt to execute step 2
        if find_and_click(step=2):
            return True

        # return False  # If after 10 attempts it fails, return False
                
def use_all_common_gear(center_x, center_y):    
    pyautogui.moveTo(center_x, center_y)
    pyautogui.rightClick()
    time.sleep(0.25)
    pyautogui.move(85, 205)  # Move to "Use All"
    pyautogui.click()    

    time.sleep(10)
    use_copperfed()

def use_copperfed():
    #? Use Copper Fed
    pyautogui.moveTo(copper_fed[0], copper_fed[1])
    pyautogui.rightClick() 
    time.sleep(0.5)
    pyautogui.click(copper_fed_salvage_common[0], copper_fed_salvage_common[1])
    time.sleep(0.5)

    handle_errors()
    time.sleep(0.5)

    pyautogui.moveTo(copper_fed[0], copper_fed[1])
    pyautogui.rightClick() 
    time.sleep(0.5)
    pyautogui.click(copper_fed_salvage_common[0], copper_fed_salvage_common[1])
    time.sleep(0.5)

    # Press confirm button using coordinates for tackling possible placements
    pyautogui.click(rune_crafter_confirm_button[0], rune_crafter_confirm_button[1])
    pyautogui.click(rune_crafter_confirm_button_1[0], rune_crafter_confirm_button_1[1])
    pyautogui.click(rune_crafter_confirm_button_2[0], rune_crafter_confirm_button_2[1])
    pyautogui.click(rune_crafter_confirm_button_3[0], rune_crafter_confirm_button_3[1])
    pyautogui.click(rune_crafter_confirm_button_4[0], rune_crafter_confirm_button_4[1])
    pyautogui.click(rune_crafter_confirm_button_5[0], rune_crafter_confirm_button_5[1])
    pyautogui.click(rune_crafter_confirm_button_6[0], rune_crafter_confirm_button_6[1])
    time.sleep(15)

    #? Use Runecrafter for salvaging greens
    pyautogui.moveTo(rune_crafter[0], rune_crafter[1])
    pyautogui.rightClick() 
    time.sleep(0.5)
    pyautogui.click(rune_crafter_salvage_green[0], rune_crafter_salvage_green[1])
    time.sleep(0.5)

    handle_errors()
    time.sleep(0.5)

    pyautogui.moveTo(rune_crafter[0], rune_crafter[1])
    pyautogui.rightClick() 
    time.sleep(0.5)
    pyautogui.click(rune_crafter_salvage_green[0], rune_crafter_salvage_green[1])
    time.sleep(0.5)

    # Press confirm button using coordinates for tackling possible placements
    pyautogui.click(rune_crafter_confirm_button[0], rune_crafter_confirm_button[1])
    pyautogui.click(rune_crafter_confirm_button_1[0], rune_crafter_confirm_button_1[1])
    pyautogui.click(rune_crafter_confirm_button_2[0], rune_crafter_confirm_button_2[1])
    pyautogui.click(rune_crafter_confirm_button_3[0], rune_crafter_confirm_button_3[1])
    pyautogui.click(rune_crafter_confirm_button_4[0], rune_crafter_confirm_button_4[1])
    pyautogui.click(rune_crafter_confirm_button_5[0], rune_crafter_confirm_button_5[1])
    pyautogui.click(rune_crafter_confirm_button_6[0], rune_crafter_confirm_button_6[1])
    time.sleep(8)

    #? Use Silver Fed for salvaging rares
    pyautogui.moveTo(silver_fed[0], silver_fed[1])
    pyautogui.rightClick()
    time.sleep(0.5)
    pyautogui.click(silver_fed_salvage_rare[0], silver_fed_salvage_rare[1])
    time.sleep(0.5)

    handle_errors()
    time.sleep(0.5)

    pyautogui.moveTo(silver_fed[0], silver_fed[1])
    pyautogui.rightClick()
    time.sleep(0.5)
    pyautogui.click(silver_fed_salvage_rare[0], silver_fed_salvage_rare[1])
    time.sleep(0.5)

    # Press confirm button using coordinates for tackling possible placements
    pyautogui.click(silver_fed_confirm_button[0], silver_fed_confirm_button[1])
    pyautogui.click(silver_fed_confirm_button_1[0], silver_fed_confirm_button_1[1])
    pyautogui.click(silver_fed_confirm_button_2[0], silver_fed_confirm_button_2[1])
    pyautogui.click(silver_fed_confirm_button_3[0], silver_fed_confirm_button_3[1])
    pyautogui.click(silver_fed_confirm_button_4[0], silver_fed_confirm_button_4[1])
    pyautogui.moveTo(1200, 170)
    time.sleep(1.5) 

    pyautogui.click(compact[0], compact[1])

def find_and_click_rare(step=0):
    image_path = './items-to-sell/yellow.png'
    threshold=0.8
    
    if step == 1 or step == 2:
        loc, w, h = search_for_item(image_path, threshold)
        if loc is not None:
            for pt in zip(*loc[::-1]):
                center_x, center_y = pt[0] + w/2, pt[1] + h/2
                
                if step == 1 and  inventory_area[0] <= center_x <= inventory_area[0] + inventory_area[2] and inventory_area[1] <= center_y <= inventory_area[1] + inventory_area[3]:
                    use_all_rare_gear(center_x, center_y)
                    return True
                
                elif step == 2 and bank_area[0] <= center_x <= bank_area[0] + bank_area[2] and bank_area[1] <= center_y <= bank_area[1] + bank_area[3]:
                    pyautogui.moveTo(center_x, center_y)
                    pyautogui.doubleClick()
                    time.sleep(0.25)
                    find_and_click_rare(step=1)
                    return True     

def use_all_rare_gear(center_x, center_y):    
    pyautogui.moveTo(center_x, center_y)
    pyautogui.rightClick()
    time.sleep(0.25)
    pyautogui.move(85, 205)  # Move to "Use All"
    pyautogui.click()    

    time.sleep(10)
    use_silverfed()  

def use_silverfed():
    # Identify Silver Fed
    loc, w, h = search_for_item('./items-to-sell/silver.png', 0.7)

    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template
            
            # Check if the center of the found item is within the defined area
            if inventory_area[0] <= center_x <= inventory_area[0] + inventory_area[2] and inventory_area[1] <= center_y <= inventory_area[1] + inventory_area[3]:
                pyautogui.moveTo(pt[0] + w/2, pt[1] + h/2)  # Click on Silver Fed
                pyautogui.rightClick()
                time.sleep(0.5)
                pyautogui.move(20, 125) #! Move cursor to "Salvage" option
                pyautogui.click()
                time.sleep(.5) 
                
                handle_errors()
                time.sleep(0.5)
                
                pyautogui.moveTo(pt[0] + w/2, pt[1] + h/2)  # Click on Silver Fed
                pyautogui.rightClick()
                time.sleep(0.5)
                pyautogui.move(20, 125) #! Move cursor to "Salvage" option
                pyautogui.click()
                time.sleep(.5) 
                
                # Press confirm button using 3 coordinates for tackling possible placements
                pyautogui.click(silver_fed_confirm_button[0], silver_fed_confirm_button[1])
                pyautogui.click(silver_fed_confirm_button_4[0], silver_fed_confirm_button_1[1])
                pyautogui.click(silver_fed_confirm_button_2[0], silver_fed_confirm_button_2[1])
                pyautogui.click(silver_fed_confirm_button_3[0], silver_fed_confirm_button_3[1])
                pyautogui.click(silver_fed_confirm_button_4[0], silver_fed_confirm_button_4[1])
                pyautogui.click(silver_fed_confirm_button_4[0], silver_fed_confirm_button_5[1])
                pyautogui.click(silver_fed_confirm_button_4[0], silver_fed_confirm_button_6[1])
                
                time.sleep(26)
                pyautogui.moveTo(1200, 170)
                time.sleep(1.5)    
                pyautogui.click(compact[0], compact[1])

                break 
    
    sell_ectos()
    sell_ectos()
    
    sell_item('./items-to-sell/lucent_motes.png')
    sell_item('./items-to-sell/lucent_motes.png')
    handle_errors() 

    sell_item('./items-to-sell/mithril_ore.png')
    sell_item('./items-to-sell/mithril_ore.png')
    handle_errors()

    sell_item('./items-to-sell/elder_wood_logs.png')
    sell_item('./items-to-sell/elder_wood_logs.png')
    handle_errors()

    sell_item('./items-to-sell/silk_scraps.png')
    sell_item('./items-to-sell/silk_scraps.png')
    handle_errors()

    sell_item('./items-to-sell/thick_leather_sections.png')
    sell_item('./items-to-sell/thick_leather_sections.png')
    handle_errors()

    manage_charms()
    manage_charms()
    handle_errors()

    sell_most_expensive_exotics(3)
    salvage_restant_exotics_few()
    manage_cristallyne_dust()
    delete_dark_matter()
    handle_errors()
            
def use_salvage_kits():
    #? Use Runecrafter for salvaging greens
    loc, w, h = search_for_item('./items-to-sell/rune_crafter.png', 0.7)

    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template
            
            # Check if the center of the found item is within the defined area
            if inventory_area[0] <= center_x <= inventory_area[0] + inventory_area[2] and inventory_area[1] <= center_y <= inventory_area[1] + inventory_area[3]:
                pyautogui.moveTo(pt[0] + w/2, pt[1] + h/2)  # Click on Rune Crafter
                pyautogui.rightClick()
                time.sleep(0.5)
                pyautogui.move(20, 90) # Move cursor to "Salvage" option
                pyautogui.click()
                time.sleep(.5) 
                
                handle_errors()
                time.sleep(0.5)
                
                pyautogui.moveTo(pt[0] + w/2, pt[1] + h/2)  # Click on Rune Crafter
                pyautogui.rightClick()
                time.sleep(0.5)
                pyautogui.move(20, 90) # Move cursor to "Salvage" option
                pyautogui.click()
                time.sleep(.5) 
    
                # Press confirm button using coordinates for tackling possible placements
                pyautogui.click(rune_crafter_confirm_button[0], rune_crafter_confirm_button[1])
                pyautogui.click(rune_crafter_confirm_button_1[0], rune_crafter_confirm_button_1[1])
                pyautogui.click(rune_crafter_confirm_button_2[0], rune_crafter_confirm_button_2[1])
                pyautogui.click(rune_crafter_confirm_button_3[0], rune_crafter_confirm_button_3[1])
                pyautogui.click(rune_crafter_confirm_button_4[0], rune_crafter_confirm_button_4[1])
                pyautogui.click(rune_crafter_confirm_button_5[0], rune_crafter_confirm_button_5[1])
                pyautogui.click(rune_crafter_confirm_button_6[0], rune_crafter_confirm_button_6[1])
                time.sleep(20)
                
                break

    #? Use Silver Fed for salvaging rares
    loc, w, h = search_for_item('./items-to-sell/silver.png', 0.7)

    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template
            
            # Check if the center of the found item is within the defined area
            if inventory_area[0] <= center_x <= inventory_area[0] + inventory_area[2] and inventory_area[1] <= center_y <= inventory_area[1] + inventory_area[3]:
                pyautogui.moveTo(pt[0] + w/2, pt[1] + h/2)  # Click on Silver Fed
                pyautogui.rightClick()
                time.sleep(0.5)
                pyautogui.move(20, 125) # Move cursor to "Salvage" option
                pyautogui.click()
                time.sleep(.5) 
                
                handle_errors()
                time.sleep(0.5)
                
                pyautogui.moveTo(pt[0] + w/2, pt[1] + h/2)  # Click on Silver Fed
                pyautogui.rightClick()
                time.sleep(0.5)
                pyautogui.move(20, 125) #1s Move cursor to "Salvage" option
                pyautogui.click()
                time.sleep(.5) 
                
                # Press confirm button using 3 coordinates for tackling possible placements
                pyautogui.click(silver_fed_confirm_button[0], silver_fed_confirm_button[1])
                pyautogui.click(silver_fed_confirm_button_4[0], silver_fed_confirm_button_1[1])
                pyautogui.click(silver_fed_confirm_button_2[0], silver_fed_confirm_button_2[1])
                pyautogui.click(silver_fed_confirm_button_3[0], silver_fed_confirm_button_3[1])
                pyautogui.click(silver_fed_confirm_button_4[0], silver_fed_confirm_button_4[1])
                pyautogui.click(silver_fed_confirm_button_4[0], silver_fed_confirm_button_5[1])
                pyautogui.click(silver_fed_confirm_button_4[0], silver_fed_confirm_button_6[1])
                
                time.sleep(2)
                pyautogui.moveTo(1200, 170)
                time.sleep(1.5)    
                pyautogui.click(compact[0], compact[1])

                break 
    
def salvage_ectos():
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

                consume_luck()

                break  
            
def sell_ectos():
    # Identify ectos by image to salvage
    image_path = './items-to-sell/globs_of_ectoplasm.png'  
    loc, w, h = search_for_item(image_path, 0.7)

    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template

            # Check if the center of the found item is within the defined area
            if inventory_area[0] <= center_x <= inventory_area[0] + inventory_area[2] and inventory_area[1] <= center_y <= inventory_area[1] + inventory_area[3]:
                pyautogui.click(pt[0] + w/2, pt[1] + h/2)  # Click on the identified Ecto
                pyautogui.rightClick()
                time.sleep(0.5)
                pyautogui.move(53, 125) # Move cursor to "Sell" option
                pyautogui.click()

                can_continue('./canContinue/menus_setup.png') 
                # time.sleep(4) 

                pyautogui.click(sellers_list[0], sellers_list[1]) # Add to sell list
                time.sleep(0.25)
                pyautogui.click(maximum_amount[0], maximum_amount[1]) # Maximum Amount
                time.sleep(0.25)
                pyautogui.click(minus_one_copper[0], minus_one_copper[1])  # Minus One Copper
                time.sleep(0.25)
                pyautogui.click(list_item[0], list_item[1]) # List
                # Wait for confirmation that the sale was successful
                can_continue('./canContinue/Success.png')

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
                pyautogui.move(53, 125) # Move cursor to "Sell" option
                pyautogui.click()
                # time.sleep(4) 
                can_continue('./canContinue/menus_setup.png') 

                pyautogui.click(sellers_list[0], sellers_list[1]) # Add to sell list
                time.sleep(0.25)
                pyautogui.click(maximum_amount[0], maximum_amount[1]) # Maximum Amount
                time.sleep(0.25)
                pyautogui.click(minus_one_copper[0], minus_one_copper[1])  # Minus One Copper
                time.sleep(0.25)
                pyautogui.click(list_item[0], list_item[1]) # List
                
                # Wait for confirmation that the sale was successful
                can_continue('./canContinue/Success.png')

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
     if is_item_present('./items-to-sell/blue_luck.png', 0.7):
        consume_purple_luck()
        consume_purple_luck_click_button()
        handle_errors()
        
        # List of image paths for different charms
        luck_images = [
            './items-to-sell/blue_luck.png',
            './items-to-sell/green_luck.png',
            './items-to-sell/yellow_luck.png',
            './items-to-sell/blue_luck.png',
        ]

        for image_path in luck_images:
            # Identify All Luck
            loc, w, h = search_for_item(image_path, 0.9)

            if loc is not None:
                for pt in zip(*loc[::-1]):
                    center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template
                    
                    # Check if the center of the found item is within the defined area
                    if inventory_area[0] <= center_x <= inventory_area[0] + inventory_area[2] and inventory_area[1] <= center_y <= inventory_area[1] + inventory_area[3]:
                        pyautogui.moveTo(pt[0] + w/2, pt[1] + h/2)  # Click on Luck
                        pyautogui.rightClick()
                        time.sleep(0.5)
                        pyautogui.move(20, 125) # Move cursor to consume option
                        pyautogui.click()
                        # time.sleep(.5) 

                        break 

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
        

def handle_errors_2():
    # Press cancel buttons
    err_buttons_coords_list = [
        (2119, 1156),  
        (2129, 1181), 
        (2119, 1156),  
        (2129, 1181), 
        (2119, 1156),  
        (2129, 1181), 
        (2119, 1156),  
        (2129, 1181), 
        (2119, 1156),  
        (2129, 1181), 
        (2119, 1156),  
        (2129, 1181),        
    ]

    for coords in err_buttons_coords_list:
        pyautogui.click(coords[0], coords[1])
        time.sleep(0.25)
        
def handle_errors():
    #? Fatal Error
    if is_item_present('./canContinue/ERR.png', 0.8):
        err_coo = (2367, 885)

        print("ERR, restarting")
        pyautogui.click(err_coo[0], err_coo[1]) #! Adjust Img Recognition
        time.sleep(.5)
        pyautogui.click(err_coo[0], err_coo[1])
        time.sleep(2)

        restart_game()
        reset_position()
        open_menus()

        use_salvage_kits()

        handle_errors_2()
        manage_rare_gear()

        consume_luck()

        sell_item('./items-to-sell/lucent_motes.png')
        sell_all()

    #? Blacker Screen
    if is_item_present('./canContinue/ERR_2.png', 0.7):
        print("ERR_2, closing ERR_2")

        while is_item_present('./canContinue/ERR_2.png', 0.7):
            handle_errors_2()
            time.sleep(2)

        use_salvage_kits()

        handle_errors_2()
        manage_rare_gear()

        consume_luck()


        sell_item('./items-to-sell/lucent_motes.png')
        sell_all()
    
    #? Black Screen Fatal
    if is_item_present('./canContinue/select_character.png', 0.8):
        restart_game()
        reset_position()
        open_menus()

        use_salvage_kits()

        handle_errors_2()
        manage_rare_gear()

        consume_luck()

        sell_item('./items-to-sell/lucent_motes.png')
        sell_all()

    if is_item_present('./canContinue/windows_desktop.png', 0.8):
        restart_game()
        reset_position()
        open_menus()

        use_salvage_kits()

        handle_errors_2()
        manage_rare_gear()

        consume_luck()

        sell_item('./items-to-sell/lucent_motes.png')
        sell_all()

def is_item_present(image_path, threshold):
    screenshot_gray = capture_game_screen() 
    itemImage = cv2.imread(image_path, 0)
    w, h = itemImage.shape[::-1]
    res = cv2.matchTemplate(screenshot_gray, itemImage, cv2.TM_CCOEFF_NORMED)
    return np.any(res >= threshold)

def restart_or_not():
    # Check Volunteer  
    pyautogui.click(2, 1176)
    time.sleep(0.7)

    if is_item_present('./canContinue/volunteer.png', 0.7):
        print("Vounteer is on, restarting")
        time.sleep(3)

        # Volunteer
        pyautogui.click(volunteer[0], volunteer[1])
        time.sleep(10)

        reset_position()
        walk_and_center_npc()
        open_menus()
    
    else:
        print("No volunteer message, reopen menus")

def open_game(): 
    game_icon_coords = (180, 2122)
    login_button_coords = (1203, 1327)
    character_coords = (1600, 2015)

    # Click on the game icon to start the game
    pyautogui.click(game_icon_coords[0], game_icon_coords[1])
    time.sleep(6)
    can_continue('./canContinue/Game_client.png')

    # Click on the login button
    pyautogui.click(login_button_coords[0], login_button_coords[1])
    time.sleep(.5)
    pyautogui.click(login_button_coords[0], login_button_coords[1])
    
    if is_item_present('./canContinue/Game_client.png'):
        pyautogui.click(login_button_coords[0], login_button_coords[1])
        time.sleep(.5)
        pyautogui.click(login_button_coords[0], login_button_coords[1])
        
    if is_item_present('./canContinue/Game_client.png'):
        pyautogui.click(login_button_coords[0], login_button_coords[1])
        time.sleep(.5)
        pyautogui.click(login_button_coords[0], login_button_coords[1])
    
    # Wait for login to process and auto start game
    can_continue('./canContinue/select_character.png')
    time.sleep(2)

    # Double-click on the character to start playing
    pyautogui.doubleClick(character_coords[0], character_coords[1])
    # Wait for the game to enter into playing mode
    can_continue('./canContinue/playing_mode.png')
    time.sleep(.5)
    pyautogui.doubleClick(character_coords[0], character_coords[1])
    time.sleep(.5)
    pyautogui.doubleClick(character_coords[0], character_coords[1])
    
    # Wait for the game to enter into playing mode
    can_continue('./canContinue/playing_mode.png')
    
def restart_game():
    pyautogui.click(1800, 500)

    # Coordinates for game icon, login, start game, and character selection
    game_icon_coords = (180, 2122)
    login_button_coords = (1203, 1327)
    character_coords = (1600, 2015)

    # Close Game
    keyboard.press_and_release('alt+f4')
    time.sleep(3)

    if is_item_present('./canContinue/shut_down_windows.png', 0.8):
        keyboard.press_and_release('alt+f4')
        time.sleep(1)

    # Click on the game icon to start the game
    pyautogui.click(game_icon_coords[0], game_icon_coords[1])
    time.sleep(6)
    can_continue('./canContinue/Game_client.png')

    # Click on the login button
    pyautogui.click(login_button_coords[0], login_button_coords[1])
    time.sleep(.5)
    pyautogui.click(login_button_coords[0], login_button_coords[1])
    time.sleep(7)  # Wait for login to process and auto start game

    if is_item_present('./canContinue/client_open.png', 0.8):
        pyautogui.click(login_button_coords[0], login_button_coords[1])
        time.sleep(7)

    if is_item_present('./canContinue/client_open.png', 0.8):
        pyautogui.click(login_button_coords[0], login_button_coords[1])
        time.sleep(7)

    can_continue('./canContinue/select_character.png')
    time.sleep(3)

    # Double-click on the character to start playing
    pyautogui.doubleClick(character_coords[0], character_coords[1])
    time.sleep(.5)
    pyautogui.doubleClick(character_coords[0], character_coords[1])
    time.sleep(.5)
    pyautogui.doubleClick(character_coords[0], character_coords[1])

    # Wait for the game to enter into playing mode
    can_continue('./canContinue/playing_mode.png')

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
  
    pyautogui.doubleClick(portal_scroll[0], portal_scroll[1]) #! Adjust Img Recognition
    time.sleep(5)

    can_continue('./canContinue/playing_mode.png')
    time.sleep(1)

    pyautogui.click(inventory_close[0], inventory_close[1]) #! Adjust Img Recognition
    time.sleep(1)

    keyboard.press_and_release('ctrl+z')
    time.sleep(1)

    pyautogui.doubleClick(mistlock[0], mistlock[1]) #! Adjust Img Recognition
    time.sleep(3)
    can_continue('./canContinue/playing_mode.png')

def walk_and_center_npc():
    # Close menus
    while not is_item_present('./canContinue/esc_menu.png', 0.7):
        keyboard.press_and_release('esc')
        time.sleep(0.25)
        
    keyboard.press_and_release('esc')
    time.sleep(0.25)
    
    # Reset Position by clicking Mistlock pass
    reset_position() 

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

        reset_position()

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

    #! Check if is the other menu walk to the right slightly

    # Walk slightly to the right to the bank NPC and open it
    press_and_hold('e', hold_time=1) 
    keyboard.press_and_release('tab')
    time.sleep(1)

    # Walk back to the initial place
    press_and_hold('q', hold_time=1)  #

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
        reset_position()
        walk_and_center_npc()
        open_menus()
    print("TP and Bank are correctly set up.")

    while not does_it_match('./center_character/correct_inventory.png', 0.8):
        print("Menus are not correctly set up, re-centering NPC...")
        reset_position()
        walk_and_center_npc()
        open_menus()
    print("Inventory is correctly set up. Continue.")

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
        # time.sleep(7)
        can_continue('./canContinue/Success.png') #! same success window? lol

        # Close last sell
        pyautogui.click(3517, 186)
        time.sleep(1.5)


def salvage_restant_exotics():
    accept_button = (1896, 1156) 
    
    # Compact Inventory
    pyautogui.click(compact[0], compact[1])
    time.sleep(0.5)
    
    # Identify Silver Fed 
    loc, w, h = search_for_item('./items-to-sell/silver.png', 0.7)

    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template
            
            # Check if the center of the found item is within the defined area
            if inventory_area[0] <= center_x <= inventory_area[0] + inventory_area[2] and inventory_area[1] <= center_y <= inventory_area[1] + inventory_area[3]:
                # Setup Silver Fed
                pyautogui.moveTo(pt[0] + w/2, pt[1] + h/2)  # Click on Silver Fed
                pyautogui.rightClick()
                time.sleep(0.5)
                pyautogui.move(20, 16) # Move cursor to use
                pyautogui.click()
                time.sleep(.5) 

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
            ]

            for coords in salvage_exotics_coords_list:
                pyautogui.moveTo(coords[0], coords[1])
                pyautogui.click()
                time.sleep(0.25)
                pyautogui.click(accept_button[0], accept_button[1]) # Accept salvage
                time.sleep(0.25)

            manage_cristallyne_dust()
            break

def salvage_restant_exotics_few():    
    accept_button = (1896, 1156) 
    
    # Compact Inventory
    pyautogui.click(compact[0], compact[1])
    time.sleep(0.5)
    
    # Identify Silver Fed 
    loc, w, h = search_for_item('./items-to-sell/silver.png', 0.7)

    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template
            
            # Check if the center of the found item is within the defined area
            if inventory_area[0] <= center_x <= inventory_area[0] + inventory_area[2] and inventory_area[1] <= center_y <= inventory_area[1] + inventory_area[3]:
                # Setup Silver Fed
                pyautogui.moveTo(pt[0] + w/2, pt[1] + h/2)  # Click on Silver Fed
                pyautogui.rightClick()
                time.sleep(0.5)
                pyautogui.move(20, 16) # Move cursor to use
                pyautogui.click()
                time.sleep(.5) 

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
            ]

            for coords in salvage_exotics_coords_list:
                pyautogui.moveTo(coords[0], coords[1])
                pyautogui.click()
                time.sleep(0.25)
                pyautogui.click(accept_button[0], accept_button[1]) # Accept salvage
                time.sleep(0.25)
        
            break

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
        time.sleep(3)
        pyautogui.click(2817, 1991)  
        time.sleep(3)

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

def remove_oldest_orders(orders=5):
    # Close last sell
    pyautogui.click(3517, 186)
    time.sleep(.7)

    #? Click My transactions
    pyautogui.click(3700, 128)
    time.sleep(3)

    #! If is on, proceed, if not click, 
    #! but is gonna be off in general 
    #? Click Buying
    pyautogui.click(2487, 358)
    time.sleep(3)

    #? Click on Price
    pyautogui.click(3558, 290)
    time.sleep(.5)

    #? Cancel Orders
    for _ in range(orders):
        pyautogui.click(3732, 359)
        time.sleep(.4)
        pyautogui.click(3732, 359)
        time.sleep(.4)
    
    # Open "Sell Items"
    time.sleep(.4)
    pyautogui.click(3517, 186)

def place_10_orders(orders=15, blue=False):
    # Close last sell
    pyautogui.click(3517, 186)
    time.sleep(.7)
    # Open "Sell Items"
    pyautogui.click(3517, 186)

    # Click Home
    pyautogui.click(2948, 136)
    time.sleep(2)
  
    # Click search
    pyautogui.click(2498, 242)
    time.sleep(0.5)

    # Type piece of unidentified gear
    pyautogui.write('piece of unidentified gear', interval=0.1)
    time.sleep(2)

    if not blue:
        # If blue is False, click Green
        pyautogui.click(2873, 356)
        can_continue('./canContinue/menus_setup.png') 
    else:
        # If blue is True, click Blue
        pyautogui.click(2873, 545) 
        can_continue('./canContinue/menus_setup.png') 

    # Click on order
    pyautogui.click(2733, 746)
    time.sleep(1)

    # 250
    pyautogui.click(3284, 356)
    time.sleep(1)
    
    # Place order
    for _ in range(orders):
        pyautogui.click(3007, 555)
        can_continue('./canContinue/Success_green.png')
        pyautogui.click(3007, 555)
        time.sleep(.3)
    
    # Close last sell
    pyautogui.click(3517, 186)
    time.sleep(1)
    # Open "Sell Items"
    pyautogui.click(3517, 186)

def place_orders_rare(iterations=1):
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
    pyautogui.click(2873, 449)
    can_continue('./canContinue/menus_setup.png') 

    # Click on order
    pyautogui.click(2733, 746)
    time.sleep(1)

    # 250
    pyautogui.click(3284, 356)
    time.sleep(1)

    # Plus One Copper
    pyautogui.click(plus_one_copper[0], plus_one_copper[1])  
    time.sleep(0.7)

    if is_item_present('./canContinue/correct_order.png', 0.7):
        # Place order
        for _ in range(iterations):
            pyautogui.click(3007, 555)
            can_continue('./canContinue/Success_green.png')
            pyautogui.click(3007, 555)
            time.sleep(.3)

    else:
        # Minus One Copper
        pyautogui.click(minus_one_copper[0], minus_one_copper[1])  
        time.sleep(0.4)

        for _ in range(iterations):
            pyautogui.click(3007, 555)
            can_continue('./canContinue/Success_green.png')
            pyautogui.click(3007, 555)
            time.sleep(.3)
    
    # Close last sell
    pyautogui.click(3517, 186)
    time.sleep(1)
    # Open "Sell Items"
    pyautogui.click(3517, 186)

            
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
                    can_continue('./canContinue/menus_setup.png') 

                    pyautogui.click(sellers_list[0], sellers_list[1])  # Add to sell list
                    time.sleep(0.25)
                    pyautogui.click(maximum_amount[0], maximum_amount[1])  # Set Maximum Amount
                    time.sleep(0.25)
                    pyautogui.click(minus_one_copper[0], minus_one_copper[1])  # Minus One Copper
                    time.sleep(0.25)
                    pyautogui.click(list_item[0], list_item[1])  # List the item for sale

                    can_continue('./canContinue/Success.png')
                    break  # Break after processing the first valid charm

            time.sleep(1)  # Sleep between processing different charms to manage screen updates and avoid rapid-fire actions

def can_continue(image_path, timeout=9):
    # Load the image to find in grayscale
    template_color = cv2.imread(image_path)
    template = cv2.cvtColor(template_color, cv2.COLOR_BGR2GRAY)
    start_time = time.time()

    while time.time() - start_time < timeout:
        screen = capture_game_screen()
        # Perform template matching
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        # If the image is found with a high enough confidence, return True
        if max_val >= 0.8:
            return True

        time.sleep(.4)  # Check every second

    # If the loop exits without finding the image, return False
    return False

def sell_item(image_path):
    # Load the image of the item to sell and search for it on screen
    loc, w, h = search_for_item(image_path, 0.8)

    # Proceed if there are matches found
    if loc is not None:
        for pt in zip(*loc[::-1]):
            center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template
            
            # Check if the center of the found item is within the defined area
            if sell_search_area[0] <= center_x <= sell_search_area[0] + sell_search_area[2] and sell_search_area[1] <= center_y <= sell_search_area[1] + sell_search_area[3]:
                pyautogui.rightClick(center_x, center_y)  # Right-click on the identified item
                time.sleep(0.5)
                pyautogui.move(16, 88)  # Move cursor to "Sell" option
                pyautogui.click()

                can_continue('./canContinue/menus_setup.png') 
                # time.sleep(3)  # Delay to allow UI to respond

                # Interact with the selling interface
                pyautogui.click(sellers_list[0], sellers_list[1])  # Click on add to sell list
                time.sleep(0.25)
                pyautogui.click(maximum_amount[0], maximum_amount[1])  # Click to set maximum amount
                time.sleep(0.25)
                pyautogui.click(list_item[0], list_item[1])  # Click to list the item for sale

                # Wait for confirmation that the sale was successful
                can_continue('./canContinue/Success.png')

                break  # Exit after processing the first valid item
            
def sell_all(): 
    # List of image paths for different charms
    charm_images = [
        './items-to-sell/ancient_wood_logs.png',
        './items-to-sell/elder_wood_logs.png',
        './items-to-sell/gossamer_Scraps.png',
        './items-to-sell/hardened_leather_sections.png',
        './items-to-sell/mithril_ore.png',
        './items-to-sell/orichalcum_ore.png',
        './items-to-sell/silk_scraps.png',
        './items-to-sell/thick_leather_sections.png',
    ]

    for image_path in charm_images:
        loc, w, h = search_for_item(image_path, 0.8)
        
        if loc is not None:
            for pt in zip(*loc[::-1]):
                center_x, center_y = pt[0] + w//2, pt[1] + h//2  # Calculate the center of the found template
                
                # Check if the center of the found item is within the defined area
                if sell_search_area[0] <= center_x <= sell_search_area[0] + sell_search_area[2] and sell_search_area[1] <= center_y <= sell_search_area[1] + sell_search_area[3]:
                    pyautogui.rightClick(center_x, center_y)  # Click on the identified charm
                    time.sleep(0.5)
                    pyautogui.move(16, 88)  # Move to "Sell" option
                    pyautogui.click()
                    can_continue('./canContinue/menus_setup.png') 

                    pyautogui.click(sellers_list[0], sellers_list[1])  # Add to sell list
                    time.sleep(0.25)
                    pyautogui.click(maximum_amount[0], maximum_amount[1])  # Set Maximum Amount
                    time.sleep(0.25)
                    # pyautogui.click(minus_one_copper[0], minus_one_copper[1])  # Minus One Copper
                    # time.sleep(0.25)
                    pyautogui.click(list_item[0], list_item[1])  # List the item for sale

                    can_continue('./canContinue/Success.png')
                    break  # Break after processing the first valid charm

            time.sleep(1)  # Sleep between processing different charms to manage screen updates and avoid rapid-fire actions

def click_game():
    pyautogui.click(78, 700)
    time.sleep(0.5)

    # Sell items section
    pyautogui.click(3450, 125)
    time.sleep(1.5)

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

def calculate_ecto_profit(ecto_price, dust_price):
    dust_yield = 1.85
    silver_cost_per_use = 0.006
    ecto_count = 7.45
    tp_fee_factor = 0.85

    # Calculating the total revenue from direct sale of ectos after TP fee
    direct_sale_revenue = ecto_price * ecto_count * tp_fee_factor

    # Calculating the total revenue from selling dust after salvage and TP fee
    total_silver_cost = silver_cost_per_use * ecto_count
    dust_revenue = ((dust_yield * dust_price * ecto_count) - total_silver_cost) * tp_fee_factor

    print(f"Total revenue from selling {ecto_count} ectos directly is {direct_sale_revenue:.2f} gold.")
    print(f"Total revenue from salvaging {ecto_count} ectos and selling the dust is {dust_revenue:.2f} gold.")

    # Calculating the revenue difference and printing the more profitable option
    revenue_difference = abs(dust_revenue - direct_sale_revenue)

    if dust_revenue > direct_sale_revenue:
        print(f"Salvage Ectos: +{revenue_difference:.2f}")
        # salvage_ectos()
    else:
        print(f"Sell Ectos Directly: +{revenue_difference:.2f}")
        # sell_ectos()

def main():
    click_game()
    # calculate_ecto_profit(0.3821, 0.2174)
    
    # open_menus()

    sell_item('./items-to-sell/lucent_motes.png')
    sell_all()
    # manage_charms()

    consume_luck()

    # take_all_and_storage(2)

    # salvage_restant_exotics()

    # place_10_orders(15, blue=False)
    # remove_oldest_orders(5)
    
    for i in range(1, 51):  
        # while True:
        #     if keyboard.is_pressed('shift+p'):
        #         print("Script detenido por el usuario")
        #         break
        
        print(f"Iteration {i}")

        handle_errors()
        manage_rare_gear()

        #? In case Green's are better 
        handle_errors()
        manage_unidentified_gear()
        time.sleep(10)

        handle_errors()
        use_salvage_kits() 
        handle_errors()

        #? In case Blue's are better 
        # handle_errors()
        # manage_common_gear()
        # handle_errors()

        sell_item('./items-to-sell/lucent_motes.png')
        consume_luck()
        

        if i % 2 == 0: 
            # consume_luck()

            sell_item('./items-to-sell/mithril_ore.png')
            handle_errors() 

            sell_item('./items-to-sell/elder_wood_logs.png')

        if i % 3 == 0:  
            sell_item('./items-to-sell/silk_scraps.png')
            sell_item('./items-to-sell/thick_leather_sections.png')

        # if i % 5 == 0:
            # place_orders_rare(1) 

        if i % 10 == 0:  
            # Checkers that watch and reload online prices
            sell_ectos() 
            # salvage_ectos()

            delete_dark_matter()
            manage_cristallyne_dust()
            handle_errors()

            manage_charms()
            manage_charms()
            manage_charms()
            manage_charms()
            sell_all()
            sell_all()
            sell_all()
            handle_errors()

            # place_orders_rare(1) 
            # place_10_orders(11, blue=True)
            place_10_orders(11, blue=False)
            remove_oldest_orders(1)

        if i % 10 == 0:            
            consume_luck()

            #! Checkers to avoid losing time
            take_all_and_storage(1)
        
        if i % 25 == 0:  
            manage_charms()
            manage_charms()
            manage_charms()
            manage_charms()
            sell_all()
            sell_all()
            sell_all()
            handle_errors()
 
            sell_ectos() 
            # salvage_ectos()

            sell_most_expensive_exotics(4)
            salvage_restant_exotics()
            manage_cristallyne_dust()

            restart_or_not()
        
        # Add a short sleep time if needed between iterations to avoid overwhelming the application
        # time.sleep(2)

if __name__ == "__main__":
    main()
