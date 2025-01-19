""" 计时设置对话窗口 """

from PySide6.QtWidgets import QVBoxLayout, QDialog, QMessageBox, QFormLayout, QSpinBox, QCheckBox

from widget.common import *


class TimerSettingDialog(QDialog):
    def __init__(self, configuration, progress):
        super().__init__()
        self.setWindowTitle("计时设置")
        self.configuration = configuration
        self.progress = progress

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignCenter)

        # 速度计算
        self.set_speed_calculation = QCheckBox()
        self.set_speed_calculation.setText("速度计算")
        self.set_speed_calculation.setChecked(self.configuration["速度计算"])
        layout.addWidget(self.set_speed_calculation)

        # 赛道长度
        self.set_length = create_spin_box(QDoubleSpinBox, min_value=0, current_value=self.configuration["赛道长度"],
                                          single_step=0.1, decimals=1, suffix=" 米")
        form_layout.addRow(QLabel("赛道长度:"), self.set_length)

        # 赛前准备时间
        self.set_preparation_time = create_spin_box(QSpinBox, min_value=0, max_value=65535,
                                                    current_value=self.configuration["赛前准备时间"], suffix=" 米")
        form_layout.addRow(QLabel("赛前准备时间:"), self.set_preparation_time)

        # 比赛时间
        self.set_competition_time = create_spin_box(QSpinBox, min_value=0, max_value=65535,
                                                    current_value=self.configuration["比赛时间"], suffix=" 秒")
        form_layout.addRow(QLabel("比赛时间:"), self.set_competition_time)

        # 保存与取消
        self.submit_button = QPushButton("保存", self)
        self.submit_button.clicked.connect(self.save_data)
        self.cancel_button = QPushButton("取消", self)
        self.cancel_button.clicked.connect(self.close)
        form_layout.addRow(self.submit_button, self.cancel_button)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def save_data(self):
        if self.progress > 0:
            QMessageBox.warning(self, "警告", "当前比赛已开始，不能再修改计时设置！")
        else:
            self.configuration["速度计算"] = self.set_speed_calculation.isChecked()
            self.configuration["赛道长度"] = self.set_length.value()
            self.configuration["赛前准备时间"] = self.set_preparation_time.value()
            self.configuration["比赛时间"] = self.set_competition_time.value()
            self.accept()  # 关闭对话框