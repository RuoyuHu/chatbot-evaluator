import os

from typing import List, Tuple


def load_dialog(target: str) -> List[Tuple[str, str]]:
    """
    Utility loader function for loading dialog files

    :param str      target: File/Directory to load conversation transcripts from
                            if target is a file, it can be loaded directly.
                            If target is a directory, this function returns all text
                            files from the directory

    :return:        List of Tuples of (file path, file name) for transcripts to be
                    loaded
    """
    eval_targets = []

    if os.path.isfile(target):
        target_name = os.path.basename(target)
        # Evaluate single conversation file
        eval_targets.append((target, target_name))

    elif os.path.isdir(target):
        # Evaluate all conversation transcripts from directory
        for target_name in os.listdir(target):
            if target_name.endswith('.txt'):
                eval_targets.append((os.path.join(target, target_name), target_name))

        print(f"Found Evaluation Targets:")
        for (_, target_name) in eval_targets:
            print(repr(target_name))

    return eval_targets
