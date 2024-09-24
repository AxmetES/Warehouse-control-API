import sys
import os

# Добавляем корневую директорию в sys.path для тестов
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
