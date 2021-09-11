from chalicelib.dao.migration.shared import BaseMigration


class Migration_0_1_3(BaseMigration):

    def __init__(self):
        super().__init__("0.1.3")

    def migrate(self):
        pass