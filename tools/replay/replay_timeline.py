import argparse
import time

from .loader import load_timeline
from .renderer import render_frame


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="timeline jsonl file")
    parser.add_argument("--sleep", type=float, default=0.0,
                        help="sleep seconds between frames")
    args = parser.parse_args()

    prev = None
    for frame in load_timeline(args.path):
        render_frame(frame, prev)
        prev = frame
        if args.sleep > 0:
            time.sleep(args.sleep)


if __name__ == "__main__":
    main()
