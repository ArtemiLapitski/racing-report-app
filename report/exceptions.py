class DriverNotFound(Exception):
    def __init__(self, driver):
        super().__init__(f"'{driver}' driver was not found.")
        self.driver = driver
