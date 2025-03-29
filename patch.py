import numpy as np

# Если атрибут отсутствует, задаём его как обычное DeprecationWarning
if not hasattr(np, "VisibleDeprecationWarning"):
    np.VisibleDeprecationWarning = DeprecationWarning

# Теперь импортируем и запускаем Rasa
from rasa.__main__ import main
if __name__ == "__main__":
    main()