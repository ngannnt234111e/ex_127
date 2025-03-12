import pandas as pd
import sys

import matplotlib.pyplot as plt
from PyQt6 import uic
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QTableWidgetItem, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


class StockAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        uic.loadUi('stock_analysis.ui', self)

        # Apply custom styling
        self.apply_custom_styling()

        # Load data
        self.load_data()

        # Set up matplotlib figure and canvas
        self.figure = plt.figure(figsize=(12, 4))
        self.canvas = FigureCanvas(self.figure)
        chart_layout = QVBoxLayout(self.chartWidget)
        chart_layout.addWidget(self.canvas)

        # Connect buttons to functions
        self.searchButton.clicked.connect(self.search_and_modify)
        self.addButton.clicked.connect(self.add_data)
        self.deleteButton.clicked.connect(self.delete_data)
        self.sortButton.clicked.connect(self.sort_by_price)
        self.statsButton.clicked.connect(self.calculate_stats)
        self.chartButton.clicked.connect(self.generate_charts)

        # Update table with initial data
        self.update_table()

        # Generate initial charts
        self.generate_charts()

    def apply_custom_styling(self):
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 12px;
                background-color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: #3498db;
                color: white;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
                padding: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
            }
            QComboBox {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
            }
            QTableWidget {
                alternate-background-color: #e6f3ff;
                gridline-color: #d4d4d4;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 4px;
                border: 1px solid #2980b9;
                font-weight: bold;
            }
            QLabel {
                font-weight: bold;
                color: #2c3e50;
            }
        """)

        # Set different colors for different control groups
        self.searchGroup.setStyleSheet(
            "QGroupBox { border-color: #e74c3c; } QGroupBox::title { background-color: #e74c3c; }")
        self.addGroup.setStyleSheet(
            "QGroupBox { border-color: #2ecc71; } QGroupBox::title { background-color: #2ecc71; }")
        self.deleteGroup.setStyleSheet(
            "QGroupBox { border-color: #f39c12; } QGroupBox::title { background-color: #f39c12; }")
        self.statsGroup.setStyleSheet(
            "QGroupBox { border-color: #9b59b6; } QGroupBox::title { background-color: #9b59b6; }")
        self.chartGroup.setStyleSheet(
            "QGroupBox { border-color: #1abc9c; } QGroupBox::title { background-color: #1abc9c; }")

        # Set different button colors
        self.searchButton.setStyleSheet("background-color: #e74c3c;")
        self.addButton.setStyleSheet("background-color: #2ecc71;")
        self.deleteButton.setStyleSheet("background-color: #f39c12;")
        self.sortButton.setStyleSheet("background-color: #9b59b6;")
        self.statsButton.setStyleSheet("background-color: #9b59b6;")
        self.chartButton.setStyleSheet("background-color: #1abc9c;")

        # Set alternating row colors for table
        self.tableWidget.setAlternatingRowColors(True)

    def load_data(self):
        try:
            # For this example, we'll use a local file path
            # In a real application, you would use the URL: https://tranduythanh.com/datasets/SampleData2.csv
            # self.df = pd.read_csv("https://tranduythanh.com/datasets/SampleData2.csv")

            # For demonstration, I'll create sample data similar to what might be in the file
            data = {
                'Symbol': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM'],
                'Price': [180.5, 350.2, 140.8, 130.5, 300.7, 250.3, 450.2, 140.6],
                'PE': [28.5, 32.1, 25.7, 40.2, 22.3, 60.5, 45.8, 12.3],
                'Group': ['Tech', 'Tech', 'Tech', 'Retail', 'Tech', 'Auto', 'Tech', 'Finance']
            }
            self.df = pd.DataFrame(data)

            # Add USD column (requirement 4)
            self.df['USD'] = self.df['Price'] / 23

            print("Data loaded successfully:")
            print(self.df)  # Requirement 1: Print all data
        except Exception as e:
            print(f"Error loading data: {e}")
            # Create empty DataFrame with the same structure if loading fails
            self.df = pd.DataFrame(columns=['Symbol', 'Price', 'PE', 'Group', 'USD'])

    def update_table(self):
        # Update the table with current DataFrame data
        self.tableWidget.setRowCount(len(self.df))
        self.tableWidget.setColumnCount(len(self.df.columns))
        self.tableWidget.setHorizontalHeaderLabels(self.df.columns)

        # Fill the table with data
        for row in range(len(self.df)):
            for col in range(len(self.df.columns)):
                value = str(self.df.iloc[row, col])
                item = QTableWidgetItem(value)

                # Color-code cells based on group
                if col == 3:  # Group column
                    group = self.df.iloc[row, col]
                    if group == 'Tech':
                        item.setBackground(QColor(217, 242, 255))  # Light blue
                    elif group == 'Retail':
                        item.setBackground(QColor(255, 240, 217))  # Light orange
                    elif group == 'Auto':
                        item.setBackground(QColor(217, 255, 217))  # Light green
                    elif group == 'Finance':
                        item.setBackground(QColor(242, 217, 255))  # Light purple

                # Color-code price cells based on value
                if col == 1:  # Price column
                    price = self.df.iloc[row, col]
                    if price > 300:
                        item.setBackground(QColor(217, 255, 217))  # Light green for high prices
                    elif price < 150:
                        item.setBackground(QColor(255, 217, 217))  # Light red for low prices

                self.tableWidget.setItem(row, col, item)

        # Resize columns to content
        self.tableWidget.resizeColumnsToContents()

    def search_and_modify(self):
        # Requirement 3: Search by Symbol and reduce Price by 1/2
        symbol = self.symbolInput.text().strip()
        if not symbol:
            QMessageBox.warning(self, "Input Error", "Please enter a symbol to search.")
            return

        if symbol in self.df['Symbol'].values:
            self.df.loc[self.df['Symbol'] == symbol, 'Price'] /= 2
            # Update USD column after price change
            self.df['USD'] = self.df['Price'] / 23
            self.update_table()
            QMessageBox.information(self, "Success", f"Price for {symbol} reduced by half.")
        else:
            QMessageBox.warning(self, "Not Found", f"Symbol {symbol} not found in the data.")

    def add_data(self):
        # Requirement 5: Add new data to DataFrame
        try:
            symbol = self.newSymbol.text().strip()
            price = float(self.newPrice.text().strip())
            pe = float(self.newPE.text().strip())
            group = self.newGroup.text().strip()

            if not all([symbol, self.newPrice.text(), self.newPE.text(), group]):
                QMessageBox.warning(self, "Input Error", "All fields are required.")
                return

            # Calculate USD
            usd = price / 23

            # Add new row to DataFrame
            new_row = pd.DataFrame({
                'Symbol': [symbol],
                'Price': [price],
                'PE': [pe],
                'Group': [group],
                'USD': [usd]
            })

            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self.update_table()

            # Clear input fields
            self.newSymbol.clear()
            self.newPrice.clear()
            self.newPE.clear()
            self.newGroup.clear()

            QMessageBox.information(self, "Success", "New data added successfully.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Price and PE must be numeric values.")

    def delete_data(self):
        # Requirement 7: Delete rows by Symbol
        symbol = self.deleteSymbol.text().strip()
        if not symbol:
            QMessageBox.warning(self, "Input Error", "Please enter a symbol to delete.")
            return

        initial_len = len(self.df)
        self.df = self.df[self.df['Symbol'] != symbol]

        if len(self.df) < initial_len:
            self.update_table()
            QMessageBox.information(self, "Success", f"Rows with Symbol {symbol} deleted.")
        else:
            QMessageBox.warning(self, "Not Found", f"Symbol {symbol} not found in the data.")

    def sort_by_price(self):
        # Requirement 2: Sort by Price ascending
        self.df = self.df.sort_values(by='Price')
        self.update_table()
        QMessageBox.information(self, "Success", "Data sorted by Price (ascending).")

    def calculate_stats(self):
        # Requirement 6: Group by Group column and calculate statistics
        stat_func = self.statsCombo.currentText()

        try:
            if stat_func == "mean":
                result = self.df.groupby('Group').mean()
            elif stat_func == "sum":
                result = self.df.groupby('Group').sum()
            elif stat_func == "count":
                result = self.df.groupby('Group').count()
            elif stat_func == "min":
                result = self.df.groupby('Group').min()
            elif stat_func == "max":
                result = self.df.groupby('Group').max()

            # Display results in a message box
            QMessageBox.information(self, f"Group {stat_func.capitalize()}",
                                    f"Results of {stat_func} by Group:\n\n{result}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error calculating statistics: {e}")

    def generate_charts(self):
        # Clear previous charts
        self.figure.clear()

        # Set a custom style for the charts
        plt.style.use('ggplot')

        # Create two subplots
        ax1 = self.figure.add_subplot(121)
        ax2 = self.figure.add_subplot(122)

        # Custom colors for the charts
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#34495e', '#d35400']

        # Chart 1: Bar chart of prices by symbol
        bars = ax1.bar(self.df['Symbol'], self.df['Price'], color=colors[:len(self.df)])
        ax1.set_title('Price by Symbol', fontweight='bold', fontsize=12)
        ax1.set_xlabel('Symbol', fontweight='bold')
        ax1.set_ylabel('Price', fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)

        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., height + 5,
                     f'{height:.1f}', ha='center', va='bottom', fontweight='bold')

        # Chart 2: Pie chart of group distribution
        group_counts = self.df['Group'].value_counts()
        explode = [0.1 if i == 0 else 0 for i in range(len(group_counts))]  # Explode first slice

        ax2.pie(group_counts, labels=group_counts.index, autopct='%1.1f%%',
                explode=explode, colors=colors[:len(group_counts)], shadow=True,
                wedgeprops={'edgecolor': 'white', 'linewidth': 1})
        ax2.set_title('Distribution by Group', fontweight='bold', fontsize=12)

        self.figure.tight_layout()
        self.canvas.draw()

