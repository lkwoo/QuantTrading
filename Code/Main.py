import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *
from urllib3 import add_stderr_logger
import MyQuant as mq

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_size()        
        self.set_ui()        

        self.add_log(mq.baa_update_data()) 
        self.setWindowTitle("Quant Trade Helper")
        self.setGeometry(self.w_x, self.w_y, self.w_width, self.w_height) # x, y, width, height
        
        date = mq.get_today()
        self.log_momentum_score_etfs(date)        
        etfs = self.BAA(date)
        self.add_log("[Date] " + date)        
        self.add_log("\r\nBAA sell info")
        
        for etf in etfs:
            self.add_log("  [ETF] " + str(etf[0]) + ", [Momemtum] " + str(etf[1]))
        
    def set_size(self):
        self.w_bound = 10
        self.w_width = 800
        self.w_height = 600
        self.w_x = 100
        self.w_y = 100
        self.t_height = 500
        self.t_width = 780
        self.log_w = 580
        self.log_h = 720

    def set_ui(self):
        btn_baag4 = QPushButton("BAA", self)  # BAA Strategy
        btn_baag4.move(self.w_bound, self.w_bound)
        btn_baag4.clicked.connect(self.btn_pass)
        
        btn_log_clear = QPushButton("Clear", self) # log clear
        btn_log_clear.move(self.w_width - self.w_bound - btn_baag4.width(), self.w_bound)
        btn_log_clear.clicked.connect(self.log_clear)
        
        self.label_log = QLabel("Log", self)
        self.label_log.move(self.w_bound, self.w_bound * 5)
        self.text_edit = QTextEdit(self)  # log
        self.text_edit.setGeometry(self.w_bound, self.w_bound * 2 + self.label_log.y() + 5, self.t_width, self.t_height)     
        
    
    def btn_stock_list(self):
        self.add_log("[종목 수] KOSPI : " + '0' + ", KOSDAQ : " + '0')

    def btn_pass(self):
        pass

    def add_log(self, log):
        self.text_edit.append(log)

    def log_clear(self):
        self.text_edit.clear()    

    def log_momentum_score_etfs(self, date = mq.get_today()):
        canary = ['SPY', 'VWO', 'VEA', 'BND']
        offensive = ['QQQ', 'VWO', 'VEA', 'BND', 'EFA', 'EEM', 'AGG']
        defensive = ['TIP', 'DBC', 'BIL', 'IEF', 'TLT', 'LQD', 'BND']                
        
        list_can = []
        list_off = []
        list_def = []        

        for etf in canary:
            list_can.append([etf, mq.get_13612W_momentum_score(etf, date)])                                        
        for etf in offensive:
            list_off.append([etf, mq.get_SMA12M(etf, date)])        
        for etf in defensive:
            list_def.append([etf, mq.get_SMA12M(etf, date)])
        
        list_can.sort(key = lambda x : x[1], reverse= True)
        list_off.sort(key = lambda x : x[1], reverse= True)
        list_def.sort(key = lambda x : x[1], reverse= True)
        
        self.add_log("[Canary] - 13612W")
        for etf in list_can:
            self.add_log("  " + etf[0] + ": " + str(round(etf[1], 3)))
        
        self.add_log("[Offensive] - SMA12M")
        for etf in list_off:
            self.add_log("  " + etf[0] + ": " + str(round(etf[1], 3)))

        self.add_log("[Defensive] - SMA12M")
        for etf in list_def:
            self.add_log("  " + etf[0] + ": " + str(round(etf[1], 3)))
        

    def BAA(self, date = mq.get_today()):
        mq.baa_update_data()
        offensive = ['QQQ', 'VWO', 'VEA', 'BND', 'EFA', 'EEM', 'AGG']
        defensive = ['TIP', 'DBC', 'BIL', 'IEF', 'TLT', 'LQD', 'BND']
        canary = ['SPY', 'VWO', 'VEA', 'BND']
        
        state = "offensive"
        for etf in canary:                        
            if mq.get_13612W_momentum_score(etf, date) < 0:
                state = "defensive"
                
        if state == "offensive":
            ret = []
            etf = offensive[0]
            mmt = mq.get_SMA12M(offensive[0], date)
            for tmp_etf in offensive:                                
                if mq.get_SMA12M(tmp_etf, date) > mmt:
                    etf = tmp_etf
                    mmt = mq.get_SMA12M(tmp_etf, date)                
            ret.append([etf, mmt])
            return ret
        else:
            decs = []
            for etf in defensive:
                decs.append([mq.get_SMA12M(etf, date), etf])
            decs.sort(reverse=True)            
            decs = decs[:3]
        
            top3 = []
            for i, e in decs:
                top3.append([e, i])
                if e == "BIL":
                    break
            
            return top3


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()