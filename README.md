## 使用方法
### 予約のしかた
予約画面で検索ボックスに科目名か科目番号を入力  
科目の選択肢がでてくるので、クリックすると対応するスロットが表示される  

### 画面


## 初期設定
### DBの作成
python manage.py migrate  

### DBにkdbデータを登録する方法
ターミナルで python manage.py load_subjects kdb.json

### ユーザーを作成する方法
python manage.py createsuperuser

### ユーザーの科目データ(教える科目)を追加する方法
サイト内のプロフィールからアップロード可能
