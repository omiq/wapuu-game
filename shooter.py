import random
import arcade
import _thread


class Fireball(arcade.Sprite):
    def update(self):
        move_rate = 10
        self.center_y += move_rate


class Bad_Guy(arcade.Sprite):
    def update(self):

        drop_rate = random.randrange(-3, 2)
        lateral_rate = random.randrange(-2, 3)

        if lateral_rate > 1:
            rotation = random.randrange(0, 3)
        else:
            rotation = random.randrange(-3, 0)

        # do the moves
        self.center_y += drop_rate
        self.center_x += lateral_rate
        self.angle += rotation


class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > 800 - 1:
            self.right = 800 - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > 600 - 1:
            self.top = 600 - 1


class MyGame(arcade.Window):
    """ Main application class. """

    def sound(self, selected_sound):

        print(selected_sound)
        if selected_sound == "fart":
            arcade.sound.play_sound(self.fart_sound)
        else:
            arcade.sound.play_sound(self.boink_sound)

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(800, 600, "Shooter")

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemies_list = None
        self.fireball_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Sounds
        self.fart_sound = None
        self.boink_sound = None

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # BG
        self.line_start = -1

        # BG
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):

        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        self.fireball_list = arcade.SpriteList()

        # Set up the player
        self.score = 0

        # Sound Effects
        self.fart_sound = arcade.sound.load_sound("raspberry.wav")
        self.boink_sound = arcade.sound.load_sound("boink.wav")

        # Our hero
        self.player_sprite = arcade.Sprite("wapuu.png", 1)
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the enemies
        for i in range(60):

            # Create a bad_guy
            bad_guy = Bad_Guy("bug.png", 1)

            # Position the bad_guy
            bad_guy.center_x = random.randrange(800)
            bad_guy.center_y = random.randrange(500, 1500)

            # Add the bad_guy to the lists
            self.enemies_list.append(bad_guy)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # move the background
        if self.line_start < 49:
            self.line_start += 1
        else:
            self.line_start = 0


        # Draw all the sprites.
        self.enemies_list.draw()
        self.fireball_list.draw()
        self.player_sprite.draw()

        # Draw the score box
        arcade.draw_rectangle_filled(590, 520, 300, 80, (0, 0, 0, 150))

        # Draw the score text
        arcade.draw_text(f"Score: {self.score}", 498, 498, arcade.color.DARK_RED, 36)
        arcade.draw_text(f"Score: {self.score}", 500, 500, arcade.color.ORANGE_RED, 36)

    '''   
    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        #self.player_sprite.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
    '''



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        MOVEMENT_SPEED = 10

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            self.fireball()
        elif key == arcade.key.ESCAPE:
            exit()


    def fireball(self):
        """Fire phasers"""

        # Create a fireball
        fireball = Fireball("fireball.png", 1)

        # play sound. If sound is blocking (eg. on Linux), thread it
        # _thread.start_new_thread(self.sound, ("fart",))
        self.sound("fart")

        # rotate it.
        fireball.angle = random.randrange(-15, 15)

        # Position the fireball
        fireball.center_x = self.player_sprite.center_x
        fireball.bottom = self.player_sprite.top

        # Add the fireball to the appropriate lists
        self.fireball_list.append(fireball)


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on the enemies
        self.enemies_list.update()

        # Call update on Wapuu
        self.player_list.update()

        # Call update on fireball sprites
        self.fireball_list.update()

        # Loop through each fireball
        for fireball in self.fireball_list:

            # Check this fireball to see if it hit an enemy
            hit_list = arcade.check_for_collision_with_list(fireball, self.enemies_list)

            # If it did, get rid of the fireball
            if len(hit_list) > 0:
                # play sound
                _thread.start_new_thread(self.sound, ("boink",))

                # kill it
                fireball.kill()

            # For every enemy we hit, add to the score and remove the bad_guy
            for bad_guy in hit_list:
                bad_guy.kill()
                self.score += 1

            # If the fireball flies off-screen, remove it.
            if fireball.bottom > 600:
                fireball.kill()



def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
