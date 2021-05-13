from keras.models import Model
from keras.layers import Input, Dense, Dropout, BatchNormalization, Conv2D, MaxPooling2D, AveragePooling2D, concatenate, \
    Activation, ZeroPadding2D, GlobalAveragePooling2D
from keras.layers import add, Flatten
from .MyModel import MyModel


class ResNet34(MyModel):

    def __init__(self, inputShape=(40, 120, 3), droprate=0.5, regularizer=0.01):
        super().__init__(inputShape=inputShape, droprate=droprate, regularizer=regularizer)

    def createModel(self):
        model_input = Input(shape=self.inputShape)
        x = ZeroPadding2D((3, 3))(model_input)
        # conv1
        x = Conv2d_BN(x, nb_filter=64, kernel_size=(7, 7), strides=(2, 2), padding='valid')
        x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)
        # conv2_x
        x = identity_Block(x, nb_filter=64, kernel_size=(3, 3))
        x = identity_Block(x, nb_filter=64, kernel_size=(3, 3))
        x = identity_Block(x, nb_filter=64, kernel_size=(3, 3))
        # conv3_x
        x = identity_Block(x, nb_filter=128, kernel_size=(3, 3), strides=(2, 2), with_conv_shortcut=True)
        x = identity_Block(x, nb_filter=128, kernel_size=(3, 3))
        x = identity_Block(x, nb_filter=128, kernel_size=(3, 3))
        x = identity_Block(x, nb_filter=128, kernel_size=(3, 3))
        # conv4_x
        x = identity_Block(x, nb_filter=256, kernel_size=(3, 3), strides=(2, 2), with_conv_shortcut=True)
        x = identity_Block(x, nb_filter=256, kernel_size=(3, 3))
        x = identity_Block(x, nb_filter=256, kernel_size=(3, 3))
        x = identity_Block(x, nb_filter=256, kernel_size=(3, 3))
        x = identity_Block(x, nb_filter=256, kernel_size=(3, 3))
        x = identity_Block(x, nb_filter=256, kernel_size=(3, 3))
        # conv5_x
        x = identity_Block(x, nb_filter=512, kernel_size=(3, 3), strides=(2, 2), with_conv_shortcut=True)
        x = identity_Block(x, nb_filter=512, kernel_size=(3, 3))
        x = identity_Block(x, nb_filter=512, kernel_size=(3, 3))
        x = GlobalAveragePooling2D()(x)

        """
        添加 top 分类器
        """
        model_output = self.top(self.droprate, self.regularizer, x)
        model = Model(inputs=model_input, outputs=model_output, name=self.__class__.__name__)
        return model


def Conv2d_BN(x, nb_filter, kernel_size, strides=(1, 1), padding='same', name=None):
    if name is not None:
        bn_name = name + '_bn'
        conv_name = name + '_conv'
    else:
        bn_name = None
        conv_name = None

    x = Conv2D(nb_filter, kernel_size, padding=padding, strides=strides, activation='relu', name=conv_name)(x)
    x = BatchNormalization(axis=3, name=bn_name)(x)
    return x


def identity_Block(inpt, nb_filter, kernel_size, strides=(1, 1), with_conv_shortcut=False):
    x = Conv2d_BN(inpt, nb_filter=nb_filter, kernel_size=kernel_size, strides=strides, padding='same')
    x = Conv2d_BN(x, nb_filter=nb_filter, kernel_size=kernel_size, padding='same')
    if with_conv_shortcut:
        shortcut = Conv2d_BN(inpt, nb_filter=nb_filter, strides=strides, kernel_size=kernel_size)
        x = add([x, shortcut])
        return x
    else:
        x = add([x, inpt])
        return x


def bottleneck_Block(inpt, nb_filters, strides=(1, 1), with_conv_shortcut=False):
    k1, k2, k3 = nb_filters
    x = Conv2d_BN(inpt, nb_filter=k1, kernel_size=1, strides=strides, padding='same')
    x = Conv2d_BN(x, nb_filter=k2, kernel_size=3, padding='same')
    x = Conv2d_BN(x, nb_filter=k3, kernel_size=1, padding='same')
    if with_conv_shortcut:
        shortcut = Conv2d_BN(inpt, nb_filter=k3, strides=strides, kernel_size=1)
        x = add([x, shortcut])
        return x
    else:
        x = add([x, inpt])
        return x
