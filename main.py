import cv2
import numpy as np
import pyautogui
import time

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
    threshold=0.7
    
    if step == 1 or step == 2:
        loc, w, h = search_for_item(image_path, threshold)
        # if loc is not None:
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
    pyautogui.moveTo(1200, 170)
    time.sleep(2.2)    
    
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
            time.sleep(1.3)
            break  
        
def manage_cristallyne_dust():   
    # Identify drystalline dust by image to salvage
    image_path = './items-to-sell/pile_of_cristallyne_dust.png'  
    loc, w, h = search_for_item(image_path, 0.7)
    if loc is not None:
        for pt in zip(*loc[::-1]):
            pyautogui.rightClick(pt[0] + w/2, pt[1] + h/2)  # Click on the identified crystallyne
            time.sleep(0.25)
            pyautogui.move(15, 127) 
            pyautogui.click()
            time.sleep(1) 

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
    loc, w, h = search_for_item(image_path, 0.8)
    if loc is not None:
        for pt in zip(*loc[::-1]):
            pyautogui.click(pt[0] + w/2, pt[1] + h/2)  # Click on the identified purple luck
            pyautogui.rightClick()
            time.sleep(0.25)
            pyautogui.move(16, 162) #! Destroy purple luck
            pyautogui.click()            
            break  

def consume_luck():
    # Consume All Luck from multiple locations
    consume_luck_coords_list = [
        (1101, 1535),  
        (1191, 1535),  
        (1278, 1535),
        (1366, 1535),
        (1453, 1535),
        (1547, 1535)
    ]

    for coords in consume_luck_coords_list:
        pyautogui.moveTo(coords[0], coords[1])
        pyautogui.rightClick()
        time.sleep(0.25)
        pyautogui.move(16, 125) # Consume All
        # pyautogui.move(16, 164) # purple one
        pyautogui.click()
        time.sleep(0.25)

def sell_items():
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
        time.sleep(1.7)        

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
 
def sell_metal_plates():
    pyautogui.click()  

def main():
    #! Make Logic to make some of the steps to trigger every x loops
    #! Make another sell items that only sells the most common. Use the full sell every x loops
    for _ in range(90):
        manage_unidentified_gear()
        time.sleep(11)

        use_salvage_kits()  
        manage_ectos()
        manage_cristallyne_dust()
        consume_purple_luck()
        consume_luck()
        sell_items()
        delete_dark_matter() 

        # Add a short sleep time if needed between iterations to avoid overwhelming the application
        time.sleep(2)

if __name__ == "__main__":
    main()
