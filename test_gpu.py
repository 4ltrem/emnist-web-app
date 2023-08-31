import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
print(tf.test.gpu_device_name())

#https://ipg-automotive.com/en/support/support-request/faq/how-to-set-up-the-gpu-coding-interface-with-visual-studio-code-250/