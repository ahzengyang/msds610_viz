"""Example: the default theme vs. the "chinese" theme.

Same data and the same ``cp.boxplot(...)`` call each time — only ``theme=``
changes. Run from the project root (after ``pip install -e .``):

    python examples/theme_demo.py

Writes three PNGs into ``examples/``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import cleanplot as cp

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "section_scores.csv"


def main():
    df = pd.read_csv(DATA)

    # 1) Default theme.
    ax = cp.boxplot(df, column="score", by="section",
                    highlight="Section C", title="Default theme")
    ax.figure.savefig(HERE / "theme_default.png")
    plt.close(ax.figure)

    # 2) Chinese theme — identical call, only theme= differs.
    ax = cp.boxplot(df, column="score", by="section", theme="chinese",
                    highlight="Section C", title="Chinese theme (中国风)")
    ax.figure.savefig(HERE / "theme_chinese.png")
    plt.close(ax.figure)

    # 3) Chinese theme with Chinese labels — no font setup needed.
    zh = {"Section A": "甲班", "Section B": "乙班",
          "Section C": "丙班", "Section D": "丁班"}
    df_zh = df.assign(班级=df["section"].map(zh)).rename(columns={"score": "考试成绩"})
    ax = cp.boxplot(df_zh, column="考试成绩", by="班级", theme="chinese",
                    highlight="丙班", title="各班级考试成绩分布")
    ax.figure.savefig(HERE / "theme_chinese_zh.png")
    plt.close(ax.figure)

    print("Saved theme_default.png, theme_chinese.png, theme_chinese_zh.png")


if __name__ == "__main__":
    main()
