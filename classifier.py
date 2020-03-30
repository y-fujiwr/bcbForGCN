import pandas as pd
import os,shutil
from pathlib import Path
import javalang

if os.path.exists("filenotfoundlog.txt"):
    os.remove("filenotfoundlog.txt")
if os.path.exists("parseErrorLog.txt"):
    os.remove("parseErrorLog.txt")

output_flag = True

#bcbのリレーション"clone"からクローンペアになっているメソッドのIDとカテゴリを抽出
df = pd.read_csv("clones.csv")
one = df.drop("FUNCTION_ID_TWO",axis=1)
one.columns=["id","category"]
two = df.drop("FUNCTION_ID_ONE",axis=1)
two.columns=["id","category"]
df2 = one.append(two,ignore_index=True)
result = df2.drop_duplicates()
probrem = result[result.duplicated(subset="id",keep=False)]
result = result.append(probrem).drop_duplicates(keep=False)
result.to_csv("id_category.csv",index=False)
probrem.to_csv("multicategory.csv",index=False)

#id_category.csv: メソッドIDとカテゴリのペア．マルチカテゴリのメソッドは除いてある
#multicategory.csv: マルチカテゴリのメソッドのIDとカテゴリのペア

FNFlist = []
for func_id, category in zip(result["id"],result["category"]):
    dirpath = "bcb_dataset/raw/{}".format(category)
    os.makedirs(dirpath,exist_ok=True)
    try:
        shutil.copy("{}/{}.java".format("function_snippets",func_id),"{}/{}.java".format(dirpath,func_id))

    #id.javaがfunction_snippets内に存在しない場合
    except FileNotFoundError:
        with open("filenotfoundlog.txt","a") as log:
            log.write("{}\n".format(func_id))
            FNFlist.append(func_id)

for func_id, category in zip(probrem["id"],probrem["category"]):
    dirpath = "bcb_dataset/multi/{}".format(category)
    os.makedirs(dirpath,exist_ok=True)
    try:
        shutil.copy("{}/{}.java".format("function_snippets",func_id),"{}/{}.java".format(dirpath,func_id))

    #id.javaがfunction_snippets内に存在しない場合
    except FileNotFoundError:
        with open("filenotfoundlog.txt","a") as log:
            log.write("{}\n".format(func_id))
            FNFlist.append(func_id)

if len(FNFlist) == 0:
    exit(1)

#function_snippets内に存在しないメソッドをbcbから抽出する
functions = pd.read_csv("functions.csv")
add_dirpath = "function_snippets/addition"
os.makedirs(add_dirpath,exist_ok=True)
for func_id in FNFlist:
    line = functions[functions["ID"]==func_id].iloc[0]
    add_func = list(Path("bcb_reduced").glob("**/{}".format(line["NAME"])))[0]
    with open(add_func,encoding="utf-8") as f:
        with open("{}/{}.java".format(add_dirpath,func_id),"w",encoding="utf-8") as output:
            output_flag = True
            code = "".join(f.readlines()[line["STARTLINE"]-1:line["ENDLINE"]])
            #コメント等で行がずれていないか確認
            def parse_program(func):
                try:
                    tokens = javalang.tokenizer.tokenize(func)
                    parser = javalang.parser.Parser(tokens)
                    tree = parser.parse_member_declaration()
                    return tree
                except Exception as e:
                    with open("parseErrorLog.txt","a",encoding="utf-8") as f:
                        f.write("{}_{}\n".format(func_id,type(e)))
                    output_flag = False
            parse_program(code)
            if output_flag == True:
                output.write(code)
