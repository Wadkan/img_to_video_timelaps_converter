import os
import logging
import shutil
import sys

import moviepy.video.io.ImageSequenceClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

logging.basicConfig(
    filename='video_renderer.log',
    filemode='a',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

#####
ROOT_FOLDER = '/Volumes/Wadkandata/________2020_Frissitopont_time_lapse'
# ROOT_FOLDER = '/Users/wadkan/Downloads/test'
#####

OUTPUT_VIDEO_FORMAT = 'mp4'
IMG_FILE_FORMAT = 'jpg'
FPS = 24
output_folder_name = 'videos_done'
OUTPUT_FOLDER = os.path.join(ROOT_FOLDER, output_folder_name)
TEMP_PREFIX = '_temp_'


def get_if_omg_is_correct(folder_name):
    return folder_name[0] != '.' and not folder_name.endswith(OUTPUT_VIDEO_FORMAT) and folder_name != output_folder_name


def get_all_image_folders_list():
    image_folders_list = []
    date_folders = sorted(os.listdir(ROOT_FOLDER))
    # date_folders = glob.glob(f'{MAIN_FOLDER}/')
    for date_folder in date_folders:
        if get_if_omg_is_correct(date_folder):
            sub_folders = sorted(os.listdir(os.path.join(ROOT_FOLDER, date_folder)))
            for sub_folder in sub_folders:
                if get_if_omg_is_correct(sub_folder):
                    image_folder = os.path.join(ROOT_FOLDER, date_folder, sub_folder)
                    image_folders_list.append(image_folder)
    return image_folders_list


def get_missing_list():
    if not os.path.exists(ROOT_FOLDER):
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
        done_video_list_without_extension = [f"{ROOT_FOLDER}/{full_filename.split('.')[0].replace('_', '/')}" for full_filename in done_video_list]
    except Exception as e3:
        logging.error(f'Error at check output folder: - {e3}')

    return sorted(list(set(all_image_folders_list) - set(done_video_list_without_extension)))


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
        logging.info(f'  rename OK {new}')
    except Exception as e3:
        logging.error(f'Error at renaming: – {e3}')


def print_and_log(msg00):
    print(msg00)
    logging.info(msg00)


def remove_temp_files():
    temp_files_list = os.listdir(OUTPUT_FOLDER)

    msg9 = f'  {len(temp_files_list)} will be removed.'
    print_and_log(msg9)

    for filename in temp_files_list:
        if os.path.split(filename)[1].startswith(TEMP_PREFIX):
            os.remove(os.path.join(OUTPUT_FOLDER, filename))


def create_video_from_an_image_folder(image_folder, out_video_path_and_name, test_mode=False):
    temp_name = get_temp_path_and_name(out_video_path_and_name)
    msg5 = f'Start rendering with folder: {image_folder} into {temp_name} ...'
    print_and_log(msg5)

    image_files = [str(image_folder + '/' + img) for img in os.listdir(image_folder) if img.endswith(f'.{IMG_FILE_FORMAT}')]
    image_files_sorted = sorted(image_files)

    if test_mode:
        [print(i) for i in image_files_sorted]
    else:
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files_sorted, fps=FPS)
        clip.write_videofile(temp_name)  # , codec='libx264'
        rename_temp_after_completed(temp_name)


def get_if_video_is_correct(file_name):
    return file_name[0] != '.' and file_name.endswith(f'.{OUTPUT_VIDEO_FORMAT}') and not file_name.startswith(TEMP_PREFIX)


def get_all_done_clips():
    all_clips_in_output_folder = os.listdir(OUTPUT_FOLDER)
    paths = []
    [paths.append(os.path.join(OUTPUT_FOLDER, video_file_name)) for video_file_name in all_clips_in_output_folder if get_if_video_is_correct(video_file_name)]
    sorted(paths)
    clips = []
    [clips.append(VideoFileClip(file_name)) for file_name in paths]
    return clips


