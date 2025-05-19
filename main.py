from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
# import classifier
import quotes
import sys
import random
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS  # temp folder created by PyInstaller
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # changing the background color to yellow
        self.setStyleSheet("background-color: black;")

        
        # set the title
        self.setWindowTitle("Ask Flowey")

        # setting  the geometry of window
        self.resize(1400, 900)

        self.center()
        self.secret_count = 0

        QFontDatabase.addApplicationFont(resource_path("fonts/DeterminationSansWebRegular-369X.ttf"))
        self.font = QFont("Determination Sans Web", 24)

        self.classifier = None
        self.loading_label = None
        self.load_classifier_async()
        # self.UiComponents()

        # show all the widgets
        self.show()

    def load_classifier_async(self):
        self.loading_widget = QWidget()
        layout = QVBoxLayout()
        self.loading_widget.setLayout(layout)

        # Create QLabel to show the GIF
        self.loading_gif_label = QLabel()
        self.loading_gif_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)

        # Load and start the GIF
        self.loading_movie = QMovie(resource_path("images/undertale_loading.gif"))  # Replace with your actual path
        self.loading_movie.setScaledSize(QSize(300, 300))  # Optional: resize
        self.loading_gif_label.setMovie(self.loading_movie)
        self.loading_movie.start()

        # Create a text label below the GIF
        self.loading_text = QLabel("* Loading Flowey's thoughts...\n* Please wait...")
        self.loading_text.setStyleSheet("color: white;")
        self.loading_text.setFont(self.font)
        self.loading_text.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        layout.addWidget(self.loading_gif_label)
        layout.addWidget(self.loading_text)

        self.setCentralWidget(self.loading_widget)

        # Start loading in a thread
        self.loader_thread = ClassifierLoader()
        self.loader_thread.loaded.connect(self.on_classifier_loaded)
        self.loader_thread.start()

    def on_classifier_loaded(self, loaded_classifier):
        self.classifier = loaded_classifier

        # Clean up loading widget
        if self.loading_movie:
            self.loading_movie.stop()
        self.loading_widget.deleteLater()

        # Load main UI
        self.UiComponents()

    def UiComponents(self):
        self.central_widget = QStackedWidget(self)
        self.setCentralWidget(self.central_widget)

        self.generate_main_page()
        self.generate_help_page()

        self.central_widget.addWidget(self.main_page)
        self.central_widget.addWidget(self.help_page)
        
    def generate_main_page(self):
        grid = QGridLayout()
        self.header = QVBoxLayout()
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout3 = QHBoxLayout()
        container0 = QWidget()
        container0.setLayout(self.header)
        # container0.setStyleSheet("background-color: red;")
        container1 = QWidget()
        container1.setLayout(self.layout1)
        container2 = QWidget()
        container2.setLayout(self.layout2)
        container2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        container3 = QWidget()
        container3.setLayout(self.layout3)

        # Make the single column stretch to fill width
        grid.setColumnStretch(0, 1)

        # Make rows stretch proportionally (60%, 20%, 20%)
        grid.setRowStretch(0, 1)  # 10%
        grid.setRowStretch(1, 5)  # 50%
        grid.setRowStretch(2, 2)  # 20%
        grid.setRowStretch(3, 2)  # 20%

        grid.addWidget(container0, 0, 0)
        grid.addWidget(container1, 1, 0)
        grid.addWidget(container2, 2, 0)
        grid.addWidget(container3, 3, 0)

        self.help = ClickableLabel()
        self.help.clicked.connect(self.on_main_header_click)
        header_pixmap = QPixmap(resource_path("images/black-questionmark.svg"))
        scaled_header_pixmap = header_pixmap.scaled(50, 50,
            aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.FastTransformation)
        self.help.setPixmap(scaled_header_pixmap)
        self.header.addWidget(self.help, stretch=1, alignment=Qt.AlignLeft | Qt.AlignHCenter)

        self.image = ClickableLabel()
        self.image.clicked.connect(self.on_image_click)
        self.set_new_image(QPixmap(resource_path('images/start.png')))

        self.image.setAlignment(Qt.AlignCenter)
        self.layout1.addWidget(self.image, stretch=6, alignment=Qt.AlignBottom | Qt.AlignHCenter)

        self.set_new_label("* Howdy!\n* I'm FLOWEY. \n* FLOWEY the FLOWER!")

        self.my_line_edit = QLineEdit()
        self.my_line_edit.setPlaceholderText("Tell something to Flowey...")

        self.my_line_edit.setMaximumWidth(800)
        self.my_line_edit.setFixedHeight(80)
        self.my_line_edit.setFont(self.font)
        self.my_line_edit.setStyleSheet("color: white;")
        self.layout3.addWidget(self.my_line_edit)
        self.my_line_edit.returnPressed.connect(self.submit)

        self.main_page = QWidget()
        self.main_page.setLayout(grid)

    def generate_help_page(self):
        self.help_page = QWidget()

        grid = QGridLayout()
        self.help_header = QVBoxLayout()
        self.help_layout1 = QVBoxLayout()

        help_container0 = QWidget()
        help_container0.setLayout(self.help_header)
        # # container0.setStyleSheet("background-color: red;")
        help_container1 = QWidget()
        help_container1.setLayout(self.help_layout1)

        # # Make the single column stretch to fill width
        grid.setColumnStretch(0, 1)

        # # Make rows stretch proportionally (60%, 20%, 20%)
        grid.setRowStretch(0, 1)  # 10%
        grid.setRowStretch(1, 9)  # 50%

        grid.addWidget(help_container0, 0, 0)
        grid.addWidget(help_container1, 1, 0)

        self.help_back = ClickableLabel()
        self.help_back.clicked.connect(self.on_help_header_click)
        header_pixmap = QPixmap(resource_path("images/black-questionmark.svg"))
        scaled_header_pixmap = header_pixmap.scaled(50, 50,
            aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.FastTransformation)
        self.help_back.setPixmap(scaled_header_pixmap)
        self.help_header.addWidget(self.help_back, stretch=1, alignment=Qt.AlignLeft | Qt.AlignHCenter)

        self.help_page = QWidget()
        # self.help_page.setStyleSheet("background-color: red;")
        self.help_page.setLayout(grid)

        self.help_label = QLabel()
        self.help_label.setText("* HOWDY! Welcome to the Help Page. \n \n* Flowey understands the sentiment behind your words... \nTry saying something *nice*... or something *nasty*. He likes both.\n\n* Flowey knows alllll about those other Underground weirdos. \nAsk what he thinks of Sans, Toriel... any of them. He won't hold back. \n \n* And hey... only TRUE heroes can take Flowey down. \n Try attacking—or clicking—if you think you've got what it takes.")
        self.help_label.setStyleSheet("color: white;")
        self.help_label.setFont(self.font)
        self.help_label.setMaximumWidth(int(self.width()*0.8))
        self.help_label.setMinimumWidth(int(self.width()*0.8))
        self.help_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.help_label.setWordWrap(True)
        self.help_layout1.addWidget(self.help_label, stretch=2, alignment=Qt.AlignTop | Qt.AlignHCenter)

    def on_help_header_click(self):
        # self.set_new_image(QPixmap('images/start.png'))
        # self.set_new_label("* Howdy!\n* I'm FLOWEY. \n* FLOWEY the FLOWER!")
        self.central_widget.setCurrentIndex(0)

    def on_main_header_click(self):
        self.label.stop()
        self.central_widget.setCurrentIndex(1)

    def on_image_click(self):
        match self.secret_count:
            case 0:
                self.set_new_image(QPixmap(resource_path('images/secret1.png')))
                self.set_new_label(quotes.secret_1)
                self.secret_count = 1
            case 1:
                self.set_new_image(QPixmap(resource_path('images/secret2.png')))
                self.set_new_label(quotes.secret_2)
                self.secret_count = 2
            case 2:
                self.set_new_image(QPixmap(resource_path('images/secret3.png')))
                self.set_new_label(quotes.secret_3)
                self.secret_count = 3
            case 3:
                self.set_new_image(QPixmap(resource_path('images/secret4.png')))
                self.set_new_label(self.rand_dialogue(quotes.secret_4))
                self.secret_count = 4
            case 4:
                self.set_new_image(QPixmap(resource_path('images/secret5.png')))
                self.set_new_label(self.rand_dialogue(quotes.secret_5))
                self.secret_count = 5
            case 5:
                self.set_new_image(QPixmap(resource_path('images/secret6.png')))
                self.set_new_label(self.rand_dialogue(quotes.secret_6))
                self.secret_count = 6
            case _:
                self.set_new_image(QPixmap(resource_path(self.get_rand_secr_rep_image())))
                self.set_new_label(self.rand_dialogue(quotes.secret_repeat))
                
    def set_new_label(self, text):
        if hasattr(self, 'label') and isinstance(self.label, TypewriterLabel):
            self.label.stop()
            self.layout2.removeWidget(self.label)
            self.label.deleteLater()  # Clean up the old label
        self.label = TypewriterLabel(text, sound_path=resource_path("sounds/voice_flowey_1.wav"), delay=50)
        self.label.setStyleSheet("color: white;")
        self.label.setFont(self.font)
        self.label.setMaximumWidth(int(self.width()*0.8))
        self.label.setMinimumWidth(int(self.width()*0.8))
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.label.setWordWrap(True)
        self.layout2.addWidget(self.label, stretch=2, alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.label.start()

    def set_new_image(self, pixmap):
        new_pixmap = pixmap
        scaled_pixmap = new_pixmap.scaled(400, 400, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.FastTransformation)
        self.image.setPixmap(scaled_pixmap)
        
    def rand_dialogue(self, options):
        res = ""
        while res == self.label.text() or res == "":
            length = len(options)
            rand = random.randint(1, length)-1
            res = options[rand]

        return res

    def submit(self):
        text = self.my_line_edit.text()
        if text != "":
            if self.secret_count > 3 and self.secret_count != 6:
                self.secret_count = 6
            if self.secret_count > 0 and self.secret_count < 4:
                self.secret_count = 0

            
            quote = self.ret_und_char_quote(text)
            if self.analyze_text(text) == 1:
                self.set_new_image(QPixmap(resource_path(self.get_rand_pos_image())))
                if quote == "":
                    self.set_new_label(self.rand_dialogue(quotes.positive_quotes))
                else:
                    self.set_new_label(quote)
            elif self.analyze_text(text) == -1:
                self.set_new_image(QPixmap(resource_path(self.get_rand_neg_image())))
                if quote == "":
                    self.set_new_label(self.rand_dialogue(quotes.negative_quotes))
                else:
                    self.set_new_label(quote)
            else:
                self.set_new_image(QPixmap(resource_path(self.get_rand_neut_image())))
                if quote == "":
                    self.set_new_label(self.rand_dialogue(quotes.neutral_quotes))
                else:
                    self.set_new_label(quote)

            self.my_line_edit.clear()

    def ret_und_char_quote(self, text):
        characters = ["Sans", "Papyrus", "Toriel", "Asgore", 
                      "Alphys", "Undyne", "Mettaton", "Asriel",
                      "Frisk", "Chara", "Napstablook", "Muffet",
                      "Temmie", "Kid", "Burgerpants", "Gaster",
                      "River", "Grillby", "Bratty", "Dog",
                      "Player"]
        for char in characters:
            if char.lower() in text.lower():
                return getattr(quotes, char)
            
        return ""
        

    def analyze_text(self, text):
        res = self.classifier.analyze_sentiment(text)[0][0]
        if res == 'positive':
            return 1
        elif res == 'negative':
            return -1
        else: 
            return 0
    
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def get_rand_pos_image(self):
        rand = random.randint(1, 4)
        return "images/positive"+str(rand)+".png"
    
    def get_rand_neg_image(self):
        rand = random.randint(1, 9)
        return "images/negative"+str(rand)+".png"
    
    def get_rand_neut_image(self):
        rand = random.randint(1, 7)
        return "images/neutral"+str(rand)+".png"
    
    def get_rand_secr_rep_image(self):
        rand = random.randint(1, 3)
        return "images/neutral"+str(rand)+".png"

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

class TypewriterLabel(QLabel):
    def __init__(self, full_text, sound_path=None, delay=50, parent=None):
        super().__init__(parent)
        self.full_text = full_text
        self.current_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.delay = delay  # milliseconds
        if sound_path:
            self.sound = QSoundEffect(self)
            self.sound.setSource(QUrl.fromLocalFile(sound_path))
            self.sound.setVolume(0.1)  # Volume range: 0.0 to 1.0
        else:
            self.sound = None

    def start(self):
        self.setText("")
        self.current_index = 0
        self.timer.start(self.delay)

    def stop(self):
        self.timer.stop()

    def update_text(self):
        if self.current_index < len(self.full_text):
            self.setText(self.text() + self.full_text[self.current_index])
            self.current_index += 1
            if self.sound:
                self.sound.play()
        else:
            self.timer.stop()

class ClassifierLoader(QThread):
    loaded = pyqtSignal(object)

    def run(self):
        import classifier  # This imports your heavy model
        self.loaded.emit(classifier)

# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())

# app = QApplication([])
# app.setStyle('Fusion')
# app.set

# palette = QPalette()
# palette.setColor(QPalette.ButtonText, Qt.red)
# app.setPalette(palette)

# window = QWidget()
# layout = QVBoxLayout()
# layout.addWidget(QLabel('Hello World!'))
# layout.addWidget(QPushButton('Bottom'))
# window.setLayout(layout)
# window.show()
# app.exec()