import ZODB
import BTrees.OOBTree
import transaction

storage = ZODB.FileStorage.FileStorage('C:/.Phong/.kmitl/.year2/html/pr/SEWeb/data_storage/mydata.fs')

db = ZODB.DB(storage)
connection = db.open()
root = connection.root

# Check if 'users' exist in the root. If not, create it.
if not hasattr(root, 'users'):
    root.users = BTrees.OOBTree.BTree()

# Commit the transaction
transaction.commit()
