from gpiozero import Button
from feederDB import reloadFeeder

button = Button(2)

while(True):
  button.wait_for_press()
  reloadFeeder("Button")