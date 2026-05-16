import xlwings as xw
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
import numpy as np
import os
import sys

from load_data import lade_daten
from calculations import berechne_werte
from excel_export import exportiere_excel


print("Programm gestartet")


dfGesamt = lade_daten()
dfGesamt = berechne_werte(dfGesamt)
exportiere_excel(dfGesamt)

