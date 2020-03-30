# BigCloneBenchデータセットの準備方法
1. BCBのリレーション "clone" を csv形式(clone.csv)で保存
2. BCBのリレーション "functions" をcsv形式(functions.csv)で保存  
以上のリレーションを含むDB: <https://www.dropbox.com/s/z2k8r78l63r68os/BigCloneBench_BCEvalVersion.tar.gz?dl=0>

3. function_snippets.zip を解凍
4. classifier.py を実行し，parseErrorLog.txt が出力されていたらコメント等で行がずれている可能性があるので，DBを直接確認し，メソッドファイルを修正
5. preprocess.sh を実行

###注意事項
機能カテゴリ番号が43種類なのに対して，0~42で抜け番があるため，43->0, 44->1, 45->16に変更している．  
