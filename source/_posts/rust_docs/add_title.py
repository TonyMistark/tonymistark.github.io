import os
import time

cwd = os.getcwd()
print(f"{cwd=}")


def work_dir():
    for root, ds, files in os.walk(cwd):
        for file in files:
            abs_path = os.path.join(root, file)
            ts = os.path.getctime(abs_path)
            time_struct = time.localtime(ts)
            insert_text_head(abs_path)


def get_start_text(title, date_str):
    return [
        "---\n",
        f"title: {title}\n",
        f"date: {date_str}\n",
        "tags: Rust\n",
        "layout: Rust\n",
        "---\n",
    ]


def insert_text_head(path: str):
    print(f"start inset: {path=}")
    if not path.endswith(".md"):
        print(f"{path=} is not md file")
        return
    ts = os.path.getctime(path)
    time_struct = time.localtime(ts)
    date_str = time.strftime("%Y-%m-%d %H:%M:S", time_struct)
    with open(path, "r") as f:
        lines = f.readlines()
        start_line_index = 0
        for index, line in enumerate(lines):
            if line.startswith("#"):
                start_line_index = index
        lines = lines[start_line_index:]

        if len(lines) < 1:
            print(f"{path=} file empty")
            return
        print(f"{lines=}")
        title = lines[0]
        if not title.startswith("#"):
            print(f"{path=} there does not exist md #")
            return

        title = title.replace("#", "").strip()
        print(f"{title=}")

        head_lines = get_start_text(title, date_str)

    with open(path, "w") as f:
        f.writelines(head_lines + lines)
    print(f"{path} insert success")


if __name__ == "__main__":
    print("start script")
    work_dir()
