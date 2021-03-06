from keras.datasets import imdb
from keras.preprocessing import sequence
from keras import models
from keras import layers
from keras import optimizers
from keras import losses
from keras import metrics
from keras import activations
import matplotlib.pyplot as plt


max_feature = 10000
max_len = 500

(train_x, train_y), (test_x, test_y) = imdb.load_data(num_words=max_feature)

train_x = sequence.pad_sequences(train_x, maxlen=max_len)
test_x = sequence.pad_sequences(test_x, maxlen=max_len)

network = models.Sequential()
network.add(layers.Embedding(max_feature, 128, input_shape=(max_len, )))

# 32个卷积核，每个卷积核长度7（可以扫描序列中7个向量）
network.add(layers.Conv1D(64, 7, activation=activations.relu))

network.add(layers.MaxPool1D(5))
network.add(layers.Conv1D(64, 7, activation=activations.relu))
network.add(layers.MaxPool1D(5))
network.add(layers.Flatten())
network.add(layers.Dense(1, activation=activations.sigmoid))

network.compile(optimizer=optimizers.RMSprop(),
                loss=losses.binary_crossentropy,
                metrics=[metrics.binary_accuracy])

print(network.summary())

history = network.fit(x=train_x, y=train_y,
                      epochs=10,
                      batch_size=128,
                      validation_split=0.2)

accuracy = history.history['binary_accuracy']
val_accuracy = history.history['val_binary_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epoch = range(1, len(accuracy) + 1)

# 绘制loss趋势图
ax_loss = plt.figure(figsize=(9, 9)).gca()
ax_loss.plot(epoch, loss, color='b', marker='>', linestyle='-', label='Loss')
ax_loss.plot(epoch, val_loss, color='r', marker='o', linestyle=':', label='Vla_Loss')
ax_loss.set_title('Loss')
ax_loss.set_xlabel('epoch')
ax_loss.set_ylabel('loss')
ax_loss.legend()

# 绘制准确率趋势图
ax_acc = plt.figure(figsize=(9, 9)).gca()
ax_acc.plot(epoch, accuracy, color='b', marker='*', linestyle='--', label='Accuracy')
ax_acc.plot(epoch, val_accuracy, color='r', marker='o', linestyle='-.', label='Val_Accuracy')
ax_acc.set_title('Accuracy')
ax_acc.set_xlabel('epoch')
ax_acc.set_ylabel('accuracy')
ax_acc.legend()

plt.show()


















































