import os
import logging

import moviepy.video.io.ImageSequenceClip

logging.basicConfig(
    filename='video_renderer.log',
    filemode='a',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

OUTPUT_VIDEO_FORMAT = 'mpg4'
IMG_FILE_FORMAT = 'jpg'
FPS = 24
# MAIN_FOLDER = '/Volumes/Wadkandata/________2020_Frissitopont_time_lapse'
MAIN_FOLDER = '/Users/wadkan/Downloads/test'
output_folder_name = 'videos_done'
OUTPUT_FOLDER = str(f'{MAIN_FOLDER}/{output_folder_name}')


def get_all_image_folders_list():
    image_folders_list = []
    date_folders = sorted(os.listdir(MAIN_FOLDER))
    # date_folders = glob.glob(f'{MAIN_FOLDER}/')
    for date_folder in date_folders:
        if date_folder[0] != '.' and date_folder != OUTPUT_FOLDER:
            sub_folders = sorted(os.listdir(str(f'{MAIN_FOLDER}/{date_folder}')))
            for sub_folder in sub_folders:
                if sub_folder[0] != '.':
                    image_folder = str(f'{MAIN_FOLDER}/{date_folder}/{sub_folder}')
                    image_folders_list.append(image_folder)
    return image_folders_list


def get_missing_list():
    if not os.path.exists(MAIN_FOLDER):
        logging.error()
        print("directory does not exist!")

    # get all videos names in a list
    all_image_folders_list = get_all_image_folders_list()
    # all_videos_list = [f'all_image_folder.{OUTPUT_VIDEO_FORMAT}' for all_image_folder in all_image_folders_list]

    # get existing videos list
    try:
        if not os.path.exists(OUTPUT_FOLDER):
            os.mkdir(OUTPUT_FOLDER)
        done_video_list = sorted(os.listdir(OUTPUT_FOLDER))
        done_video_list_without_extension = [full_filename.split('.')[0] for full_filename in done_video_list]
    except Exception as e3:
        logging.error(f'Error at check output folder: - {e3}')

    return set(all_image_folders_list) - set(done_video_list_without_extension)


# date_folder_folder = '20201117'
# sub_folder = '105MEDIA'


def create_video_from_an_image_folder(image_folder, out_video_path_and_name):
    image_files = [str(image_folder + '/' + img) for img in os.listdir(image_folder) if img.endswith(f'.{IMG_FILE_FORMAT}')]
    image_files_sorted = sorted(image_files)
    # clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files_sorted, fps=FPS)
    # clip.write_videofile(out_video_path_and_name)


if __name__ == '__main__':
    logging.info(f'----- Started ------')
    try:
        missing_folders_list = get_missing_list()
    except Exception as e:
        logging.error(f'Error with main folder - {e}')

for an_image_folder in missing_folders_list:
    try:
        an_out_video_path_and_name = str(f'{an_image_folder}.{OUTPUT_VIDEO_FORMAT}')
        create_video_from_an_image_folder(an_image_folder, an_out_video_path_and_name)
    except Exception as e1:
        error_msg = f'Error at {an_out_video_path_and_name} – {e1}.'
        logging.error(error_msg)
        try:
            os.remove()
        except Exception as e2:
            logging.error(f'Error at removing {an_out_video_path_and_name} – {e2}')
    else:
        logging.info(f'{an_out_video_path_and_name} is done.')
