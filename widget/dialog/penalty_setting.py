""" 罚时设置对话窗口 """

from copy import deepcopy

import pandas as pd
from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QDialog, \
    QMessageBox, QFileDialog, QSpinBox, QScrollArea, QHBoxLayout, \
    QSpacerItem, QSizePolicy, QGridLayout, QToolButton

from widget.common import *


class PenaltySettingDialog(QDialog):
    setting_saved = pyqtSignal()

    def __init__(self, configuration):
        super().__init__()
        self.setWindowTitle("罚时设置")
        self.configuration = configuration
        self.penalties = deepcopy(configuration["罚时种类"])

        # 创建布局
        layout = QVBoxLayout()

        # 导入按钮
        self.import_button = QPushButton("导入罚时种类")
        self.import_button.clicked.connect(self.import_penalties)
        layout.addWidget(self.import_button)

        # 滚动区域
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        # 显示区域
        penalty_widget = QWidget()
        self.penalty_layout = QGridLayout(penalty_widget)
        self.scroll_area.setWidget(penalty_widget)

        # 添加保存和取消按钮
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("保存", self)
        self.submit_button.clicked.connect(self.save_data)
        button_layout.addWidget(self.submit_button)
        self.cancel_button = QPushButton("取消", self)
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.fixed_layout()

        self.update_penalty_list()

    def import_penalties(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "导入罚时种类",
            "",
            "Excel Files (*.xls *.xlsx);;All Files (*)"
        )

        if file_name:
            try:
                df = pd.read_excel(file_name)

                penalties_list = []  # 读入的罚时种类
                invalid_rows = []  # 用于记录无效行的索引

                for index, row in df.iterrows():
                    penalty_type = row[0]  # 第一列
                    penalty_duration = row[1]  # 第二列

                    # 类型检查
                    if isinstance(penalty_type, str) and isinstance(penalty_duration, (int, float)):
                        penalties_list.append((penalty_type, int(penalty_duration)))  # 将有效元组添加到列表中
                    else:
                        invalid_rows.append(index + 1)  # 记录无效行的行号（+1 以符合 Excel 行号）

                # 合并罚时种类
                for new_penalty, new_duration in penalties_list:
                    found = False
                    for index, (penalty, duration) in enumerate(self.penalties):
                        if new_penalty == penalty:
                            self.penalties[index] = (penalty, new_duration)
                            found = True
                            break
                    if not found:
                        self.penalties.append((new_penalty, new_duration))

                # 存在无效行
                if invalid_rows:
                    invalid_rows_str = ', '.join(map(str, invalid_rows))
                    QMessageBox.warning(self, "警告", f"以下行的数据不符合格式：{invalid_rows_str}。请检查并重新导入。")

            except Exception as e:
                QMessageBox.critical(self, "错误", f"读取文件时出错：{e}")

    def update_penalty_list(self):
        # 清除罚时面板中的所有控件
        for i in reversed(range(self.penalty_layout.count())):
            item = self.penalty_layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not self.penalties:
            spacer_top = QSpacerItem(0, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.penalty_layout.addItem(spacer_top, 0, 0, 1, 2)

            empty_label = create_label("罚时种类为空，请手动导入！")
            self.penalty_layout.addWidget(empty_label, 1, 0, 1, 2)

            spacer_bottom = QSpacerItem(0, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.penalty_layout.addItem(spacer_bottom, 2, 0, 1, 2)
        else:
            type_label = create_label("罚时种类")
            self.penalty_layout.addWidget(type_label, 0, 0)

            duration_label = create_label("时长")
            self.penalty_layout.addWidget(duration_label, 0, 1)

            button_size = QSize(20, 20)
            for number, (penalty_type, penalty_duration) in enumerate(self.penalties):
                set_type = create_line_edit(text=penalty_type, alignment=Qt.AlignmentFlag.AlignCenter)
                set_type.editingFinished.connect(
                    lambda line_edit=set_type, n=number: self.update_penalty_text(n, line_edit))
                self.penalty_layout.addWidget(set_type, number + 1, 0)

                set_duration = create_spin_box(QSpinBox, min_value=-32768, max_value=32767,
                                               current_value=penalty_duration, suffix=" 秒",
                                               alignment=Qt.AlignmentFlag.AlignCenter)
                set_duration.editingFinished.connect(
                    lambda spinbox=set_duration, n=number: self.update_penalty_duration(n, spinbox))
                self.penalty_layout.addWidget(set_duration, number + 1, 1)

                remove_button = QToolButton()
                remove_button.setText("-")
                remove_button.setFixedSize(button_size)
                remove_button.clicked.connect(lambda _, n=number: self.remove_penalty(n))
                self.penalty_layout.addWidget(remove_button, number + 1, 2)

            add_type = create_line_edit(alignment=Qt.AlignmentFlag.AlignCenter)
            self.penalty_layout.addWidget(add_type, len(self.penalties) + 1, 0)

            add_duration = create_spin_box(QSpinBox, min_value=-32768, max_value=32767, suffix=" 秒",
                                           alignment=Qt.AlignmentFlag.AlignCenter)
            self.penalty_layout.addWidget(add_duration, len(self.penalties) + 1, 1)

            add_button = QToolButton()
            add_button.setText("+")
            add_button.setFixedSize(button_size)
            add_button.clicked.connect(lambda: self.add_penalty(add_type.text(), add_duration.value()))
            self.penalty_layout.addWidget(add_button, len(self.penalties) + 1, 2)

            self.fixed_layout()

    def fixed_layout(self):
        total_rows = 4
        total_columns = 3

        for row in range(total_rows):
            for column in range(total_columns):
                if self.penalty_layout.itemAtPosition(row, column) is None:
                    placeholder = QWidget()
                    placeholder.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    self.penalty_layout.addWidget(placeholder, row, column)

    def remove_penalty(self, penalty_id):
        if 0 <= penalty_id < len(self.penalties):
            del self.penalties[penalty_id]
            self.update_penalty_list()

    def add_penalty(self, text, value):
        if text and value != 0:
            for penalty, _ in self.penalties:
                if penalty == text:
                    QMessageBox.warning(self, "警告", "已存在同名的罚时种类！")
                    return
            self.penalties.append((text, value))
            self.update_penalty_list()
        else:
            QMessageBox.warning(self, "警告", "罚时种类为空或罚时时长为0！")

    def update_penalty_text(self, penalty_id, line_edit):
        if 0 <= penalty_id < len(self.penalties):
            self.penalties[penalty_id] = (line_edit.text(), self.penalties[penalty_id][1])

    def update_penalty_duration(self, penalty_id, spinbox):
        if 0 <= penalty_id < len(self.penalties):
            self.penalties[penalty_id] = (self.penalties[penalty_id][0], spinbox.value())

    def save_data(self):
        self.configuration["罚时种类"] = self.penalties
        self.setting_saved.emit()
        self.accept()  # 关闭对话框