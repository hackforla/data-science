"""
Purpose: This is for processing multiple files of the same kind.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
import os
import glob


def multiple_files(filepath: str, filetype: str, process_function, session):
    """
    It processes multiple files of the same kind.

    :param filepath: the absolute filepath where files live.
    :param filetype: the type of files.
    :param process_function: the processing function being used.
    :param session: A SQLAlchemy session object.
    """
    # TODO: write tests
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.{}'.format(filetype)))
        for f in files:
            all_files.append(os.path.abspath(f))
    num_files = len(all_files)

    for i, datafile in enumerate(all_files, 1):
        process_function(
            datafile,
            session=session,
        )
        print('{}/{} files processed.'.format(i, num_files))
