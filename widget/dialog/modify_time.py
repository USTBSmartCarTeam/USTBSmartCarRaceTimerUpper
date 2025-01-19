""" 调整剩余时间对话窗口 """
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QDialog, QFormLayout, QSpinBox

from widget.common import *


class ModifyTimeDialog(QDialog):
    setting_saved = Signal()

    def __init__(self, team):
        super().__init__()
        self.setWindowTitle("修改剩余时间")
        self.team = team

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignCenter)

        # 比赛阶段
        self.modify_phase = create_combo_box(["赛前准备阶段", "正式比赛阶段"], team["比赛阶段"])
        form_layout.addRow(QLabel("比赛阶段:"), self.modify_phase)

        # 剩余时间
        self.modify_remaining_time = create_spin_box(QSpinBox, min_value=0, current_value=team["剩余时间"],
                                                     suffix=" 秒")
        form_layout.addRow(QLabel("剩余时间:"), self.modify_remaining_time)

        # 添加保存和取消按钮
        self.submit_button = QPushButton("保存", self)
        self.submit_button.clicked.connect(self.save_data)
        self.cancel_button = QPushButton("取消", self)
        self.cancel_button.clicked.connect(self.close)
        form_layout.addRow(self.submit_button, self.cancel_button)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def save_data(self):
        self.team["比赛阶段"] = self.modify_phase.currentText()
        self.team["剩余时间"] = self.modify_remaining_time.value()
        self.setting_saved.emit()
        self.accept()
