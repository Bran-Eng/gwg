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
    time.sleep(1)
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
                time.sleep(1)
                find_and_click(step=1)
                return True
                
    elif step == 3:        
        pyautogui.moveTo(3280, 1800)        
        for _ in range(5):
            pyautogui.scroll(-500)  
            pyautogui.scroll(-500)
            pyautogui.scroll(-500)
            pyautogui.scroll(-500)            
            time.sleep(1)  

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
    # 1/5) Use Runecrafter for salvaging greens
    pyautogui.moveTo(rune_crafter[0], rune_crafter[1])
    pyautogui.rightClick() 
    pyautogui.click(rune_crafter_salvage_green[0], rune_crafter_salvage_green[1])
    pyautogui.click(rune_crafter_confirm_button[0], rune_crafter_confirm_button[1])
    time.sleep(30)

    # 2/5) Use Silver Fed for salvaging rares
    pyautogui.moveTo(silver_fed[0], silver_fed[1])
    pyautogui.rightClick()
    pyautogui.click(silver_fed_salvage_rare[0], silver_fed_salvage_rare[1])
    # Press confirm button using 3 coordinates for tackling possible placements
    pyautogui.click(silver_fed_confirm_button[0], silver_fed_confirm_button[1])
    pyautogui.click(silver_fed_confirm_button_2[0], silver_fed_confirm_button_2[1])
    pyautogui.click(silver_fed_confirm_button_3[0], silver_fed_confirm_button_3[1])
    time.sleep(6)
    


def manage_ectos():
    # Salvage ectos using Silver Fed (Assuming coordinates are for salvaging ectos)
    pyautogui.moveTo(silver_fed[0], silver_fed[1])
    pyautogui.rightClick()
    pyautogui.click(silver_fed_salvage_stack[0], silver_fed_salvage_stack[1]) 
    time.sleep(1) 

    # Identify ectos by image 
    image_path = './items-to-sell/globs_of_ectoplasm.png'  
    loc, w, h = search_for_item(image_path, 0.7)
    if loc is not None:
        for pt in zip(*loc[::-1]):
            pyautogui.click(pt[0] + w/2, pt[1] + h/2)  # Click on the identified ecto
            pyautogui.click(silver_fed_salvage_stack_accept[0], silver_fed_salvage_stack_accept[1])
            time.sleep(12) #! Adjust ecto time
            break  

    


def process_and_sell_items():
    use_salvage_kits()  
    manage_ectos() 

def main():
    # Add loop
    manage_unidentified_gear()
    time.sleep(13)
    process_and_sell_items()  

if __name__ == "__main__":
    main()
