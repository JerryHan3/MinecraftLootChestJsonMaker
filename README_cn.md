# 战利品表数据生成器

本工具用于为Minecraft Wiki的[Module:LootChest](https://zh.minecraft.wiki/w/Module:LootChest)生成所需数据。

> [!Warning]
> 本脚本生成的数据不兼容[英文Minecraft Wiki](https://minecraft.wiki)。

## 用法

1. 将 `JsonMaker.py` 文件和 `JsonMakerMap.json` 放到 `loot_table` 文件夹中。
2. 按下方所述调整映射表文件。
3. 执行 `JsonMaker.py` 脚本。脚本会将所有映射表中指定的文件夹中的战利品表合并在一起，按照文件名和映射表指定的后缀命名键，并根据键名按字母顺序进行排序。

脚本会生成 `result.json` 文件和 `structureList.txt` 文件，分别包含所生成的JSON数据和所有包含的结构名称。

### 映射表格式

映射表 `JsonMakerMap.json` 是一个复合数据列表，每一个条目需要包含以下键值对：

- `path`（必需）：指向目标文件夹的相对路径字符串。
- `suffix`（必需）：该文件夹内所有战利品表将要添加的后缀名。
- `overrides`（可选）：一段复合数据，键名为目标文件名，值为对该文件特别使用的后缀名。

仓库中包含的映射表是个人在[中文Minecraft Wiki](https://zh.minecraft.wiki)使用的规则。
