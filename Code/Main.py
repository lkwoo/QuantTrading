import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_size()        
        self.set_ui()        

        self.add_log("wait for login...") 
        self.setWindowTitle("Quant Trade Helper")
        self.setGeometry(self.w_x, self.w_y, self.w_width, self.w_height) # x, y, width, height
        
    def set_size(self):
        self.w_bound = 10
        self.w_width = 1200
        self.w_height = 800
        self.w_x = 100
        self.w_y = 100
        self.t_height = 120
        self.t_width = 480

    def set_ui(self):
        btn_get_account = QPushButton("Acnt Check", self)
        btn_get_account.move(self.w_bound, self.w_bound)

        btn_stock_recommand_0 = QPushButton("Stock List", self)
        btn_stock_recommand_0.move(btn_get_account.x() + btn_get_account.width() + self.w_bound, self.w_bound)
        btn_stock_recommand_0.clicked.connect(self.btn_stock_list)
        
        btn_test = QPushButton("Test", self)
        btn_test.move(btn_stock_recommand_0.x() + btn_stock_recommand_0.width() + self.w_bound, self.w_bound)
        btn_test.clicked.connect(self.btn_test)

        self.label_list = QLabel("List", self)
        self.label_list.move(self.w_bound, self.w_bound * 2 + btn_get_account.height())
        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(self.w_bound, self.w_bound * 2 + self.label_list.y() + 5, self.t_width, 180)
        
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(self.w_bound, self.w_height - self.w_bound - self.t_height, self.t_width, self.t_height)     
        self.label_log = QLabel("Log", self)
        self.label_log.move(self.w_bound, self.text_edit.y() - 25)
    
    def btn_stock_list(self):
        self.add_log("[종목 수] KOSPI : " + '0' + ", KOSDAQ : " + '0')

    def btn_test(self):
        pass

    def add_log(self, log):
        self.text_edit.append(log)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()