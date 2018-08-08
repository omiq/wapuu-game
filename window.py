# https://makerhacks.com

import subprocess
import arcade

# Open the window. Set the window title and dimensions (width and height)
arcade.open_window(800, 600, "Drawing Test")
arcade.set_background_color(arcade.color.BLACK)


# render function that draws our stuff
def render(sprite_x=0, sprite_y=0, line_start=0, rot=0):
    # Start the render process
    arcade.start_render()

    # Draw vertical lines every 50 pixels
    for x in range(0, 800, 50):
        arcade.draw_line(x+line_start, 0, x+line_start, 600, arcade.color.BLUE_GRAY, 2)

    # Draw horizontal lines every 50 pixels
    for y in range(0, 600, 50):
        arcade.draw_line(0, y+line_start, 800, y+line_start, arcade.color.BLUEBERRY, 2)

    # Text
    arcade.draw_text("Loc: {}, {}".format(sprite_x, sprite_y), 50, 500, arcade.color.RED_ORANGE, 36)

    # Berry Textures
    texture = arcade.load_texture("raspberry.png")

    scale = 2  # 2x size

    arcade.draw_texture_rectangle(500, 600, scale * texture.width,
                                  scale * texture.height, texture, rot+0)

    arcade.draw_texture_rectangle(500, 500, scale * texture.width,
                                  scale * texture.height, texture, rot+23)

    arcade.draw_texture_rectangle(500, 400, scale * texture.width,
                                  scale * texture.height, texture, rot+45)

    arcade.draw_texture_rectangle(500, 300, scale * texture.width,
                                  scale * texture.height, texture, rot+68)

    arcade.draw_texture_rectangle(500, 200, scale * texture.width,
                                  scale * texture.height, texture, rot+90)

    arcade.draw_texture_rectangle(500, 100, scale * texture.width,
                                  scale * texture.height, texture, rot+112)

    arcade.draw_texture_rectangle(500, 0, scale * texture.width,
                                  scale * texture.height, texture, rot+135)

    # Sprites
    sprite = arcade.Sprite("raspberry.png", scale=1, center_x=sprite_x, center_y=sprite_y)
    sprite.draw()

    # Finish the render to show our work.
    arcade.finish_render()


# set up sprite coords
sprite_x = 100
sprite_y = 100
x_dir = 10
y_dir = 10
line_start = -1
rot = 0

# load sound effect - bug in the module on Ubuntu :(
fart_sound = arcade.sound.load_sound("raspberry.wav")

# loop forever
while 1:

    # bounce the berry
    if sprite_x == 750:
        arcade.sound.play_sound(fart_sound)
        x_dir = -10

    if sprite_x == 50:
        arcade.sound.play_sound(fart_sound)
        x_dir = 10

    if sprite_y == 550:
        arcade.sound.play_sound(fart_sound)
        y_dir = -10

    if sprite_y == 50:
        arcade.sound.play_sound(fart_sound)
        #subprocess.Popen(["aplay", "raspberry.wav"])
        y_dir = 10

    sprite_x += x_dir
    sprite_y += y_dir

    # move the background
    if line_start < 49:
        line_start += 1
    else:
        line_start = 0

    # rotation
    if rot < 359:
        rot += 1
    else:
        rot = 0

    # draw
    render(sprite_x, sprite_y, line_start, rot)

    # wait a little bit
    arcade.pause(0.05)
