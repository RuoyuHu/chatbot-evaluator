import re
import os

"""
Plugin for processing raw dialog transcripts into a framework-accepted format, typically

[NAME][DELIM][UTTERANCE] i.e. "BOT__SAID__Hello world"


[Quick Start]

1. Drag and drop this file into your working directory i.e. example/
2. Change the 'src_dir' and 'tar_dir' variables to where to read the raw transcriptions,
   and where to save the preprocessed text files respectively. The paths should be
   relative to where the script is run.
3. Run the script

    python3 preprocess.py


!!! Make sure the 'name_maps' object has the correct names corresponding to your Actor
    names
"""

FIND_NAMES = r"\n(\w+)\s?:"

def main():
    src_dir = "example_conversation"
    tar_dir = "example_conversation_preprocessed"
    delim = "__SAID__"

    src_files = os.listdir(src_dir)

    for src_file in src_files:

        path = os.path.join(src_dir, src_file)
        block = open(path, 'r').read()
        print(f"Preprocessing \'{path}\'")

        names = list(set(re.findall(FIND_NAMES, block)))
        print(f"Found Names: {repr(names)}")

        botname = "Eve"
        if botname in names and len(names) == 2:
            botname = names.index(botname)
            print(f"Detected Botname as {repr(names[botname])}")
            username = names.index((names[:botname] + names[botname + 1:])[0])
            print(f"Detected User name as {repr(names[username])}")
        else:
            botname = int(input(f"Botname is {', '.join(['[' + str(i + 1) + ']' + names[i] for i in range(len(names))])}\n>"))
            botname -= 1
            username = int(input(f"Username is {', '.join(['[' + str(i + 1) + ']' + names[i] for i in range(len(names))])}\n>"))
            username -= 1

        name_maps = {
            names[botname]: "BOT",
            names[username]: "USER"
        }

        lines = block.splitlines()
        line_count = len(lines)

        # remove empty lines
        lines = list(filter(lambda x: len(x) > 0, lines))
        print(f"Removed {line_count - len(lines)} empty lines")

        for i, line in enumerate(list(lines)):
            if len(re.findall(r"^\w+:\s?", line)) == 0:
                # Line is not conversation
                lines[i] = ''
                continue

            find_inset_name = re.compile(f"({'|'.join(names)})([: ,\\.!\\?\\n]|$)")
            inset_names = re.findall(find_inset_name, line)
            new_line = line
            for (inset_name, suff) in inset_names:
                repl_name = f"{name_maps[inset_name]}{suff}"
                (new_line, _) = re.subn(find_inset_name, repl_name, new_line, count=1)

            replace_speaker = f"\\1{delim}"
            new_line = re.sub(r"^(\w+):\s?", replace_speaker, new_line)
            lines[i] = new_line

        lines = list(filter(lambda x: len(x) > 0, lines))

        transcript = '\n'.join(lines)

        if not os.path.exists(tar_dir):
            os.mkdir(tar_dir)

        tar_file = open(os.path.join(tar_dir, src_file), 'w')
        tar_file.write(transcript)
        tar_file.close()


if __name__ == "__main__":
    main()
