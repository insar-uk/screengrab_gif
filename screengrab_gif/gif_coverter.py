import imageio
import os


def create_gif(screenshot_folder: str, capture_duration: int = -1):
    # Get initial working directory
    initial_working_directory = os.getcwd()

    # Change the current working directory to the screenshot folder
    os.chdir(screenshot_folder)

    # Get the list of captured screenshots
    screenshot_files = sorted([f for f in os.listdir() if f.endswith(".png")])

    if len(screenshot_files) == 0:
        print("No screenshots found.")
        return

    # Create a GIF file name
    gif_file = "captured_screenshots.gif"

    # Create an empty list to store image frames
    frames = []

    # Read each screenshot file and append it to the frames list
    for screenshot_file in screenshot_files:
        image = imageio.imread(screenshot_file)
        frames.append(image)

    # Change the current working directory back to the initial working directory
    os.chdir(initial_working_directory)

    # Set the interval to acheive a close to real-time speed
    if capture_duration > 0:
        float_capture_interval = capture_duration / len(screenshot_files)
    else:
        float_capture_interval = 1

    # Save the frames as a GIF file, make sure it loops!
    imageio.mimsave(gif_file, frames, duration=float_capture_interval, loop=1)

    print(f"Saved the captured screenshots as {gif_file}.")

    # Delete the screenshot files
    for screenshot_file in screenshot_files:
        os.remove(os.path.join(screenshot_folder, screenshot_file))


if __name__ == '__main__':
    defaultPath = os.path.join(os.getcwd(), 'screenshots')
    create_gif(defaultPath)
