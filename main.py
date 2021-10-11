import arcade
import Instruction
import Window

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Captain Neckbeard: Perkins Cove")
    #Load launch screen:
    start_view = Instruction.BeginGameView()
    window.show_view(start_view)
    #begin:
    arcade.run()

if __name__ == '__main__':
    main()