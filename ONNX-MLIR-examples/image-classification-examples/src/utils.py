
from tensorflow.keras.preprocessing.image import ImageDataGenerator    
from tensorflow.keras.layers import Dense
# from tensorflow.keras.layers import Conv2D,BatchNormalization, Dropout, Flatten, Dense,MaxPooling2D,MaxPool2D,SeparableConv2D,Input,LeakyReLU,concatenate,Activation
# from tensorflow.keras.optimizers import Adam, SGD
# from tensorflow.keras.initializers import Constant
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.regularizers import l2
# from tensorflow.keras.applications.resnet_v2 import ResNet50V2, ResNet101V2
import matplotlib.pyplot as plt
# import matplotlib.image as img
# import numpy as np
from PIL import Image

import random
import cv2
import os
import pickle
# import seaborn as sns 


from tensorflow.keras.applications.inception_v3 import InceptionV3
# from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
                                         
def view_image(path_image):                    
    """View image

    Args:
        path_image (_type_): path of the image to view
    """
    
    image = Image.open(path_image).convert("L")
    plt.imshow(image,cmap='gray')
    plt.show()
    

def load_data():
    """ loading dataset from datasets folder """
    img_gen = ImageDataGenerator(rescale=1./255)

    train_loader = img_gen.flow_from_directory(
        directory = 'chest_xray/train',target_size=(128,128),batch_size=50,seed=42
    )

    test_loader = img_gen.flow_from_directory(
        directory = 'chest_xray/test',target_size=(128,128),batch_size=50,seed=42
    )

    train_labels = train_loader.class_indices
    print(train_labels)

    test_labels = test_loader.class_indices

    return train_loader, test_loader, train_labels, test_labels



def build_model_InceptionV3():
    """build the InceptionV3 model"""
    base_model = InceptionV3(weights='imagenet', include_top=False)

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(2, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    
    for layer in base_model.layers:
        layer.trainable = False
    for i, layer in enumerate(base_model.layers):
        print(i, layer.name)

    for layer in model.layers[:249]:
        layer.trainable = False
    for layer in model.layers[249:]:
        layer.trainable = True

    return model


def plot_history(history):
    """Plot training history"""
    plt.subplots(figsize=(12,5))
    length = len(history['accuracy'])
    plt.plot(range(length),history['accuracy'], label = "Train Accuracy")
    plt.plot(range(length),history['val_accuracy'], label = "Validat Accuracy")
    # plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.title('Train accuracy VS Validation accuracy')
    plt.legend()

    plt.subplots(figsize=(12,5))
    plt.plot(range(length),history['loss'], label = "Train Loss")
    plt.plot(range(length),history['val_loss'], label = "Validation Loss")
    # plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title('Train Loss VS Validation Loss')
    plt.legend()
    plt.show()


def get_fig_axs(subplot_params):
    fig, axs = plt.subplots(
        nrows=subplot_params["nrows"], ncols=subplot_params["ncols"], 
        figsize=(subplot_params["figsize_col"], subplot_params["figsize_row"]),
        dpi=subplot_params["dpi"], facecolor=subplot_params["facecolor"], 
        edgecolor=subplot_params["edgecolor"], subplot_kw=subplot_params["subplot_kw"])
        
    return fig, axs


def show_predictions(y_img_batch, y_true, y_pred, subplot_params, plot_params, class_map, testing_dir,count=8, sample=True):
    fig, axs = get_fig_axs(subplot_params)
    plt.rcParams.update({'axes.titlesize': plot_params["axes.titlesize"]})
    plt.subplots_adjust(hspace=subplot_params["hspace"], wspace=subplot_params["wspace"])
    
    m = {}
    length = len(y_true)
    for i in range(0, count): 
        num = i
        if sample:
            num = random.randint(0, length-1)
            while num in m:
                num = int(random.randint(0, length-1))

            m[num]=1

            plt.subplot(subplot_params["nrows"], subplot_params["ncols"],i+1)
            img = cv2.imread(testing_dir, 1)
            plt.imshow(img)

            plt.xticks([])
            plt.yticks([])
                
            original = class_map[y_true[num]]
            predicted = class_map[y_pred[num]]  
                
            title_text = ("%s%s%s%s%s"%("True: ", original, "\n", "Pred: ", predicted))
                
            if original==predicted:
                plt.title(title_text)
            else:
                plt.title(title_text, color='red')

    plt.tight_layout()
    plt.show()


def plot_CXR_images(path):
    imgs = []
    valid_images = [".jpeg",".gif",".png",".tga"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        imgs.append(Image.open(os.path.join(path,f)))

    plt.figure(figsize=(15,9))

    for i in range(1,13):
        plt.subplot(3, 4, i)
        plt.imshow(imgs[i], cmap='gray')
        plt.xticks([])
        plt.yticks([])
    plt.show()

def plot_CXR_images_big(path="chest_xray/train/PNEUMONIA/",
                        count=6):
    imgs = []
    valid_images = [".jpeg",".gif",".png",".tga"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        imgs.append(Image.open(os.path.join(path,f)))
    for i in range(1,count):
        plt.figure(figsize=(15,9))
        plt.imshow(imgs[i], cmap='gray')
        plt.show()


def plot_history(path = "models/"):
    file_list = os.listdir(path)
    pkl_file_list = [f for f in file_list if '.pkl' in f]
    plt.subplots(figsize=(12,5))
    for i in pkl_file_list:
        with open(os.path.join(path,i), "rb") as file_pi:
            history_train = pickle.load(file_pi)
        length = len(history_train['accuracy'])
        plt.plot(range(length),history_train['accuracy'], label =i)
        plt.xlabel("Epochs")
        plt.ylabel("Accuracy")
        plt.title("Train Accuracy")
    plt.legend()
    plt.show()

    plt.subplots(figsize=(12,5))
    for i in pkl_file_list:
        with open(os.path.join(path,i), "rb") as file_pi:
            history_train = pickle.load(file_pi)
        length = len(history_train['loss'])
        plt.plot(range(length),history_train['loss'], label =i)
        plt.xlabel("Epochs")
        plt.ylabel("Loss")
        plt.title("Train Loss")
    plt.legend()
    plt.show()