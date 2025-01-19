from PySide6.QtGui import QFont, QKeyEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout

from .common import *


class FullScreenWindow(QWidget):
    def __init__(self, configuration, race_data):
        super().__init__()
        self.configuration = configuration
        self.race_data = race_data
        self.initialization = False
        self.setWindowTitle("投屏窗口")

        self.setStyleSheet("""
            QWidget {
                background-color: black;
                color: white;
            }
            QLabel {
                background-color: black;
                color: white;
            } 
        """)

        # 创建主布局
        layout = QVBoxLayout()

        # 设置初始字体大小
        self.fontTitle = QFont()
        self.font = QFont()
        self.fontTitle.setPointSize(15)
        self.font.setPointSize(30)

        # 标题
        self.title = create_label(self.configuration["比赛名称"] + self.configuration["比赛阶段"], font=self.fontTitle,
                                  style="color: #FFD700; font: bold; margin-top: 30px; margin-bottom: 10px;")
        layout.addWidget(self.title)

        self.subheading = create_label(self.configuration["比赛组别"], font=self.font,
                                       style="color: #FFD700; font: bold; margin-top: 10px; margin-bottom: 20px;")
        layout.addWidget(self.subheading)

        # 比赛信息
        grid_layout = QGridLayout()

        progress = create_label("比赛进度", font=self.font)
        grid_layout.addWidget(progress, 0, 0)

        self.progress_display = create_label(font=self.font, style="color: #FFA500;")
        grid_layout.addWidget(self.progress_display, 0, 1)

        next_team = create_label("下支队伍", font=self.font)
        grid_layout.addWidget(next_team, 0, 2)

        self.next_team_display = create_label(font=self.font, style="color: #FFA500;")
        grid_layout.addWidget(self.next_team_display, 0, 3)

        team_id = create_label("队伍号", font=self.font)
        grid_layout.addWidget(team_id, 1, 0)

        self.team_id_display = create_label(font=self.font, style="color: #FFA500;")
        grid_layout.addWidget(self.team_id_display, 1, 1)

        real_time = create_label("实时时间", font=self.font)
        grid_layout.addWidget(real_time, 1, 2)

        self.real_time_display = create_label(font=self.font)
        grid_layout.addWidget(self.real_time_display, 1, 3)

        team_name = create_label("队伍名称", font=self.font)
        grid_layout.addWidget(team_name, 2, 0)

        self.team_name_display = create_label(font=self.font, style="color: #FFA500;")
        grid_layout.addWidget(self.team_name_display, 2, 1)

        best_record = create_label("最好成绩", font=self.font)
        grid_layout.addWidget(best_record, 2, 2)

        self.best_record_display = create_label(font=self.font, style="color: #FF0000;")
        grid_layout.addWidget(self.best_record_display, 2, 3)

        team_members = create_label("队伍成员", font=self.font)
        grid_layout.addWidget(team_members, 3, 0)

        self.team_members_display = create_label(font=self.font, style="color: #FFA500;")
        grid_layout.addWidget(self.team_members_display, 3, 1)

        remaining_time = create_label("剩余时间", font=self.font)
        grid_layout.addWidget(remaining_time, 3, 2)

        self.remaining_time_display = create_label(font=self.font)
        grid_layout.addWidget(self.remaining_time_display, 3, 3)

        # 设置行高均匀分布
        column_count = grid_layout.columnCount()
        for i in range(column_count):
            grid_layout.setRowStretch(i, 1)

        layout.addLayout(grid_layout)

        # 提示
        attention = create_label(">>>>>>>>>>  北科大智能车队提醒您，冷静发车，赛出实力！ <<<<<<<<<<", font=self.font,
                                 style="color: #FFFF00; font: bold; margin-top: 30px; margin-bottom: 30px;")
        layout.addWidget(attention)

        self.setLayout(layout)
        self.initialization = True

    def resizeEvent(self, event):
        width = self.width()
        new_font_size = max(10, width // 30)
        self.font.setPointSize(new_font_size)
        self.title.setFont(self.font)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
