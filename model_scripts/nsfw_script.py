from env import root_path
from nsfw_model.nsfw_detector import predict
import os

from python_ai_utils.utils.download_util import download_file

model = None


def check_and_download_nsfw_model():
    nsfw_model_path = os.path.join(root_path, 'nsfw_mobilenet2.224x224.h5')
    url = 'https://s3.amazonaws.com/ir_public/nsfwjscdn/nsfw_mobilenet2.224x224.h5'
    if not os.path.exists(nsfw_model_path):
        if not download_file(url, root_path):
            return


def predict_simge_image(nd_image):
    global model
    if model is None:
        model = predict.load_model('./nsfw_mobilenet2.224x224.h5')
    list_result = predict.classify_nd(model, nd_image)
    if len(list_result) > 0:
        result = list_result[0]
        print(f'nsfw result {result}')
        return result

# Predict single image
# predict.classify(model, '2.jpg')
# {'2.jpg': {'sexy': 4.3454722e-05, 'neutral': 0.00026579265, 'porn': 0.0007733492, 'hentai': 0.14751932, 'drawings': 0.85139805}}

# Predict multiple images at once
# predict.classify(model, ['/Users/bedapudi/Desktop/2.jpg', '/Users/bedapudi/Desktop/6.jpg'])
# {'2.jpg': {'sexy': 4.3454795e-05, 'neutral': 0.00026579312, 'porn': 0.0007733498, 'hentai': 0.14751942, 'drawings': 0.8513979}, '6.jpg': {'drawings': 0.004214506, 'hentai': 0.013342537, 'neutral': 0.01834045, 'porn': 0.4431829, 'sexy': 0.5209196}}

# Predict for all images in a directory
# predict.classify(model, '/Users/bedapudi/Desktop/')
