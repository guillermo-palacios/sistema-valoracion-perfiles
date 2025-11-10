import sys
from PyQt5.QtWidgets import (QApplication)
from VtsValoracion import VtsValoracion

app=QApplication([])
w=VtsValoracion()
w.show()

sys.exit(app.exec_())
