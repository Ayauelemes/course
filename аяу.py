import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QMessageBox, QFrame, QSizePolicy
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt


class DatabaseManager:
    def __init__(self, db_name="users_pyside.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def register_user(self, email, password):
        try:
            self.cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            self.conn.commit()
            return True, "Тіркелу сәтті өтті!"
        except sqlite3.IntegrityError:
            return False, "Бұл Email адресі тіркелген."

    def login_user(self, email, password):
        self.cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        return self.cursor.fetchone() is not None


class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.setWindowTitle("Кіру және Тіркелу (PySide6)")
        self.setFixedSize(700, 450) # Өлшемді бекіту

        self.setup_ui()
        self.apply_style()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
       
        self.left_frame = QFrame()
        self.left_frame.setObjectName("LeftFrame")
        self.left_frame.setFixedWidth(300)
        left_layout = QVBoxLayout(self.left_frame)
        left_layout.setAlignment(Qt.AlignCenter)
        
        logo_label = QLabel("Desktop - Primary")
        logo_label.setFont(QFont('Arial', 14, QFont.Bold))
        logo_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(logo_label)

       
        self.right_frame = QFrame()
        self.right_frame.setObjectName("RightFrame")
        right_layout = QVBoxLayout(self.right_frame)
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(50, 50, 50, 50)
        
        
        title = QLabel("Кіру")
        title.setFont(QFont('Arial', 28, QFont.Light))
        title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title)
        
       
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Құпия сөз")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Батырмалар
        self.login_button = QPushButton("Кіру")
        self.login_button.setObjectName("PrimaryButton")
        self.login_button.clicked.connect(self.handle_login)
        
        self.register_button = QPushButton("Тіркелу")
        self.register_button.setObjectName("SecondaryButton")
        self.register_button.clicked.connect(self.handle_register)

        right_layout.addWidget(self.email_input)
        right_layout.addWidget(self.password_input)
        right_layout.addWidget(self.login_button)
        right_layout.addWidget(self.register_button)

        main_layout.addWidget(self.left_frame)
        main_layout.addWidget(self.right_frame)
        
    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 #1e3a8a, stop:1 #3b82f6); /* Көк градиент */
                color: white;
            }
            
            /* Сол жақ көмескі блок */
            QFrame#LeftFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 15px 0 0 15px; /* Бұрыштарды дөңгелектеу */
                border-right: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            /* Оң жақ форма блогы */
            QFrame#RightFrame {
                background-color: transparent; 
            }

            /* Енгізу өрістері */
            QLineEdit {
                padding: 12px;
                border: 1px solid rgba(255, 255, 255, 0.4);
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.2); /* Мөлдір фон */
                color: white;
                margin-bottom: 10px;
                font-size: 16px;
            }
            
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.7);
            }
            
            /* Батырмалардың негізгі стилі */
            QPushButton {
                padding: 12px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                margin-top: 10px;
            }
            
            /* Кіру батырмасы (Primary) */
            QPushButton#PrimaryButton {
                background-color: #3b82f6; 
                color: white;
            }
            
            /* Тіркелу/Рестарт батырмасы (Secondary) */
            QPushButton#SecondaryButton {
                background-color: #6b7280; 
                color: white;
            }
        """)
    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        
        if self.db.login_user(email, password):
            QMessageBox.information(self, "Сәттілік", f"Қош келдіңіз, {email}!")
        else:
            QMessageBox.warning(self, "Қате", "Қате Email немесе Құпия сөз.")
        self.email_input.clear()
        self.password_input.clear()

    def handle_register(self):
        email = self.email_input.text()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Қате", "Барлық өрістерді толтырыңыз.")
            return

        success, message = self.db.register_user(email, password)
        if success:
            QMessageBox.information(self, "Сәттілік", message)
        else:
            QMessageBox.warning(self, "Қате", message)
        self.email_input.clear()
        self.password_input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginApp()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.setAttribute(Qt.WA_TranslucentBackground)
    window.show()
    sys.exit(app.exec())