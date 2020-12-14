import os
import logging
import sys

import moviepy.video.io.ImageSequenceClip

logging.basicConfig(
    filename='video_renderer.log',
    filemode='a',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

#####
# MAIN_FOLDER = '/Volumes/Wadkandata/________2020_Frissitopont_time_lapse'
MAIN_FOLDER = '/Users/wadkan/Downloads/test'
#####

OUTPUT_VIDEO_FORMAT = 'mp4'
IMG_FILE_FORMAT = 'jpg'
FPS = 24
output_folder_name = 'videos_done'
OUTPUT_FOLDER = str(f'{MAIN_FOLDER}/{output_folder_name}')


def get_if_use(folder_name):
    return folder_name[0] != '.' and not folder_name.endswith(OUTPUT_VIDEO_FORMAT) and folder_name != output_folder_name


def get_all_image_folders_list():
    image_folders_list = []
    date_folders = sorted(os.listdir(MAIN_FOLDER))
    # date_folders = glob.glob(f'{MAIN_FOLDER}/')
    for date_folder in date_folders:
        if get_if_use(date_folder):
            sub_folders = sorted(os.listdir(str(f'{MAIN_FOLDER}/{date_folder}')))
            for sub_folder in sub_folders:
                if get_if_use(sub_folder):
                    image_folder = str(f'{MAIN_FOLDER}/{date_folder}/{sub_folder}')
                    image_folders_list.append(image_folder)
    return image_folders_list


def get_missing_list():
    if not os.path.exists(MAIN_FOLDER):
        logging.error(f'Error with main folder - {e}')
        print('ERROR: Missing main folder.')
        sys.exit()

    # get all videos names in a list
    all_image_folders_list = get_all_image_folders_list()

    # get existing videos list
    try:
        if not os.path.exists(OUTPUT_FOLDER):
            os.mkdir(OUTPUT_FOLDER)
        done_video_list = sorted(os.listdir(OUTPUT_FOLDER))
        done_video_list_without_extension = [f"{MAIN_FOLDER}/{full_filename.split('.')[0].replace('_', '/')}" for full_filename in done_video_list]
    except Exception as e3:
        logging.error(f'Error at check output folder: - {e3}')

    return set(all_image_folders_list) - set(done_video_list_without_extension)


def get_temp_path_and_name(path, to_temp_back_back=False):
    temp_naming = '_temp_'
    head_and_tail = os.path.split(path)
    if not to_temp_back_back:
        return os.path.join(head_and_tail[0], f'{temp_naming}{head_and_tail[1]}')
    else:
        return os.path.join(head_and_tail[0], head_and_tail[1].replace(temp_naming, ''))


def rename_temp_after_completed(temp_name):
    try:
        new = get_temp_path_and_name(temp_name, True)
        os.rename(temp_name, new)
        logging.error(f'Rename {new} done.')
    except Exception as e3:
        logging.error(f'Error at renaming: – {e3}')


def remove_temp_files():
    temp_files_list = os.listdir(OUTPUT_FOLDER)
    for filename in temp_files_list:
        if os.path.split(filename)[1].startswith('_temp_'):
            os.remove(os.path.join(OUTPUT_FOLDER, filename))


def create_video_from_an_image_folder(image_folder, out_video_path_and_name, test_mode=False):
    temp_name = get_temp_path_and_name(out_video_path_and_name)
    print(f'Start rendering with folder: {image_folder} into {temp_name} ...')
    logging.info(f'Start rendering with folder: {image_folder} into {temp_name} ...')

    image_files = [str(image_folder + '/' + img) for img in os.listdir(image_folder) if img.endswith(f'.{IMG_FILE_FORMAT}')]
    image_files_sorted = sorted(image_files)

    if test_mode:
        [print(i) for i in image_files_sorted]
    else:
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files_sorted, fps=FPS)
        clip.write_videofile(temp_name)  # , codec='libx264'
        rename_temp_after_completed(temp_name)


if __name__ == '__main__':
    logging.info(f'----- APP Started ------')
    missing_folders_list = get_missing_list()
    if len(missing_folders_list) == 0:
        print('The videos are already done.')
        logging.info('The videos are already done.')
    else:
        # TODO: calculate needed space (video x 24.7 = imgs)
        # TODO: check and print whether we have enough space
        print(f'There are {len(missing_folders_list)} videos to render.')
        logging.info(f'There are {len(missing_folders_list)} videos to render.')

        options = [('s', 'Start conversation'),
                   ('i', 'Show img_files'),
                   ('r', 'remove temp files from output folder'),
                   ('e', 'Exit')
                   ]
        options_letters = [i[0] for i in options]
        print(options_letters)

        [print(f'{i[0]} - {i[1]}') for i in options]

        do_i_start = ''
        while do_i_start not in options_letters:

            do_i_start = input(' -->')

            if do_i_start not in options_letters:
                print('Incorrect answer.')
        if do_i_start == 'e':
            print('Bye then.')
        else:
            if do_i_start == 'r':
                remove_temp_files()
            elif do_i_start == 'i':
                TEST_MODE = True
                logging.info(f'-- SHOW IMAGES--')
            elif do_i_start == 's':
                TEST_MODE = False
                logging.info(f'-- START RENDERING--')

            for an_image_folder in missing_folders_list:
                try:
                    path_from_main = an_image_folder.replace(MAIN_FOLDER, '')
                    file_name_from_folders = path_from_main.replace('/', '_')[1:]
                    an_out_video_path_and_name = str(f'{OUTPUT_FOLDER}/{file_name_from_folders}.{OUTPUT_VIDEO_FORMAT}')
                    create_video_from_an_image_folder(an_image_folder, an_out_video_path_and_name, TEST_MODE)
                except Exception as e1:
                    error_msg = f'Error at {an_out_video_path_and_name} – {e1}.'
                    logging.error(error_msg)
                    # os.remove()
                    # except Exception as e2:
                    #     logging.error(f'Error at removing {an_out_video_path_and_name} – {e2}')
                else:
                    logging.info(f'{an_out_video_path_and_name} is done.')

# TODO: IF DONE and in the menu: merge all videos into one, and after clear small videos after a prompt.
