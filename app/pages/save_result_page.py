from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class SaveResultPage(QWidget):
    create_next_same_context_requested = Signal()
    create_next_same_subject_requested = Signal()
    go_home_requested = Signal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.label = QLabel("保存しました")

        same_context_button = QPushButton("同じ条件で次を作成")
        same_subject_button = QPushButton("同じ個体で次を作成")
        home_button = QPushButton("ホームへ戻る")

        same_context_button.clicked.connect(self.create_next_same_context_requested.emit)
        same_subject_button.clicked.connect(self.create_next_same_subject_requested.emit)
        home_button.clicked.connect(self.go_home_requested.emit)

        layout.addWidget(self.label)
        layout.addWidget(same_context_button)
        layout.addWidget(same_subject_button)
        layout.addWidget(home_button)
        layout.addStretch()

    def set_saved_path(self, path: str):
        self.label.setText(f"保存しました\n{path}")
