from PyQt5.QtWidgets import QApplication, QFileDialog, QGraphicsScene, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from select_img_gui import Imagemain
import shutil
import sys,os
import cv2
from PyQt5.QtWidgets import QMessageBox, QGraphicsView,QApplication, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import QPoint
class Select(Imagemain):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.image_dir = ""
        self.label_dir = ""
        self.img_list = []
        self.image_count = 0
        self.img_end = ["jpg", "JPG", "jpeg", "JPEG", "png", "PNG", "bmp", "BMP"]
        self.move_idx_list = []
        self.openimgdir.clicked.connect(self.openimgdirfn)
        self.openlabeldir.clicked.connect(self.openlabeldirfn)
        self.btn_before.clicked.connect(self.image_before)
        self.btn_next.clicked.connect(self.image_next)
        self.btn_moveimg.clicked.connect(self.moveimgfn)

        self.image_idx = 0

        # 使用graphicsView显示图片
        self.graphicsView.setRenderHint(QPainter.Antialiasing)
        self.graphicsView.setDragMode(QGraphicsView.RubberBandDrag)  # 设置图元的拖动属性
        self.graphicsView.setAcceptDrops(True)  # 此窗口小部件启用了放置事件
        self.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
        self.zoomscale = 1  # 图片放缩尺度
        self.scene = QGraphicsScene()  # 创建画布
        self.graphicsView.setScene(self.scene)  # 把画布添加到窗口
        self.graphicsView.show()

        self.show()

    def image_before(self):
        if self.image_dir == "":
            reply = QMessageBox(QMessageBox.Question, self.tr("提示"), self.tr("请选择图片所在路径,路径中不允许有中文!"), QMessageBox.NoButton, self)
            yr_btn = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
            reply.exec_()
            if reply.clickedButton() == yr_btn:
                self.openimgdirfn()
        else:
            if self.image_idx-1 < 0:
                self.image_idx = 0
            else:
                self.image_idx = self.image_idx - 1
            self.imgshow()
    
    def image_next(self):
        if self.image_dir == "":
            reply = QMessageBox(QMessageBox.Question, self.tr("提示"), self.tr("请选择图片所在路径,路径中不允许有中文!"), QMessageBox.NoButton, self)
            yr_btn = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
            reply.exec_()
            if reply.clickedButton() == yr_btn:
                self.openimgdirfn()
        else:
            if self.image_idx +1 > len(self.image_dir)-1:
                self.image_idx = len(self.image_dir)-1
            else:
                self.image_idx = self.image_idx + 1
            self.imgshow()
    
    def moveimgfn(self):
        if self.label_dir == "":
            reply = QMessageBox(QMessageBox.Question, self.tr("提示"), self.tr("请选择筛选后的保存路径,路径中不允许有中文!"), QMessageBox.NoButton, self)
            yr_btn = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
            reply.exec_()
            if reply.clickedButton() == yr_btn:
                self.openlabeldirfn()
        elif self.image_dir == "":
            reply = QMessageBox(QMessageBox.Question, self.tr("提示"), self.tr("请选择图片所在路径,路径中不允许有中文!"), QMessageBox.NoButton, self)
            yr_btn = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
            reply.exec_()
            if reply.clickedButton() == yr_btn:
                self.openimgdirfn()
        elif self.label_dir == self.image_dir:
            reply = QMessageBox(QMessageBox.Question, self.tr("提示"), self.tr("保存路径和图片路径是一样的,请重新选择!"), QMessageBox.NoButton, self)
            yr_btn = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
            reply.exec_()
            if reply.clickedButton() == yr_btn:
                self.openlabeldirfn()
        else:
            shutil.move(os.path.join(self.image_dir,self.img_list[self.image_idx]), self.label_dir)
            self.listWidgetlabel.clear()
            already_exist_lable_list = [item for item in os.listdir(self.label_dir)]
            self.listWidgetlabel.addItems(already_exist_lable_list)
            self.img_list = [item for item in os.listdir(self.image_dir)]
            self.listWidgetimg.clear()
            self.listWidgetimg.addItems(self.img_list)
            if len(already_exist_lable_list) == self.image_count:
                reply = QMessageBox(QMessageBox.Question, self.tr("提示"), self.tr("已经全部筛完,点击确定工具将关闭!"), QMessageBox.NoButton, self)
                yr_btn = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
                reply.exec_()
                if reply.clickedButton() == yr_btn:
                    sys.exit()
            else:
                self.imgshow()

    def imgshow(self):
        img = cv2.imread(os.path.join(self.image_dir, self.img_list[self.image_idx]))
        cvimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 把opencv 默认BGR转为通用的RGB
        y, x = img.shape[:-1]
        frame = QImage(cvimg, x, y, QImage.Format_RGB888)
        self.scene.clear()  #先清空上次的残留
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！
        self.item.setScale(self.zoomscale)
        self.scene.addItem(self.item)  # 将图元添加到场景中
        rect = self.graphicsView.scene().sceneRect()
        self.graphicsView.setScene(self.scene)  
        rect.setTopLeft(self.graphicsView.mapToScene(QPoint(0, 0)))
        self.graphicsView.setScene(self.scene)  # 将场景添加至视图  picshow为graphicsView视图
        self.graphicsView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.now_idx.setText(self.img_list[self.image_idx])

    def openimgdirfn(self):
        self.image_dir = QFileDialog.getExistingDirectory(self, "选择图片目录")
        if self.image_dir != "":
            for item in os.listdir(self.image_dir):
                if item.split(".")[-1] in self.img_end:
                    self.img_list.append(item)
                    self.listWidgetimg.addItem(item)
            if self.img_list == []:
                reply = QMessageBox(QMessageBox.Question, self.tr("提示"), self.tr("该文件夹内没有图片喔,请重新选择目录!"), QMessageBox.NoButton, self)
                reply.addButton(self.tr("确定"), QMessageBox.YesRole)
                reply.exec_()
                self.openimgdirfn()
            else:
                self.image_count = len(self.img_list)
                self.img_list.sort()
                self.imgshow()

    def openlabeldirfn(self):
        self.label_dir = QFileDialog.getExistingDirectory(self, "选择保存目录")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    select = Select()
    sys.exit(app.exec_())
