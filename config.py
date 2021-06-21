import os

PREFIX_PATH = "E:\\Banggioi\\Ky8\\CSDL DPT\\code\\csdl-dpt-face-search"
DATA_PATH = os.path.join(PREFIX_PATH, "data")

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Phung06122910"
MYSQL_DATABASE = "csdl_dpt_search_img"

SQLALCHEMY_DATABASE_URL = "mysql://{}:{}@{}/{}".format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE)

CASCADE_PATH = "E:\\Banggioi\\Ky8\\CSDL DPT\\code\\csdl-dpt-face-search\\venv\\Lib\\site-packages\\cv2\\data"

HISTOGRAM_THRESHOLD = 15
HISTOGRAM_DIST_THRESHOLD = 70

MEAN_FRAME_THRESHOLD = 20
LEN_FRAME_THRESHOLD = 10


if __name__ == "__main__":
    print(DATA_PATH)