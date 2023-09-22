import tensorflow as tf
from tensorflow.keras.applications import VGG19
from tensorflow.keras.models import Model

from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg19 import preprocess_input
from keras.applications.vgg19 import decode_predictions
base_model = VGG19(weights=None, include_top=True)  # 'weights=None' ensures that we only get the architecture
base_model.load_weights('./vgg19_weights_tf_dim_ordering_tf_kernels.h5')




def process_image(image):
    '''
    Make an image ready-to-use by VGG19
    '''
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the VGG model
    image = preprocess_input(image)

    return image

def predict_class(image):
    '''
    Predict and render the class of a given image 
    '''
    # predict the probability across all output classes
    yhat = base_model.predict(image)
    # convert the probabilities to class labels
    label = decode_predictions(yhat)
    # retrieve the most likely result, e.g. highest probability
    label = label[0][0]
    # return the classification
    prediction = label[1]
    percentage = '%.2f%%' % (label[2]*100)

    return prediction, percentage

if __name__ == '__main__':
    ''' for test'''
    # load an image from file
    image = load_img('../image.jpg', target_size=(224, 224))
    image = process_image(image)
    prediction, percentage = predict_class(image)
    print(prediction, percentage)