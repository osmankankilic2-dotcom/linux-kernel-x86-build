from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import threading
import os
import yt_dlp

class AslanVideoDownloaderApp(App):
    def build(self):
        self.title = "Aslan Video İndirici"
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        # Title Label
        title_label = Label(
            text="🦁 Aslan Video İndirici",
            font_size='24sp',
            size_hint_y=None,
            height='50dp',
            color=(1, 0.6, 0, 1)
        )
        layout.add_widget(title_label)
        
        # URL Input
        self.url_input = TextInput(
            text='',
            hint_text='Video bağlantısını buraya yapıştırın (YouTube, TikTok, vb.)...',
            size_hint_y=None,
            height='50dp',
            multiline=False
        )
        layout.add_widget(self.url_input)
        
        # Download Button
        self.download_btn = Button(
            text='Videoyu İndir',
            size_hint_y=None,
            height='55dp',
            background_color=(0.1, 0.6, 0.9, 1)
        )
        self.download_btn.bind(on_press=self.start_download_thread)
        layout.add_widget(self.download_btn)
        
        # Status / Log Output
        scroll = ScrollView(size_hint=(1, 1))
        self.status_label = Label(
            text='İndirmeye hazır...',
            size_hint_y=None,
            halign='left',
            valign='top',
            color=(0.9, 0.9, 0.9, 1)
        )
        self.status_label.bind(
            width=lambda *x: setattr(self.status_label, 'text_size', (self.status_label.width, None)),
            texture_size=lambda *x: setattr(self.status_label, 'height', self.status_label.texture_size[1])
        )
        scroll.add_widget(self.status_label)
        layout.add_widget(scroll)
        
        return layout

    def log_message(self, message):
        Clock.schedule_once(lambda dt: self._update_log(message))

    def _update_log(self, message):
        self.status_label.text += f"\n{message}"

    def start_download_thread(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "Hata: Lütfen geçerli bir video URL'si girin!"
            return
        
        self.download_btn.disabled = True
        self.status_label.text = f"İndirme başlatılıyor: {url}"
        
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.daemon = True
        thread.start()

    def download_video(self, url):
        download_path = os.path.expanduser("~/Download")
        if not os.path.exists(download_path):
            os.makedirs(download_path, exist_ok=True)
            
        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.ytdl_hook],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.log_message("✅ İndirme başarıyla tamamlandı!")
        except Exception as e:
            self.log_message(f"❌ Hata oluştu: {str(e)}")
        finally:
            Clock.schedule_once(lambda dt: setattr(self.download_btn, 'disabled', False))

    def ytdl_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%')
            speed = d.get('_speed_str', 'N/A')
            self.log_message(f"İndiriliyor: {percent} (Hız: {speed})")

if __name__ == '__main__':
    AslanVideoDownloaderApp().run()
