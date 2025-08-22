
TRAIN_RATE = 0.75
VAL_RATE = 0.15
TEST_RATE = 0.1

from sklearn.model_selection import train_test_split
import shutil

def train_val_test_split(folder_root, dataset_root, type_index):
    """
    Split and save train/val/test set
    Input:
    - folder_root: folder_root containing mel-spec images
    - dataset_root: Directory to save dataset
    - type_root : train_root, val_root or test_root
    - type_index: class index in type_list
    """

    def save_set(subset, dataset_root, typeset, type_index):
      """
      Save X_train, X_val, X_test to their respective dir
      Input:
        - subset - X_train, X_val, X_test
        - dataset_root: Directory to save dataset
        - typeset - train, val, test
        - type index - Class index
      """
      # Copy file from subset to train/val/test folder
      for file in subset:
          srcpath = os.path.join(src_dir, file)
          dst_dir = dataset_root + "/" + typeset + "/{}".format(type_list[type_index][0])
          if not os.path.exists(dst_dir):
              os.makedirs(dst_dir)
          shutil.copy(srcpath, dst_dir)


    src_dir = folder_root + "/{}".format(type_list[type_index][0])
    X = os.listdir(src_dir)
    Y = ["{}".format(type_list[type_index][0]) for i in range(0, len(X))]
    # Train 75%, test 25%
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size= 1 - TRAIN_RATE, random_state=42, shuffle = True)
    # Val 15 %, test 10%
    X_val, X_test, Y_val, Y_test = train_test_split(X_test, Y_test, test_size = TEST_RATE / (TEST_RATE + VAL_RATE), random_state=42, shuffle = True)

    # Create dataset_root to save dataset
    if not os.path.exists(dataset_root):
        os.makedirs(dataset_root)
    # Save train/val/test of each class
    save_set(X_train, dataset_root, "train", type_index)
    save_set(X_val, dataset_root, "val", type_index)
    save_set(X_test, dataset_root, "test", type_index)

# Train/val/test_split for class "cailuong"
train_val_test_split(folder_root, dataset_root, 0)

# Train/val/test_split for class "catru"
train_val_test_split(folder_root, dataset_root, 1)

# Train/val/test_split for class "chauvan"
train_val_test_split(folder_root, dataset_root, 2)