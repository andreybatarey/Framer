import cv2
import pathlib as p
import os
import moviepy as mv
import logging
logger = logging.getLogger(__name__)


class Framer:
    def dannie(self, infolder_path, outfolder_path, soundfolder_path, fos):
        self.infolder_path = p.Path(infolder_path)
        self.outfolder_path = p.Path(outfolder_path)
        self.soundfolder_path = p.Path(soundfolder_path)
        self.fos = fos  # Store the frame rate parameter

    def imena(self):  # получение имен файлов
        self.files = [f for f in self.infolder_path.iterdir() if f.is_file()]  # Проверяем это файл или нет

    def extract_audio(self, video_path, audio_name):
        """Получаем аудио"""
        vid = mv.VideoFileClip(video_path)
        audio = vid.audio
        audio_path = self.soundfolder_path / audio_name
        audio.write_audiofile(str(audio_path), codec='pcm_s16le')  # Сохраняем как wav
        audio.close()
        vid.close()

    def take_screenshots(self, video_path):
        """Скриншотим."""
        vid_cv = cv2.VideoCapture(video_path)
        fps = vid_cv.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps / self.fos)
        frame_count = 0
        screenshot_count = 0

        while True:
            ret, frame = vid_cv.read()
            if not ret:
                break
            if frame_count % frame_interval == 0:
                scrin_name = os.path.join(self.outfolder_path, f"{screenshot_count}.jpg")
                cv2.imwrite(scrin_name, frame)
                screenshot_count += 1

            frame_count += 1

        vid_cv.release()
        cv2.destroyAllWindows()

    def process_files(self):
        """Главный метод"""
        if not self.files:
            logger.info("Папка пуста. Завершение программы.")
            return

        has_video = any(f.suffix in ['.mp4', '.avi', '.mov'] for f in self.files)
        has_image = any(f.suffix in ['.jpg', '.jpeg', '.png'] for f in self.files)

        if has_image:
            # Перемещение файлов в выходную папку
            for f in self.files:
                if f.suffix in ['.jpg', '.jpeg', '.png']:
                    target_path = self.outfolder_path / f.name
                    p.Path(f).rename(target_path)
            logger.info("Все изображения перемещены в папку вывода.")

        if has_video:

            for f in self.files:
                if f.suffix in ['.mp4', '.avi', '.mov']:
                    video_path = str(f)
                    audio_name = f"{f.stem}.wav"  # Использование названия видео, для названия аудиофайла
                    self.extract_audio(video_path, audio_name)
                    self.take_screenshots(video_path)
            logger.info("Аудио и скриншоты извлечены из видео.")

        if not has_image and not has_video:
            logger.info("В папке нет ни изображений, ни видео. Завершение программы.")



framer_instance = Framer()


framer_instance.dannie(
    input("Введите путь к папке с файлами: "),
    input("Введите путь к папке с выводом: "),
    input("Введите путь к папке со звуком: "),
    int(input("Введите частоту нарезания видео, по умолчанию = 2. Можете ввести два если согласны: "))
)

framer_instance.imena()
framer_instance.process_files()