def convert_all_images_into_clips(the_missing_folders_list):
    i = 1
    length = len(the_missing_folders_list)
    for an_image_folder in the_missing_folders_list:
        if not TEST_MODE:
            msg_remain = f'... START {i} / {length}'
            print_and_log(msg_remain)
            i += 1

        try:
            path_from_main = an_image_folder.replace(ROOT_FOLDER, '')
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
            logging.info(f'DONE - {an_out_video_path_and_name}')
    if not TEST_MODE:
        msg6 = 'All images converted.'
        print_and_log(msg6)


def concatenate_clips():
    # TODO: can choose: concatenate full videos, too
    full_file_name = f'full_video.{OUTPUT_VIDEO_FORMAT}'
    all_done_clips = get_all_done_clips()
    final_path = os.path.join(ROOT_FOLDER, OUTPUT_FOLDER, full_file_name)
    temp_name = get_temp_path_and_name(final_path)

    if len(all_done_clips) > 0:
        msg1 = f'START CONCATENATE {len(all_done_clips)} clips'
        print_and_log(msg1)
        final = concatenate_videoclips(all_done_clips, method='compose')
        final.write_videofile(temp_name)
        rename_temp_after_completed(temp_name)


def get_free_space():
    hard_drive = os.path.splitdrive(ROOT_FOLDER)[0]
    hard_drive = '/' if hard_drive == '' else hard_drive
    total, used, free = shutil.disk_usage(hard_drive)
    free_space = free // (2 ** 30)
    estimated_size = '??'

    message = f'Drive: {hard_drive}\n'
    message += f'{free_space} GigaByte - AVAILABLE SPACE\n'
    message += f'{estimated_size} GigaByte - ESTIMATED FILE SIZE'
    return message
    # print("Total: %d GiB" % (total // (2 ** 30)))
    # print("Used: %d GiB" % (used // (2 ** 30)))
    # print("Free: %d GiB" % (free // (2 ** 30)))


def do_sleep():
    if os.name == 'posix':  # for Linus
        os.system('shutdown -s now')


if __name__ == '__main__':
    try:
        msg = '----- APP Started ------'
        print_and_log(msg)
        missing_folders_list = get_missing_list()

        if len(missing_folders_list) == 0:
            msg = 'The videos are already done.'
            print_and_log(msg)
        else:
            msg = f'There are {len(missing_folders_list)} videos to render.'
            print_and_log(msg)

            options = [('s', 'Start conversation'),
                       ('ss', 'Start conversation and than sleep'),
                       ('i', 'Show img_files'),
                       ('r', 'remove temp files from output folder'),
                       ('+', 'Concatenating clips'),
                       ('g', 'Get free space - no working...'),
                       ('e', 'Exit')
                       ]
            options_letters = [i[0] for i in options]

            while True:
                print()
                [print(f'{i[0]} - {i[1]}') for i in options]
                do_i_start = input(' --> ')

                if do_i_start == 'ss':
                    msg8 = ' - sleep mode is active -'
                    print_and_log(msg8)

                if do_i_start not in options_letters:
                    print('Incorrect answer.')
                elif do_i_start == 'e':
                    print('Bye then.')
                    break
                elif do_i_start == 'r':
                    remove_temp_files()
                elif do_i_start == 'g':
                    print(get_free_space())
                elif do_i_start == '+':
                    concatenate_clips()
                elif do_i_start == 'i':
                    TEST_MODE = True
                    logging.info(f'-- SHOW IMAGES--')
                    convert_all_images_into_clips(missing_folders_list)
                elif do_i_start == 's' or do_i_start == 'ss':
                    TEST_MODE = False
                    logging.info(f'-- START RENDERING--')
                    convert_all_images_into_clips(missing_folders_list)

                if do_i_start == 'ss':
                    do_sleep()
    except Exception as ee:
        print(ee)
