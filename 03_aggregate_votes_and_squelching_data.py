import pandas as pd
import requests

spreadsheet_ids = [
    {
        "gid": "1k9q2xMr6NIPVe2_akm9hZBeYB9fjbPRZeseooqRMrqw",
        "round": "zk",
    },
    {
        "gid": "1YlX95hOspQaGtr8yIK9K5oV8G-ZMT7FRGAquIFzvdt8",
        "round": "oss",
    },
    {
        "gid": "19XEb70_FUV7Xf1HLcAOgpkahYoUZsBUSgYWYNPgLeuw",
        "round": "infra",
    },
    {
        "gid": "1dq8hA3-o8bK0arfSvENaw1Yf05gdhdjs6ioG0hjvQR4",
        "round": "community",
    },
    {
        "gid": "1FuQX4piLMvc2lQBSzVbNeQ5Bzi4ooYs3NQd9f_3zrHA",
        "round": "climate",
    },
]

for spreadsheet in spreadsheet_ids:
    gid = spreadsheet["gid"]
    url = f"https://docs.google.com/spreadsheets/d/{gid}/export?format=csv"
    print(url, spreadsheet["round"])


dfs = [
    pd.read_csv("climate.csv"),
    pd.read_csv("community.csv"),
    pd.read_csv("infra.csv"),
    pd.read_csv("oss.csv"),
    pd.read_csv("zk.csv"),
]


combined_df = pd.concat(dfs, ignore_index=True)

validated_projects = combined_df[combined_df["coefficient"] == 1]


votes = pd.read_csv("votes_0x1b165fe4da6bc58ab8370ddc763d367d29f50ef0.csv")
breakpoint()
print(votes)
