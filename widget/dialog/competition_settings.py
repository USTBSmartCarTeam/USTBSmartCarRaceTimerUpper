""" 比赛设置对话窗口 """

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QDialog, QFormLayout

from widget.common import *


class CompetitionSettingDialog(QDialog):
    setting_saved = Signal()

    def __init__(self, configuration):
        super().__init__()
        self.setWindowTitle("比赛设置")
        self.configuration = configuration

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignCenter)

        # 比赛名称
        self.set_title = create_line_edit(self.configuration["比赛名称"])
        form_layout.addRow(QLabel("比赛名称:"), self.set_title)

        # 比赛阶段
        self.set_stage = create_line_edit(self.configuration["比赛阶段"])
        form_layout.addRow(QLabel("比赛阶段:"), self.set_stage)

        # 比赛组别
        self.set_category = create_line_edit(self.configuration["比赛组别"])
        form_layout.addRow(QLabel("比赛组别:"), self.set_category)

        # 保存与取消按钮
        self.submit_button = QPushButton("保存", self)
        self.submit_button.clicked.connect(self.save_data)
        self.cancel_button = QPushButton("取消", self)
        self.cancel_button.clicked.connect(self.close)
        form_layout.addRow(self.submit_button, self.cancel_button)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def save_data(self):
        self.configuration["比赛名称"] = self.set_title.text()
        self.configuration["比赛阶段"] = self.set_stage.text()
        self.configuration["比赛组别"] = self.set_category.text()
        self.setting_saved.emit()
        self.accept()
