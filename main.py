import cv2
import numpy as np
import pyautogui
import time

# Areas Coordinates
inventory_area = (0, 0, 2350, 2160)
bank_area = (2840, 1125, 3840, 2160)
tp_area = (2430, 60, 3840, 1090)
tp_price_area = () # Little square of silver and gold price area

compact = (2229, 176)
take_all = (2615, 1025)

rune_crafter = (481, 287)
rune_crafter_confirm_button = (1811, 1415)

silver_fed = (566, 285)
silver_fed_confirm_button = (1811, 1247)
silver_fed_confirm_button_2 = (1811, 1219)
silver_fed_confirm_button_3 = (1811, 1286)


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
            


def main():
    
    manage_unidentified_gear()
    time.sleep(13)

if __name__ == "__main__":
    main()
