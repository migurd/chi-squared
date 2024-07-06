import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QImage
from PyQt5.QtCore import Qt
from agregar_window import AgregarWindow

class MainApp(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Interfaz Responsive")
    self.setGeometry(100, 100, 600, 400)  # Smaller window size

    self.central_widget = QWidget()
    self.setCentralWidget(self.central_widget)

    self.main_layout = QHBoxLayout(self.central_widget)

    # Frame izquierdo
    self.left_frame = QFrame(self)
    self.left_frame.setFrameShape(QFrame.StyledPanel)
    self.left_frame.setMinimumWidth(300)
    self.main_layout.addWidget(self.left_frame)

    self.left_layout = QVBoxLayout(self.left_frame)

    # Imagen circular
    self.img_label = QLabel(self.left_frame)
    self.img_label.setPixmap(self.make_image_circular("img/LogoMechi.png", (300, 300)))
    self.img_label.setAlignment(Qt.AlignCenter)
    self.left_layout.addWidget(self.img_label)

    # Texto
    self.text_label = QLabel("MECHI\nEquipo 4\nInteligencia de Negocios\nDr. Luis Javier Mena Camare", self.left_frame)
    self.text_label.setAlignment(Qt.AlignCenter)
    self.text_label.setStyleSheet("font-size: 16px; margin-top: 20px;")
    self.left_layout.addWidget(self.text_label)

    # Frame derecho
    self.right_frame = QFrame(self)
    self.right_frame.setFrameShape(QFrame.StyledPanel)
    self.right_frame.setMinimumWidth(300)
    self.main_layout.addWidget(self.right_frame)

    self.right_layout = QVBoxLayout(self.right_frame)
    self.right_layout.setAlignment(Qt.AlignCenter)  # Center the buttons
    self.right_layout.setSpacing(10)  # Reduce spacing between buttons

    # Botones
    self.insertar_button = QPushButton("INSERTAR DATOS", self.right_frame)
    self.insertar_button.setMinimumSize(270, 50)  # 90% of 300px width
    self.insertar_button.setStyleSheet("font-size: 20px; background-color: #e0ffe0;")
    self.insertar_button.clicked.connect(self.open_agregar_window)
    self.right_layout.addWidget(self.insertar_button)

    self.importar_button = QPushButton("IMPORTAR DATOS", self.right_frame)
    self.importar_button.setMinimumSize(270, 50)  # 90% of 300px width
    self.importar_button.setStyleSheet("font-size: 20px; background-color: #e0ffe0;")
    self.importar_button.clicked.connect(self.open_agregar_window_and_import_data)
    self.right_layout.addWidget(self.importar_button)

    self.cerrar_button = QPushButton("CERRAR", self.right_frame)
    self.cerrar_button.setMinimumSize(270, 50)  # 90% of 300px width
    self.cerrar_button.setStyleSheet("font-size: 20px; background-color: #ffe0e0;")
    self.cerrar_button.clicked.connect(self.close_app)
    self.right_layout.addWidget(self.cerrar_button)

  def make_image_circular(self, image_path, size):
    img = QImage(image_path)
    img = img.scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)

    output = QImage(size[0], size[1], QImage.Format_ARGB32)
    output.fill(Qt.transparent)

    painter = QPainter(output)
    path = QPainterPath()
    path.addEllipse(0, 0, size[0], size[1])
    painter.setClipPath(path)
    painter.drawImage(0, 0, img)
    painter.end()

    return QPixmap.fromImage(output)

  def open_agregar_window(self):
    self.agregar_window = AgregarWindow()
    self.agregar_window.show()

  def open_agregar_window_and_import_data(self):
    self.agregar_window = AgregarWindow()
    self.agregar_window.show()
    self.agregar_window.import_data()

  def close_app(self):
    self.close()

if __name__ == "__main__":
  app = QApplication(sys.argv)
  main_app = MainApp()
  main_app.show()
  sys.exit(app.exec_())
