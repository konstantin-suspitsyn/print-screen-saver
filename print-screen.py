import enum
import datetime as dt
import os
from PIL import ImageGrab
from typing import Optional
from pynput import keyboard


class ScreenshotSaver:

    """
    Listens to the keyboard
    On PrtScreen release makes screenshot and saves it into folder

    Resulting folder structure will be like this:

    self.screen_folder_path_parent/
    ├─ class started as service named folder ("%Y-%m-%d-%H-%M-%S")
    │ ├─ 001.png
    │ ├─ ....png
    │ └─ ∞.png
    ├─ class started as service named folder ("%Y-%m-%d-%H-%M-%S")
    ...
    """

    def __init__(self, screen_folder_path_parent: str) -> None:
        """
        :param screen_folder_path_parent: Parent folder for the screenshots
        """
        self.full_path: Optional[str | None] = None
        self.made_print_screen: bool = False
        self.screen_folder_path_parent: str = screen_folder_path_parent
        self.screen_folder_path: str = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.screen_no: int = 0

    def is_folder_in(self, screen_folder_path_parent: str, screen_folder_path: str) -> None:
        """
        Checks if parent-folder and sub-folder for screenshots exists
        If not, creates them

        :param screen_folder_path_parent:
        :param screen_folder_path:
        :return:
        """
        if not os.path.exists(screen_folder_path_parent):
            os.mkdir(screen_folder_path_parent)
            os.mkdir(os.path.join(screen_folder_path_parent, screen_folder_path))
        else:
            subdirectories: list[str] = [str(x[0]).rsplit("\\", 1)[-1] for x in os.walk(screen_folder_path_parent)]
            if screen_folder_path not in subdirectories:
                os.mkdir(os.path.join(screen_folder_path_parent, screen_folder_path))

        self.full_path = os.path.join(screen_folder_path_parent, screen_folder_path)

    def on_press(self, key: enum) -> None:
        """
        Listens to the print screen
        :param key: key pressed
        """
        if key == keyboard.Key.print_screen:
            if not self.made_print_screen:
                self.is_folder_in(self.screen_folder_path_parent, self.screen_folder_path)
                self.made_print_screen = True
            im = ImageGrab.grab()
            path_to_image: str = os.path.join(self.full_path, str(self.screen_no).zfill(3))
            im.save("{}.png".format(path_to_image))
            self.screen_no += 1

    def wait_for_screenshots(self):
        """
        Listens to the keyboard in a thread
        :return:
        """
        listener = keyboard.Listener(on_press=self.on_press)
        # start to listen on a separate thread
        listener.start()
        listener.join()


if __name__ == "__main__":
    screenshot_saver = ScreenshotSaver(r"Z:\working\screenshots\python")
    screenshot_saver.wait_for_screenshots()
