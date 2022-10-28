import glob
import sys
import os
import os.path as osp
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player")
        WINDOW_SIZE = (1600, 900)
        self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1]+100)

        self.mediaPlayers = []
        self.videoItems = []
        self.scenes = []
        self.views = []

        for i in range(4):
            self.mediaPlayers.append(QMediaPlayer(None, QMediaPlayer.VideoSurface))
            self.mediaPlayers[i].setVolume(0)
            self.videoItems.append(QGraphicsVideoItem())
            self.videoItems[i].setSize(QSizeF(int(WINDOW_SIZE[0]/2.5), int(WINDOW_SIZE[1]/2.5)))
            self.scenes.append(QGraphicsScene(self))
            self.views.append(QGraphicsView(self.scenes[i]))
            self.scenes[i].addItem(self.videoItems[i])
        
        self.openButton = QPushButton('Open Video Folder')
        self.openButton.clicked.connect(self.openFile)
        self.openfolderShortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.openfolderShortcut.activated.connect(self.openFile)

        self.playButton = QPushButton()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.playVideo)
        playShortcut = QShortcut(QKeySequence("Space"), self)
        playShortcut.activated.connect(self.playVideo)


        widget = QWidget(self)
        self.setCentralWidget(widget)
        self.window_layout = QGridLayout()

        for i, view in enumerate(self.views):
            self.window_layout.addWidget(view, i//2, i%2)

        self.window_layout.addWidget(self.openButton, 2, 0)
        self.window_layout.addWidget(self.playButton, 2, 1)
        widget.setLayout(self.window_layout)            

        for i, mediaPlayer in enumerate(self.mediaPlayers):
            mediaPlayer.setVideoOutput(self.videoItems[i])

        for mediaPleyer in self.mediaPlayers:
            mediaPleyer.error.connect(self.handleError)

        self.show()
    
    def openFile(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open Video Folder", os.getenv('HOME'))
        if folder_path != '':
            video_paths =  glob.glob(osp.join(folder_path, '*.mp4'))
            for i, video_path in enumerate(video_paths):
                self.mediaPlayers[i].setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))

    def playVideo(self):
        for mediaPlayer in self.mediaPlayers:
            if mediaPlayer.state() == QMediaPlayer.PlayingState:
                mediaPlayer.pause()
            else:
                mediaPlayer.play()

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayers[0].errorString())

if '__main__' == __name__:
    app = QApplication(sys.argv)
    player = Window()
    sys.exit(app.exec_())