from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import qrcode
from pyzbar.pyzbar import decode


class Wow(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.camera_image = Image()
        self.layout.add_widget(self.camera_image)
        self.results_label = Label(text="Scanning QR codes...")
        self.layout.add_widget(self.results_label)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/30.0)  # Update every 30 frames per second
        return self.layout

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            decoded_objects = decode(frame)
            self.show_frame(frame, decoded_objects)

    def show_frame(self, frame, decoded_objects):
        for obj in decoded_objects:
            x, y, w, h = obj.rect
            qr_data = obj.data.decode('utf-8')
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.camera_image.texture = image_texture

        if decoded_objects:
            self.results_label.text = "\n".join([obj.data.decode('utf-8') for obj in decoded_objects])
        else:
            self.results_label.text = "Scanning QR codes..."

if __name__ == '__main__':
    Wow().run()
