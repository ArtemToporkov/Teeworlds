MAP_SAVING_DIALOG_STYLE = """
    QInputDialog {
        background-color: #66594b;
        border: 5px solid #38312a; /* Коричневая рамка */
        border-radius: 15px; /* Скруглённые углы */
        padding: 5px; /* Дополнительное пространство внутри кнопки */
        color: #000000;
        font-family: Arial;
        font-weight: bold;
    }
    QInputDialog QPushButton {
        background-color: #FFC89C;
        font-family: Arial;
        font-weight: bold;
    }

    QInputDialog QPushButton:hover {
        background-color: #FFDBBF; /* Изменение цвета фона при наведении */
        border-radius: 15px; /* Скруглённые углы */
        font-family: Arial;
        font-weight: bold;
    }

    QInputDialog QPushButton:pressed {
        background-color: #FFB881; /* Изменение цвета фона при нажатии */
        border-radius: 15px; /* Скруглённые углы */
        font-family: Arial;
        font-weight: bold;
    }
    
    QInputDialog QLineEdit {
        background-color: #FFC89C;
    }
    """