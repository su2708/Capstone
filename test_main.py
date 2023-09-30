import test_thread as WT

work = WT.WorkThread(WT.model_weights)

if __name__ == "__main__":
    WT.image_label.setFixedSize(WT.width, WT.height)
    WT.image_label2.setFixedSize(WT.width, WT.height)
    WT.window.setWindowTitle("Multi Camera Demo")
    WT.layout_h.addWidget(WT.image_label)    
    WT.layout_h.addWidget(WT.image_label2)
    WT.layout_v.addLayout(WT.layout_h,20)
    WT.window.setLayout(WT.layout_v)
    WT.window.resize(660, 250)

    work.start()
    
    WT.window.show()
    WT.app.exec()
    work.quit()
    WT.picam2.close()

