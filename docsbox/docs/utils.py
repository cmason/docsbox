import os
import zipfile

from shutil import copyfile

from wand.image import Image

from docsbox import app


def make_zip_archive(uuid, tmp_dir):
    """
    Creates ZIP archive from given @tmp_dir.
    """
    zipname = "{0}.zip".format(uuid)
    result_path = os.path.join(app.config["MEDIA_PATH"],
                               zipname)
    result_url = os.path.join(app.config["MEDIA_URL"],
                              zipname)
    with zipfile.ZipFile(result_path, "w") as output:
        for dirname, subdirs, files in os.walk(tmp_dir):
            for filename in files:
                path = os.path.join(dirname, filename)
                output.write(path, path.split(tmp_dir)[1])
    return result_path, result_url

def make_single_file(tmp_file, tmp_dir):
    result_path = os.path.join(app.config["MEDIA_PATH"], tmp_file)
    result_url = os.path.join(app.config["MEDIA_URL"], tmp_file)
    copyfile(os.path.join(tmp_dir, tmp_file), result_path)
    return result_path, result_url

def make_result_file(uuid, tmp_dir):
    tmp_files = os.listdir(tmp_dir)
    if len(tmp_files) == 1:
        return make_single_file(tmp_files.pop(), tmp_dir)
    else:
        return make_zip_archive(uuid, tmp_dir)


def make_thumbnails(image, tmp_dir, size):
    thumbnails_folder = os.path.join(tmp_dir, "thumbnails/")
    os.mkdir(thumbnails_folder)
    (width, height) = size
    for index, page in enumerate(image.sequence):
        with Image(page) as page:
            filename = os.path.join(thumbnails_folder, "{0}.png".format(index))
            page.resize(width, height)
            if app.config["THUMBNAILS_QUANTIZE"]:
                page.quantize(app.config["THUMBNAILS_QUANTIZE_COLORS"],
                              app.config["THUMBNAILS_QUANTIZE_COLORSPACE"], 0, True, True)
            page.save(filename=filename)
    else:
        image.close()
    return index
