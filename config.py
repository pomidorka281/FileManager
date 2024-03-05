class Config:
    def __init__(self):
        with open('cfg.txt', 'r') as cfg:
            self.work_folder = cfg.read()

    def set_folder(self, name):
        self.work_folder = name
        with open('cfg.txt', 'w') as cfg:
            cfg.write(self.work_folder)
