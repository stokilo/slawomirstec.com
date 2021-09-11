from chalicelib.dao.migration.shared import BaseMigration


class Migration_0_1_2(BaseMigration):

    def __init__(self):
        super().__init__("0.1.2")

    def migrate(self):
        pass