from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import threading
import os
import yt_dlp

class AslanVideoDownloaderApp(App):
    def build(self):
        self.title = "Aslan Video İndirici"
        
        root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Scrollable layout for all controls
        scroll = ScrollView(size_hint=(1, 1))
        layout = BoxLayout(orientation='vertical', padding=10, spacing=12, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # Title Label
        title_label = Label(
            text="🦁 Aslan Video İndirici",
            font_size='22sp',
            size_hint_y=None,
            height='45dp',
            color=(1, 0.6, 0, 1),
            bold=True
        )
        layout.add_widget(title_label)
        
        # URL Input
        layout.add_widget(Label(text="Video / Playlist URL:", size_hint_y=None, height='25dp', halign='left'))
        self.url_input = TextInput(
            text='',
            hint_text='Bağlantıyı buraya yapıştırın...',
            size_hint_y=None,
            height='45dp',
            multiline=False
        )
        layout.add_widget(self.url_input)
        
        # Format Selection (MP4 / MP3)
        layout.add_widget(Label(text="İndirme Formatı:", size_hint_y=None, height='25dp', halign='left'))
        self.format_spinner = Spinner(
            text='MP4 (Video)',
            values=('MP4 (Video)', 'MP3 (Sadece Ses)'),
            size_hint_y=None,
            height='45dp'
        )
        layout.add_widget(self.format_spinner)
        
        # Quality Selection
        layout.add_widget(Label(text="Kalite Tercihi:", size_hint_y=None, height='25dp', halign='left'))
        self.quality_spinner = Spinner(
            text='En Yüksek (Best)',
            values=('En Yüksek (Best)', '1080p', '720p', '480p'),
            size_hint_y=None,
            height='45dp'
        )
        layout.add_widget(self.quality_spinner)
        
        # Audio Language Selection
        layout.add_widget(Label(text="Ses Dili Tercihi (Örn: tr, en):", size_hint_y=None, height='25dp', halign='left'))
        self.lang_input = TextInput(
            text='tr',
            hint_text='tr, en vb.',
            size_hint_y=None,
            height='40dp',
            multiline=False
        )
        layout.add_widget(self.lang_input)
        
        # Playlist Checkbox Layout
        playlist_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp', spacing=10)
        self.playlist_checkbox = CheckBox(size_hint_x=None, width='40dp', active=False)
        playlist_layout.add_widget(self.playlist_checkbox)
        playlist_layout.add_widget(Label(text="Oynatma Listesini (Playlist) İndir", halign='left'))
        layout.add_widget(playlist_layout)
        
        # Download Button
        self.download_btn = Button(
            text='🚀 İndirmeyi Başlat',
            size_hint_y=None,
            height='50dp',
            background_color=(0.1, 0.6, 0.9, 1),
            bold=True
        )
        self.download_btn.bind(on_press=self.start_download_thread)
        layout.add_widget(self.download_btn)
        
        # Status / Log Output
        self.status_label = Label(
            text='Sistem hazır. Bağlantı bekleniyor...',
            size_hint_y=None,
            halign='left',
            valign='top',
            color=(0.9, 0.9, 0.9, 1),
            font_size='13sp'
        )
        self.status_label.bind(
            width=lambda *x: setattr(self.status_label, 'text_size', (self.status_label.width, None)),
            texture_size=lambda *x: setattr(self.status_label, 'height', self.status_label.texture_size[1])
        )
        layout.add_widget(self.status_label)
        
        scroll.add_widget(layout)
        root_layout.add_widget(scroll)
        return root_layout

    def log_message(self, message):
        Clock.schedule_once(lambda dt: self._update_log(message))

    def _update_log(self, message):
        self.status_label.text += f"\n{message}"

    def start_download_thread(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "⚠️ Hata: Lütfen geçerli bir URL girin!"
            return
        
        self.download_btn.disabled = True
        self.status_label.text = f"İndirme başlatılıyor..."
        
        # Collect options
        is_mp3 = "MP3" in self.format_spinner.text
        quality = self.quality_spinner.text
        lang = self.lang_input.text.strip()
        is_playlist = self.playlist_checkbox.active
        
        thread = threading.Thread(target=self.download_video, args=(url, is_mp3, quality, lang, is_playlist))
        thread.daemon = True
        thread.start()

    def download_video(self, url, is_mp3, quality, lang, is_playlist):
        download_path = os.path.expanduser("~/Download")
        if not os.path.exists(download_path):
            os.makedirs(download_path, exist_ok=True)
            
        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.ytdl_hook],
            'noplaylist': not is_playlist,
        }
        
        # Quality & Format mapping
        if is_mp3:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            if quality == '1080p':
                ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
            elif quality == '720p':
                ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
            elif quality == '480p':
                ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
            else:
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                
        if lang:
            ydl_opts['match_filter'] = lambda info: None # placeholder or language filter options
            
        try:
            self.log_message(f"Bağlantı işleniyor (Playlist: {'Evet' > is_playlist else 'Hayır'})...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.log_message("🎉 İndirme başarıyla tamamlandı! 'Download' klasörüne kaydedildi.")
        except Exception as e:
            self.log_message(f"❌ Hata: {str(e)}")
        finally:
            Clock.schedule_once(lambda dt: setattr(self.download_btn, 'disabled', False))

    def ytdl_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            self.log_message(f"İndiriliyor: %{percent} | Hız: {speed} | Kalan Süre: {eta}")

if __name__ == '__main__':
    AslanVideoDownloaderApp().run()
