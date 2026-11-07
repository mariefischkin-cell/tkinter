
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models

print("TensorFlow version:", tf.__version__)

(x_train, y_train), (x_test, y_test) = (
    tf.keras.datasets.mnist.load_data()
)

x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

augmentation = tf.keras.Sequential([
    layers.RandomRotation(0.08),
    layers.RandomTranslation(0.1, 0.1),
    layers.RandomZoom(0.1)
])

def build_model(activation="relu", optimizer="adam"):
    model = models.Sequential([
        layers.Input(shape=(28, 28, 1)),
        augmentation,
        layers.Conv2D(32, 3, activation=activation),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation=activation),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation=activation),
        layers.Dropout(0.3),
        layers.Dense(10, activation="softmax")
    ])

    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

experiments = [
    ("ReLU + Adam", "relu", "adam"),
    ("Tanh + Adam", "tanh", "adam"),
    ("ReLU + RMSprop", "relu", "rmsprop")
]

results = {}
best_accuracy = 0
best_model = None

for name, activation, optimizer in experiments:
    print("\nTraining:", name)

    model = build_model(activation, optimizer)

    history = model.fit(
        x_train,
        y_train,
        epochs=3,
        batch_size=128,
        validation_split=0.1,
        verbose=1
    )

    loss, accuracy = model.evaluate(
        x_test, y_test, verbose=0
    )

    results[name] = accuracy

    print(name, "Accuracy:", round(accuracy * 100, 2), "%")

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model

best_model.save("best_mnist_model.keras")

print("\nEXPERIMENT RESULTS")

for name, accuracy in results.items():
    print(name, ":", round(accuracy * 100, 2), "%")

predictions = best_model.predict(x_test[:10], verbose=0)

plt.figure(figsize=(12, 5))

for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(x_test[i].squeeze(), cmap="gray")
    plt.title(
        "Predicted: " + str(np.argmax(predictions[i]))
    )
    plt.axis("off")

plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
plt.bar(results.keys(), [v * 100 for v in results.values()])
plt.ylabel("Test Accuracy (%)")
plt.title("MNIST Model Comparison")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()
