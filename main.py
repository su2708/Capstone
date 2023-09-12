import work_thread as WT

work = WT.WorkThread()

if __name__ == "__main__":
    WT.image_label.setFixedSize(320, 240)
    WT.image_label2.setFixedSize(320, 240)
    WT.window.setWindowTitle("Multi Camera Demo")
    WT.layout_h.addWidget(WT.image_label)    
    WT.layout_h.addWidget(WT.image_label2)
    WT.layout_v.addLayout(WT.layout_h,20)
    WT.window.setLayout(WT.layout_v)
    WT.window.resize(660, 500)

    work.start()
    
    WT.window.show()
    WT.app.exec()
    work.quit()
    WT.picam2.close()

