from chalicelib.dao.migration.shared import BaseMigration


class Migration_0_1_1(BaseMigration):

    def __init__(self):
        super().__init__("0.1.1")

    def migrate(self):
        pass