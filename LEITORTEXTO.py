import asyncio
import io
import time
import tkinter as tk
import ctypes
import pyautogui
import pyperclip

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

from winrt.windows.graphics.imaging import BitmapDecoder
from winrt.windows.media.ocr import OcrEngine
from winrt.windows.storage.streams import DataWriter, InMemoryRandomAccessStream

class Snipper:

    def __init__(self, root):
        self.root = root

        self.root.attributes("-alpha", 0.3)
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.config(cursor="cross")

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect = None

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2
        )

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.root.withdraw()
        time.sleep(0.1) 

        try:
            self.process_ocr_windows()
        finally:
            self.root.destroy()

    def process_ocr_windows(self):
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        width = abs(self.start_x - self.end_x)
        height = abs(self.start_y - self.end_y)

        if width > 5 and height > 5:
            screenshot = pyautogui.screenshot(region=(x1, y1, width, height))

            img_byte_arr = io.BytesIO()
            screenshot.save(img_byte_arr, format="PNG")
            img_bytes = img_byte_arr.getvalue()
            
            try:
                texto_extraido = asyncio.run(self.run_windows_ocr(img_bytes))
                if texto_extraido:
                    pyperclip.copy(texto_extraido)
                    print("\n--- Texto extraído com sucesso e copiado! ---")
                    print(texto_extraido)
                    print("-" * 40)
                else:
                    print("Nenhum texto detectado na imagem.")
            except Exception as e:
                print(f"Erro ao processar o OCR: {e}")

    async def run_windows_ocr(self, img_bytes):
        data_writer = DataWriter()
        data_writer.write_bytes(img_bytes)
        buffer = data_writer.detach_buffer()

        stream = InMemoryRandomAccessStream()
        await stream.write_async(buffer)
        stream.seek(0)

        decoder = await BitmapDecoder.create_async(stream)
        software_bitmap = await decoder.get_software_bitmap_async()

        engine = OcrEngine.try_create_from_user_profile_languages()
        if not engine:
            return ""

        result = await engine.recognize_async(software_bitmap)
        return "\n".join([line.text for line in result.lines])


if __name__ == "__main__":
    root = tk.Tk()
    app = Snipper(root)
    root.mainloop()
    