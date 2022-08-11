# color_decreaser
Python script to decrease a number of colors in image /n
When you run a script (PySimpleGUI user interface) it asks you to write an image file with extension (can be PNG, BMP, JPG with or without alpha) and the number of steps which is diference of colors by formula sqrt(a^2+b^2+c^2) < t where abc are rgb and t is step you enter in UI then it shows you original image and image with less colors on second window and you can save image with less colors (note that if image width is over 800 it would resize it in half both width and height)
