from wsgiref.util import is_hop_by_hop
import numpy as np, cv2 as cv

WAIT = 1000
MARGIN_L = 10
MARGIN_U = 10
MARGIN_R = 500
MARGIN_D = 500

BUTTON_L = MARGIN_L+20
BUTTON_U = MARGIN_U+110
BUTTON_R = MARGIN_R-20
BUTTON_D = MARGIN_D-330
BUTTON_C = ((BUTTON_L+BUTTON_R)//2,(BUTTON_D+BUTTON_U)//2)
BUTTON_OFFSET = 70
B_COLOR = (255,0,0)
B_THICC = -1

class Application:
    def __init__(self):
        self.__root = "toor"
        self.__window = np.ones((512,512,3),np.uint8)

        cv.namedWindow(self.__root)
        cv.setMouseCallback(self.__root, self.on_mouse_event)

    def draw_window(self):
        self.__window = cv.rectangle(self.__window, (MARGIN_L,MARGIN_U), (MARGIN_R,MARGIN_D), (0,0,255), 2)
        
        self.__window = cv.rectangle(self.__window, (BUTTON_L,BUTTON_U), (BUTTON_R,BUTTON_D), B_COLOR, B_THICC)
        cv.putText(self.__window, '1: Daily log', (-100+BUTTON_C[0], BUTTON_C[1]), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        
        self.__window = cv.rectangle(self.__window, (BUTTON_L,BUTTON_U+BUTTON_OFFSET), (BUTTON_R,BUTTON_D+BUTTON_OFFSET), B_COLOR, B_THICC)
        cv.putText(self.__window, '2: Project log', (-125+BUTTON_C[0], BUTTON_C[1]+BUTTON_OFFSET), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        
        self.__window = cv.rectangle(self.__window, (BUTTON_L,BUTTON_U+2*BUTTON_OFFSET), (BUTTON_R,BUTTON_D+2*BUTTON_OFFSET), B_COLOR, B_THICC)
        cv.putText(self.__window, '3: Settings', (-100+BUTTON_C[0], BUTTON_C[1]+2*BUTTON_OFFSET), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        
        self.__window = cv.rectangle(self.__window, (BUTTON_L,BUTTON_U+3*BUTTON_OFFSET), (BUTTON_R,BUTTON_D+3*BUTTON_OFFSET), B_COLOR, B_THICC)
        cv.putText(self.__window, 'p: Process Data', (-125+BUTTON_C[0], BUTTON_C[1]+3*BUTTON_OFFSET), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        
        cv.imshow(self.__root, self.__window)

    def on_mouse_event(self, event, x, y, flags, param):
        pass

    def daily_log_button_press(device=0):
        pass
        
    def project_log_button_press():
        pass

    def settings_button_press():
        pass
    
    def process_data_button_press():
        pass

    def __call__(self):
        while cv.getWindowProperty(self.__root, cv.WND_PROP_VISIBLE):
            self.draw_window()
            command = cv.waitKey(WAIT)

            if command == ord('q'):
                break
            if command == ord('1'):
                print("Daily Log")
                cv.destroyAllWindows()
                self.daily_log_button_press()
                self.draw_window()
            if command == ord('2'):
                print("Project Log")
                self.project_log_button_press()
            if command == ord('3'):
                print("Settings")
                self.settings_button_press()
            if command == ord('p'):
                print("Data Processing")
                self.process_data_button_press()

        cv.destroyAllWindows()
