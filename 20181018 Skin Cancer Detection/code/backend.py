import tensorflow as tf
import numpy as np

model_path = r'C:\Users\Admin\Desktop\program\Projects\20181018 Skin Cancer Detection\saved model\architecture_V1\weights-improvement-36-0.80.hdf5'
#image_path = r'G:\cancer images\test_set\benign\benign_2.jpg'

def predict(image_path):
	# take image_path from front end

	model = tf.keras.models.load_model(model_path)
	model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

	test_image = tf.keras.preprocessing.image.load_img(image_path, target_size = (64, 64)) 
	test_image = tf.keras.preprocessing.image.img_to_array(test_image)
	test_image = np.expand_dims(test_image, axis = 0)

	result = model.predict(test_image)
	return result.item(0)

