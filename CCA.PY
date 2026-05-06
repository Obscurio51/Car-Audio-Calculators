import sys, os, math, random, base64, tempfile, shutil, subprocess, atexit
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTextEdit, QComboBox, QRadioButton, QButtonGroup, QMessageBox, QFrame, QGridLayout)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QTimer

# pygame opzionale
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

# Stringa base64 della musica
BASE64_XM = r"""RXh0ZW5kZWQgTW9kdWxlOiBSZWxvYWRlZCBLZXlnZW4gIzEgIBpGYXN0VHJhY2tlciB2Mi4wMCAgIAQBFAEAAAoAAAAEAAUACAAAAAYAfQAAAQABAgIDAwQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQAAAABAAPMCmzEFDwSbPQEEoYMuAoMxCICIBICbMQgMIIMxBps9AQwggzoCgykIgzEGiASAmzEIDCCDMQebPQEMIIMuAoMxCICIBICbKQgMIIMxBos1AQSDOgKDKQiDMQaIBICbMQgMIIMxBZs9AQwggy4CgzEIgIgEgJspCAwggzEGizoBBIM6AoMpCIMxBogEgJsxCAwggzEHmzUBDCCDLgKDMQiAiASAmykIDCCDMQaLPQEEgzoCgykIgzEGiASAmzEIDCCDMQWLPAEEgywCgzAIgIgEgJspCAwggzEGiASDOAKDJwiDMQaIBICbMAgMIIMxB5s8AQwwgywCgzAIgJgCEICbJwgMIIMxBpgCEIM4AoMnCIMxBpgCEICbMAgMIIMxBZs8AQwlgywCgzAIgJgCEICbJwgMIIMxBpgCEIM4AoMnCIMxBpgCEICbMAgMIIMxB5s8AQwggywCgzAIgJgCEICbJwgMIIMxBpgCEIM4AoMnCIMxBpgCEICbMAgMIIMxBYs8AQSDLAKDMAiAiASAmycIDCCDMQabPAEMIIM4AoMnCIMxBogEgJswCAwggzEHmzwBDCCDLAKDMAiAiASAmycIDCCDMQaLMwEEgzgCgycIgzEGiASAmzAIDCCDMQWbPAEMIIMsAoMwCICIBICbJwgMIIMxBos4AQSDOAKDJwiDMQaIBICbMAgMIIMxB5szAQwggywCgzAIgIgEgJsnCAwggzEGizwBBIM4AoMnCIMxBogEgJswCAwggzEFizoBBIMnAoMuCICIBICbJwgMIIMxBogEgzMCgycIgzEGiASAmy4IDCCDMQebOgEMMIMnAoMuCICYAhCAmycIDCCDMQaYAhCDMwKDJwiDMQaYAhCAmy4IDCCDMQWbOgEMJYMnAoMuCICYAhCAmycIDCCDMQaYAhCDMwKDJwiDMQaYAhCAmy4IDCCDMQebOgEMIIMnAoMuCICYAhCAmycIDCCDMQaYAhCDMwKDJwiDMQaYAhCAmy4IDCAJAAAAAEAA8wKbMQUPBJs9AQShgy4CgzEIgIgEgJsxCAwggzEGmz0BDCCDOgKDKQiDMQaIBICbMQgMIIMxB5s9AQwggy4CgzEIgIgEgJspCAwggzEGizUBBIM6AoMpCIMxBogEgJsxCAwggzEFmz0BDCCDLgKDMQiAiASAmykIDCCDMQaLOgEEgzoCgykIgzEGiASAmzEIDCCDMQebNQEMIIMuAoMxCICIBICbKQgMIIMxBos9AQSDOgKDKQiDMQaIBICbMQgMIIMxBYs8AQSDLAKDMAiAiASAmykIDCCDMQaIBIM4AoMnCIMxBogEgJswCAwggzEHmzoBDDCDLAKDMAiAmAIQgJsnCAwggzEGmAIQgzgCgycIgzEGmAIQgJswCAwggzEFmzgBDCWDLAKDMAiAmAIQgJsnCAwggzEGmAIQgzgCgycIgzEGmAIQgJswCAwggzEHmzMBDCCDLAKDMAiAmAIQgJsnCAwggzEGmAIQgzgCgycIgzEGmAIQgJswCAwggzEFizwBBIMsAoMwCICIBICbJwgMIIMxBps8AQwggzgCgycIgzEGiASAmzAIDCCDMQebPAEMIIMsAoMwCICIBICbJwgMIIMxBoszAQSDOAKDJwiDMQaIBICbMAgMIIMxBZs8AQwggywCgzAIgIgEgJsnCAwggzEGizgBBIM4AoMnCIMxBogEgJswCAwggzEHmzMBDCCDLAKDMAiAiASAmycIDCCDMQaLPAEEgzgCgycIgzEGiASAmzAIDCCDMQWLOgEEgycCgy4IgIgEgJsnCAwggzEGiASDMwKDJwiDMQaIBICbLggMIIMxB5s4AQwwgycCgy4IgJgCEICbJwgMIIMxBpgCEIMzAoMnCIMxBpgCEICbLggMIIMxBZs3AQwlgycCgy4IgJgCEICbJwgMIIMxBpgCEIMzAoMnCIMxBpgCEICbLggMIIMxB5szAQwggycCgy4IgJgCEICbJwgMIIMxBpgCEIMzAoMnCIMxBpgCEICbLggMIAkAAAAAQACoApsxBQ8Eky4IN4MuAoMxCICQN4CbMQgMIIMxBpA3gzoCgykIgzEGkDeAmzEIDCCDMQeQV4MuAoMxCICQV4CbKQgMIIMxBpBXgzoCgykIgzEGkFeAmzEIDCCDMQWQN4MuAoMxCICQN4CbKQgMIIMxBpA3gzoCgykIgzEGkDeAmzEIDCCDMQeQV4MuAoMxCICQN4CbKQgMIIMxBpBXgzoCgykIgzEGkDeAmzEIDCCDMQWTLAhHgywCgzAIgJBHgJspCAwggzEGkEeDOAKDJwiDMQaQR4CbMAgMIIMxB5BXgywCgzAIgJBXgJsnCAwggzEGkFeDOAKDJwiDMQaQV4CbMAgMIIMxBZBHgywCgzAIgJBHgJsnCAwggzEGkEeDOAKDJwiDMQaQR4CbMAgMIIMxB5BHgywCgzAIgJBHgJsnCAwggzEGkEeDOAKDJwiDMQaQR4CbMAgMIIMxBZBHgywCgzAIgJBHgJsnCAwggzEGkEeDOAKDJwiDMQaQR4CbMAgMIIMxB5BXgywCgzAIgJBXgJsnCAwggzEGkFeDOAKDJwiDMQaQV4CbMAgMIIMxBZBHgywCgzAIgJBHgJsnCAwggzEGkEeDOAKDJwiDMQaQR4CbMAgMIIMxB5BXgywCgzAIgJBHgJsnCAwggzEGkFeDOAKDJwiDMQaQR4CbMAgMIIMxBZMnCEeDJwKDLgiAkEeAmycIDCCDMQaQR4MzAoMnCIMxBpBHgJsuCAwggzEHkFmDJwKDLgiAkFmAmycIDCCDMQaQWYMzAoMnCIMxBpBZgJsuCAwggzEFkEeDJwKDLgiAkEeAmycIDCCDMQaQR4MzAoMnCIMxBpBHgJsuCAwggzEHkEeDJwKDLgiAkEeAmycIDCCDMQaQR4MzAoMnCIMxBpBHgJsuCAwgCQAAAABAAKgCmzEFDwSTLwg3gy8CgzIIgJA3gJsyCAwggzEGkDeDOwKDKgiDMQaQN4CbMggMIIMxB5BXgy8CgzIIgJBXgJsqCAwggzEGkFeDOwKDKgiDMQaQV4CbMggMIIMxBZA3gy8CgzIIgJA3gJsqCAwggzEGkDeDOwKDKgiDMQaQN4CbMggMIIMxB5BXgy8CgzIIgJA3gJsqCAwggzEGkFeDOwKDKgiDMQaQN4CbMggMIIMxBZMtCEeDLQKDMQiAkEeAmyoIDCCDMQaQR4M5AoMoCIMxBpBHgJsxCAwggzEHkFeDLQKDMQiAkFeAmygIDCCDMQaQV4M5AoMoCIMxBpBXgJsxCAwggzEFkEeDLQKDMQiAkEeAmygIDCCDMQaQR4M5AoMoCIMxBpBHgJsxCAwggzEHkEeDLQKDMQiAkEeAmygIDCCDMQaQR4M5AoMoCIMxBpBHgJsxCAwggzEFkEeDLQKDMQiAkEeAmygIDCCDMQaQR4M5AoMoCIMxBpBHgJsxCAwggzEHkFeDLQKDMQiAkFeAmygIDCCDMQaQV4M5AoMoCIMxBpBXgJsxCAwggzEFkEeDLQKDMQiAkEeAmygIDCCDMQaQR4M5AoMoCIMxBpBHgJsxCAwggzEHkFeDLQKDMQiAkEeAmygIDCCDMQaQV4M5AoMoCIMxBpBHgJsxCAwggzEFkygIR4MoAoMvCICQR4CbKAgMIIMxBpBHgzQCgygIgzEGkEeAmy8IDCCDMQeQWYMoAoMvCICQWYCbKAgMIIMxBpBZgzQCgygIgzEGkFmAmy8IDCCDMQWQR4MoAoMvCICQR4CbKAgMIIMxBpBHgzQCgygIgzEGkEeAmy8IDCCDMQeQR4MoAoMvCICQR4CbKAgMIIMxBpBHgzQCgygIgzEGkEeAmy8IDCAJAAAAAEAAqAKbMQUPBJMwCDeDMAKDMwiAkDeAmzMIDCCDMQaQN4M8AoMrCIMxBpA3gJszCAwggzEHkFeDMAKDMwiAkFeAmysIDCCDMQaQV4M8AoMrCIMxBpBXgJszCAwggzEFkDeDMAKDMwiAkDeAmysIDCCDMQaQN4M8AoMrCIMxBpA3gJszCAwggzEHkFeDMAKDMwiAkDeAmysIDCCDMQaQV4M8AoMrCIMxBpA3gJszCAwggzEFky4IR4MuAoMyCICQR4CbKwgMIIMxBpBHgzoCgykIgzEGkEeAmzIIDCCDMQeQV4MuAoMyCICQV4CbKQgMIIMxBpBXgzoCgykIgzEGkFeAmzIIDCCDMQWQR4MuAoMyCICQR4CbKQgMIIMxBpBHgzoCgykIgzEGkEeAmzIIDCCDMQeQR4MuAoMyCICQR4CbKQgMIIMxBpBHgzoCgykIgzEGkEeAmzIIDCCDMQWQR4MuAoMyCICQR4CbKQgMIIMxBpBHgzoCgykIgzEGkEeAmzIIDCCDMQeQV4MuAoMyCICQV4CbKQgMIIMxBpBXgzoCgykIgzEGkFeAmzIIDCCDMQWQR4MuAoMyCICQR4CbKQgMIIMxBpBHgzoCgykIgzEGkEeAmzIIDCCDMQeQV4MuAoMyCICQR4CbKQgMIIMxBpBXgzoCgykIgzEGkEeAmzIIDCCDMQWTKQhHgykCgzAIgJBHgJspCAwggzEGkEeDNQKDKQiDMQaQR4CbMAgMIIMxB5BZgykCgzAIgJBZgJspCAwggzEGkFmDNQKDKQiDMQaQWYCbMAgMIIMxBZBHgykCgzAIgJBHgJspCAwggzEGkEeDNQKDKQiDMQaQR4CbMAgMIIMxB5BHgykCgzAIgJBHgJspCAwggzEGkEeDNQKDKQiDMQaQR4CbMAgMIAcBAABDb21wb3NlZCAmIFRyYWNrZWQgQnkAAgEAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAAEAEAACAAsAA4ACAAYABYAIAAIADwAAABGAAAAUAAAAFoAAABkAAAAbgAAAAAAIAAKACgAHgAYADIAIAA8ACAARgAgAFAAIABaACAAZAAgAG4AIAB4ACAAggAgAAYGAgMFAgMFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAAAAAAAAAAcAAAAQAABgAAVQ29tcG9zZWQgJiBUcmFja2VkIEJ5IAAAAACBAAAAABLuAAAAAAD+APIOAADwAOUA4QAHAQAATEhTL0RGUyAoYykAAAAAAAAAAAAAAAIBACgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAABABAAAgALAAOAAgAGAAWACAACAA8AAAARgAAAFAAAABaAAAAZAAAAG4AAAAAACAACgAoAB4AGAAyACAAPAAgAEYAIABQACAAWgAgAGQAIABuACAAeAAgAIIAIAAGBgIDBQIDBQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHwAAAAMAAAAcAAAAEAAAYAAC0xIUy9ERlMgKGMpICAgICAgICAgICAM+v7+AKX67fYAAAAAAAAAAAAA/wA1y/4AAAAAAAAAAAAAOMgAAAAAAAAAAAAAAAAAPMQAAAIAAAAAAAAAAAD1AAAA5QAeAADhAAAeAQAAAAAAAAAAAAD7+QD6APkA+QD5APgA+QD4APgA+AD4APgA+QD5APkA+QD4APoABwEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAQAoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAQAQAAIACwADgAIABgAFgAgAAgAPAAAAEYAAABQAAAAWgAAAGQAAABuAAAAAAAgAAoAKAAeABgAMgAgADwAIABGACAAUAAgAFoAIABkACAAbgAgAHgAIACCACAABgYCAwUCAwUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOAAAAAAAAAA4AAABAAAGAAAAgICAgICAgICAgICAgICAgICAgICAgAACzAAAZ5wCTAADu9OoHAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBACgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAABABAAAgALAAOAAgAGAAWACAACAA8AAAARgAAAFAAAABaAAAAZAAAAG4AAAAAACAACgAoAB4AGAAyACAAPAAgAEYAIABQACAAWgAgAGQAIABuACAAeAAgAIIAIAAGBgIDBQIDBQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4AAAAAAAAADgAAAEAAAYAAACAgICAgICAgICAgICAgICAgICAgICAAANEAABoIBhAx4QT58gcBAABEb25lIGF0IDA5LjEwLjIwMDMAAAAAAgEAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAAEAEAACAAsAA4ACAAYABYAIAAIADwAAABGAAAAUAAAAFoAAABkAAAAbgAAAAAAIAAKACgAHgAYADIAIAA8ACAARgAgAFAAIABaACAAZAAgAG4AIAB4ACAAggAgAAYGAgMFAgMFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA3AMAAAAAAAAAAAAAQAAAgAASRG9uZSBhdCAwOS4xMC4yMDAzICAgIAAAAAIc4v7yBBIO3P4EEgzeGgTs+PziUuDaRqw6ykbSCvAegP4CrnDhD/HB/kHX4rws3hKUOqK+Qv8BAP8LXpgA/wG+Qv6gYgD/ATrGAAAAPsJesvAAPsJuklioWMZE4hIO+hoYPrCB3wIGGfULAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANEvAPf01t5GiAq6CiyaKuD2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI+AAAAA7yIkjESvb4GAgm+CLqT9f8LfMNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPMIBOL8xCD04vrq7uIe7vL09NoQ7vgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAAoW9iTqHv4CEAIUAiTyHvruHB76BBoI7AIqAfEPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP3uCgTq9g7eLOIABPjiLuD69AIC9OgI7hjQJPT0+gbyCvYI8PQG7gby+g709gzy+vj2Evj6BOQY+vr+EOICBAb0AAAAAAAABPwAAAb6AAAAAAAAAAAGCPIS8AoU+PwCBhDkChAEAgL+FPYK/vwS/gr8/AwI8BgA/P4U4iL0AAr8CgQC+v4O+AD6BAYI9g7wBAIK+gYE7hYC8vgADPoAAPQCFvIK9AjyBvwCCOwQ9gwC9Ar+BP4O+ADuEvoEAPoS8vgMAAb0EAL4DvII+Az0CAYA9BTsDv78AgIE/gICCPz2DPj4Bv4M8Ab+CPACAAL+/gjuDPoK9AAC8gj2CPoI8gIE+gT0Avz8BPr2CgTuDPgI9vYCBPoC+BLoDPQM+AL8/gjy/g74AAL+BAD+/Aj6Agb2AggG7hIABP78BgT0BgL2Evr8DPgE/AII+gL6/goE8gz0FP74/hD6BPwGAAAK9g76/vgKCvz8CPII/gACAAoA+AQC/PgICvwC/AQCAPYK9gb8CAL6/v78Bg7qCvoABAL8AvwE/voC/AT8CPIIBPwEAvwI8gL6DPIG9hLyBgAK7gAU6AgI9vwCCPgG+gzwDvr+Av74DPj+CPoG/AIA/Ar4CPgCAv4AAv4C/vYKAPr8EvYG9gr0BgT6+gb8BAAAAAoHAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBACgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAABABAAAgALAAOAAgAGAAWACAACAA8AAAARgAAAFAAAABaAAAAZAAAAG4AAAAAACAACgAoAB4AGAAyACAAPAAgAEYAIABQACAAWgAgAGQAIABuACAAeAAgAIIAIAAGBgIDBQIDBQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJoBAAAAAAAAAAAAAEAAAIAAACAgICAgICAgICAgICAgICAgICAgICAAAAAAAAAAABbbBxTlAxAF6zPH8SHm+SEnBbPsaL4f5OJI1hXoE+Iw5TuRU/m081L4/ADfQhWwGi64MOr4FOUACgfyDAAA8SXqDATkEPAV9wAnEpI14x0A49dn3/EPAOY05vgACAAA+yykIyjQHALbT9TvLRu7EPzxDwAA6gcPFgTX9Rz+xzkA5hLectnQG/T0+hIA5jDq5g4O3VqmI+8PAAAQ4f0o8/f47jTmAB4J2QAA+Bi3Kg8ADPQW9g7mFuL5ABstnyjxDznT9h/TRZ1I0/UL7hnnLeUR7Dm/Qb8VBQD70GupEiID2x8D3g8J+wDwDAAW4gAIHvL0/v4A6iL0ABDkOuL0/PElyS399/Qq5A7wAhycKSEA6iLwAPj5NuX0AuQS5z/iAOo9vxoe7v37CNr5V9P3AAAMG7wdAAAM7AgAAPEP8SX68AwA9BO7Zc8R3hv0AAQMzxUM+Ajq9SH0BAjfN+oAAB7BAC34/PEPABPhB/n99RoAAATbV+jTJfb0CfcE/An57AMKFfL+AB740DjTKdcPEADrBQcBAABFbmpveSEgOikAAAAAAAAAAAAAAAAAAgEAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAAEAEAACAAsAA4ACAAYABYAIAAIADwAAABGAAAAUAAAAFoAAABkAAAAbgAAAAAAIAAKACgAHgAYADIAIAA8ACAARgAgAFAAIABaACAAZAAgAG4AIAB4ACAAggAgAAYGAgMFAgMFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAmgIAAAAAAAAAAAAAQAAAgAAJRW5qb3khIDopICAgICAgICAgICAgIAAAAIAAAICAAAAAAAAAABTsIlyBAOMUCcc5AAAAAAAAAAAAAAAAAADtE5tmMvb24gAAAAAAAAAAAAAAAAA6+AqE1jT6O+0TAAAAAO0QAwAAAJtOF2Oe/38M6tToANAAAAAAAAAAAAAAAGKeFOwyzhTsftbcfFPt7iXpFwAAAAAAAAAAAAAAAO1EToGBgH6CXqIAAAAAAAAAAAAAGOgAAAAAcDR00EBWgQAAAAAA98o/0S8AALf2U8U2wgpsTrDQEPAAAAAABDj00AAe8hLefpYGSADGOmyErQH/ALdJ4x0A6RcAAOkX+wWNc+2umBa37RReOGpi1MqaeuwASraadvAQBOwAgIAA8sDoMBj49uwwkoHRLwAAAAAA2Sdxj2cw6hqWClKEJjSWMNAACvYAFOwAVKzKNkoglgBiNGr/s972SLCBn9KPAHWLANGWLtyPgQCeYvQS4KQy9E6CcJAwDBhiVDrMCOgUGOwUeKYY6LZ2DO5C8F0R78vGqsU7xUtiMtjIUti6KNhK6upEaCYuyBr22NAUNLgAIt4AACLeFOykdErEdA7k8hZrs7qT6RezOvwX55pOvvQyCt78yFgGdCJklMAiIvq4apYo2DZK6qo05Ogi8Dz28t5MSGassAI22vZUyAC6gsAYNvyyXNq6GAAW/spotqw09jCIRJBiwN4Q8JpmAHaOQPzOfKLeUhS4GGy2DhISbIIgCjJ0cqwQPHqkpuxUwPYWFp4m/J6kks582Pru3ky0WKKGhCZMyMw2CCSiOhoA7GKy9s5y7rQuABDQ7GDU+AACOObgAvQmDsQg4Arc6hgc2v4C+tZ2oOQs+hAm0DDCTsge0EjMDhgkzghOpij4QuTcTphIANIy8AIc8sw44ADU5AQ0kgcBAABTYW1wbGVzIGJ5IE1ha3RvbmUAAAAAAgEAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAAEAEAACAAsAA4ACAAYABYAIAAIADwAAABGAAAAUAAAAFoAAABkAAAAbgAAAAAAIAAKACgAHgAYADIAIAA8ACAARgAgAFAAIABaACAAZAAgAG4AIAB4ACAAggAgAAYGAgMFAgMFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgAAAAAAAAAOAAAAQAABgAASU2FtcGxlcyBieSBNYWt0b25lICAgIAAAszIBOtXQ++799kC3""" 

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CableCalc(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(resource_path("icongg.ico")))
        self.setWindowTitle("CAA")
        self.resize(1100, 750)
        self.setStyleSheet("background-color: black; color: #23ff00; font-family: Consolas;")
        self.NEON_GREEN = "#23ff00"
        self.NEON_GREEN_DIM = "#0fa000"
        self.music_on = False
        self.music_temp_path = None

        self.build_ui()
        self.prepare_music_from_base64_string()
        
        # Avvia musica di default
        if PYGAME_AVAILABLE:
            self.toggle_music()

        # Pulsazioni estetiche
        self.logo_timer = QTimer()
        self.logo_timer.timeout.connect(self.logo_pulse_tick)
        self.logo_timer.start(400)
        self.entries_timer = QTimer()
        self.entries_timer.timeout.connect(self.pulse_entries_tick)
        self.entries_timer.start(460)

        atexit.register(self.cleanup)

    def build_ui(self):
        layout = QVBoxLayout(self)

        logo_ascii = r'''
..%%%%...%%%%%%..%%%%%%..%%%%%%...%%%%...%%..%%..%%%%%%...%%%%....%%%%...%%..%%..%%%%%%...%%%%...%%......%%%%%%..%%...%%..%%%%%%..%%..%%..%%%%%%...%%%%...%%%%%%..%%%%%%...%%%%...%%..%%..%%%%%%.
.%%......%%.........%%.....%%....%%..%%..%%%.%%..%%......%%..%%..%%..%%..%%..%%....%%....%%..%%..%%........%%....%%%.%%%..%%......%%%.%%....%%....%%..%%.....%%.....%%....%%..%%..%%%.%%..%%.....
..%%%%...%%%%......%%......%%....%%..%%..%%.%%%..%%%%....%%......%%%%%%..%%..%%....%%....%%%%%%..%%........%%....%%.%.%%..%%%%....%%.%%%....%%....%%%%%%....%%......%%....%%..%%..%%.%%%..%%%%...
.....%%..%%.......%%.......%%....%%..%%..%%..%%..%%......%%..%%..%%..%%...%%%%.....%%....%%..%%..%%........%%....%%...%%..%%......%%..%%....%%....%%..%%...%%.......%%....%%..%%..%%..%%..%%.....
..%%%%...%%%%%%..%%%%%%..%%%%%%...%%%%...%%..%%..%%%%%%...%%%%...%%..%%....%%....%%%%%%..%%..%%..%%%%%%..%%%%%%..%%...%%..%%%%%%..%%..%%....%%....%%..%%..%%%%%%..%%%%%%...%%%%...%%..%%..%%%%%%.
.................................................................................................................................................................................................
'''
        self.logo_label = QLabel(logo_ascii)
        self.logo_label.setFont(QFont("Consolas", 8, QFont.Weight.Bold))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)

        main_frame = QHBoxLayout()
        layout.addLayout(main_frame)

        # SINISTRA: INPUT
        self.left_frame = QVBoxLayout()
        main_frame.addLayout(self.left_frame, 1)

        self.entry_lunghezza = self.make_entry("Lunghezza cavo positivo (metri):", "5")
        self.entry_potenza = self.make_entry("Potenza RMS totale (W):", "3000")
        self.entry_deltav = self.make_entry("Caduta di tensione ammessa (V):", "0.5")
        self.entry_tensione = self.make_entry("Tensione nominale (V):", "12.8")

        self.left_frame.addWidget(QLabel("Classe amplificatore:"))
        self.combo_classe = QComboBox()
        self.combo_classe.addItems(["A","AB","D","T","G","H"])
        self.combo_classe.setCurrentIndex(2)
        self.style_combo(self.combo_classe)
        self.left_frame.addWidget(self.combo_classe)

        self.left_frame.addWidget(QLabel("Materiale conduttore:"))
        self.combo_materiale = QComboBox()
        self.combo_materiale.addItems(["OFC - Rame", "CCA - Alluminio ramato"])
        self.combo_materiale.setCurrentIndex(0)
        self.style_combo(self.combo_materiale)
        self.left_frame.addWidget(self.combo_materiale)

        self.left_frame.addWidget(QLabel("Utilizzo reale (musica/test):"))
        self.combo_utilizzo = QComboBox()
        self.combo_utilizzo.addItems(["10% - burning tesla mode", "20% - ", "30% - uso leggero", "40% - uso comune",
            "50% - ", "60% - uso intenso", "70% - ", "80% - ", "90% - SPL", "100% - segnale continuo (test)"])
        self.combo_utilizzo.setCurrentIndex(4)
        self.style_combo(self.combo_utilizzo)
        self.left_frame.addWidget(self.combo_utilizzo)

        self.left_frame.addWidget(QLabel("Metodo collegamento massa:"))
        self.massa_group = QButtonGroup()
        self.rb_battery = QRadioButton("Diretto a batteria (2×L)")
        self.rb_chassis = QRadioButton("Telaio auto (1.3×L)")
        self.rb_chassis.setChecked(True)
        for rb in [self.rb_battery, self.rb_chassis]:
            rb.setStyleSheet(f"color:{self.NEON_GREEN};")
            self.left_frame.addWidget(rb)
            self.massa_group.addButton(rb)

        self.calc_btn = self.make_neon_button(">>> GENERA ANALISI DATI <<<", self.calcola)
        self.left_frame.addWidget(self.calc_btn)
        self.music_btn = self.make_neon_button("Musica: ON", self.toggle_music)
        self.left_frame.addWidget(self.music_btn)

        # DESTRA: DASHBOARD
        self.right_frame = QVBoxLayout()
        main_frame.addLayout(self.right_frame, 1)

        self.right_frame.addWidget(QLabel("RISULTATI RAPIDI"))
        self.box_sezione = self.make_display_box("SEZIONE MINIMA TEORICA", "0.00", "mm²")
        self.right_frame.addWidget(self.box_sezione)

        grid = QGridLayout()
        self.box_corrente = self.make_display_box("CORRENTE STIMATA", "0.0", "A", font_size=18)
        self.box_farad = self.make_display_box("CAPACITÀ SUGGERITA", "0.0", "F", font_size=18)
        grid.addWidget(self.box_corrente, 0, 0)
        grid.addWidget(self.box_farad, 0, 1)
        self.right_frame.addLayout(grid)

        self.right_frame.addWidget(QLabel("REPORT TECNICO"))
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.text_output.setStyleSheet(f"background:#001100; color:{self.NEON_GREEN}; border: 1px solid #003300;")
        self.right_frame.addWidget(self.text_output)

    def make_display_box(self, title, value, unit, font_size=24):
        frame = QFrame()
        frame.setStyleSheet(f"border: 2px solid {self.NEON_GREEN_DIM}; background: #000800; border-radius: 5px;")
        v_box = QVBoxLayout(frame)
        lbl_t = QLabel(title)
        lbl_t.setStyleSheet("border:none; color:#0fa000; font-size: 10px; font-weight: bold;")
        lbl_v = QLabel(f"{value} {unit}")
        lbl_v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_v.setStyleSheet(f"border:none; color:{self.NEON_GREEN}; font-size: {font_size}pt; font-weight: bold;")
        lbl_v.setObjectName("val")
        v_box.addWidget(lbl_t)
        v_box.addWidget(lbl_v)
        return frame

    def make_entry(self, label_text, default=""):
        lbl = QLabel(label_text)
        lbl.setStyleSheet(f"color:{self.NEON_GREEN}; font-weight:bold;")
        self.left_frame.addWidget(lbl)
        e = QLineEdit()
        e.setStyleSheet(f"background:#001100; color:{self.NEON_GREEN}; border:1px solid #003300;")
        e.setText(default)
        self.left_frame.addWidget(e)
        return e

    def style_combo(self, combo):
        combo.setStyleSheet(f"background:#001100; color:{self.NEON_GREEN}; border:1px solid #003300; font-family:Consolas;")

    def make_neon_button(self, text, callback):
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        btn.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        btn.setStyleSheet(f"QPushButton {{ background-color: #001100; color: {self.NEON_GREEN}; border: 2px solid #003300; padding: 6px; }} QPushButton:hover {{ border-color:{self.NEON_GREEN}; }}")
        return btn

    def logo_pulse_tick(self):
        self.logo_label.setStyleSheet(f"color:{self.NEON_GREEN_DIM if random.random()<0.4 else self.NEON_GREEN};")

    def pulse_entries_tick(self):
        for e in [self.entry_lunghezza, self.entry_potenza, self.entry_deltav, self.entry_tensione]:
            e.setStyleSheet(f"background:#001100; color:{self.NEON_GREEN}; border:1px solid {self.NEON_GREEN if random.random()<0.25 else '#003300'};")

    def calcola(self):
        try:
            lunghezza = float(self.entry_lunghezza.text().replace(",", "."))
            potenza = float(self.entry_potenza.text().replace(",", "."))
            delta_v = float(self.entry_deltav.text().replace(",", "."))
            tensione = float(self.entry_tensione.text().replace(",", "."))
            
            utilizzo_text = self.combo_utilizzo.currentText()
            utilizzo = float(utilizzo_text.split("%")[0]) / 100.0

            eff_dict = {"A":0.25, "AB":0.55, "D":0.85, "T":0.80, "G":0.70, "H":0.80}
            eff = eff_dict.get(self.combo_classe.currentText(), 0.80)

            fattore_massa = 2.0 if self.rb_battery.isChecked() else 1.3
            lung_eff = lunghezza * fattore_massa

            rho = 0.0175 if "OFC" in self.combo_materiale.currentText() else 0.0280
            
            corrente = potenza / (tensione * eff) * utilizzo
            if corrente <= 0: raise ValueError
            
            r_max = delta_v / corrente
            sezione = (rho * lung_eff) / r_max
            farad = round(potenza / 1000, 2)

            # Update Dashboard
            self.box_sezione.findChild(QLabel, "val").setText(f"{sezione:.2f} mm²")
            self.box_corrente.findChild(QLabel, "val").setText(f"{corrente:.1f} A")
            self.box_farad.findChild(QLabel, "val").setText(f"{farad} F")

            res = (
                f"--- ANALISI CABLAGGIO ALIMENTAZIONE ---\n"
                f"Classe Amplificazione: {self.combo_classe.currentText()}\n"
                f"Efficienza stimata: {eff*100:.0f}%\n"
                f"Assorbimento medio stimato: {corrente:.1f} A\n"
                f"---------------------------------------\n"
                f"Resistività materiale: {rho} Ω·mm²/m\n"
                f"Lunghezza totale calcolata: {lung_eff:.1f} m\n"
                f"Caduta tensione target: {delta_v} V\n"
                f"---------------------------------------\n"
                f"SEZIONE MINIMA RICHIESTA: {sezione:.2f} mm²\n"
                f"CONDENSATORE CONSIGLIATO: {farad} Farad"
            )
            self.text_output.setPlainText(res)

        except:
            QMessageBox.critical(self, "Errore", "Valori inseriti non validi!")

    def prepare_music_from_base64_string(self):
        if not BASE64_XM.strip(): return
        try:
            raw = base64.b64decode("".join(BASE64_XM.split()))
            fd, path = tempfile.mkstemp(suffix=".xm")
            os.close(fd)
            with open(path, "wb") as f: f.write(raw)
            self.music_temp_path = path
        except: pass

    def toggle_music(self):
        if not PYGAME_AVAILABLE or not self.music_temp_path: return
        if self.music_on:
            pygame.mixer.music.stop()
            self.music_on = False
            self.music_btn.setText("Musica: OFF")
        else:
            try:
                if not pygame.mixer.get_init(): pygame.mixer.init()
                pygame.mixer.music.load(self.music_temp_path)
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
                self.music_on = True
                self.music_btn.setText("Musica: ON")
            except: pass

    def cleanup(self):
        if PYGAME_AVAILABLE:
            try: pygame.mixer.music.stop()
            except: pass
        if self.music_temp_path and os.path.exists(self.music_temp_path):
            try: os.remove(self.music_temp_path)
            except: pass

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = CableCalc()
    window.show()
    sys.exit(app.exec())