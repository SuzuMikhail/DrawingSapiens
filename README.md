# DrawingSapiens
Ah~ Power of a pen~ inside my body~ (A open source illustrate software)

# The target of the project
A user-friendly illustrate software.

# All api I have tested
- pyglet (Surface pen is not supported, due to not implemented "Windows Ink API"
- pyqt5 (Surface pen is supported. Need open "Windows Ink" feature in driver settings when use tablet, or tablet will be abnormally. I think the problem is caused by wintab.h of Qt5, which is written by LCS/Telegraphics in 1998
- cgkit (Need python 3.3, so I not intend to use it)
- pySide2 (I have not enough space to install MSVC, so delayed)
