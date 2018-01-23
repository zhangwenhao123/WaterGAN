import os
import scipy.misc
import numpy as np
os.environ["CUDA_VISIBLE_DEVICES"]="0"
from model import WGAN
from utils import pp, visualize, to_json

import tensorflow as tf

flags = tf.app.flags
flags.DEFINE_integer("epoch", 26, "Epoch to train [25]")
flags.DEFINE_float("learning_rate", 0.0002, "Learning rate of for adam [0.0002]")
flags.DEFINE_float("beta1", 0.5, "Momentum term of adam [0.5]")
flags.DEFINE_integer("train_size", np.inf, "The size of train images [np.inf]")
flags.DEFINE_integer("batch_size", 64, "The size of batch images [64]")
flags.DEFINE_integer("input_height", 480, "The size of image to use (will be center cropped). [108]")
flags.DEFINE_integer("input_width", 640, "The size of image to use (will be center cropped). If None, same value as input_height [None]")
flags.DEFINE_integer("input_water_height",405, "The size of image to use (will be center cropped). [108]")  #1024
flags.DEFINE_integer("input_water_width", 720, "The size of image to use (will be center cropped). If None, same value as input_height [None]")  #1360
flags.DEFINE_integer("output_height", 48, "The size of the output images to produce [64]")
flags.DEFINE_integer("output_width", 64, "The size of the output images to produce. If None, same value as output_height [None]")
flags.DEFINE_integer("c_dim", 3, "Dimension of image color. [3]")
flags.DEFINE_float("max_depth", 2.5, "Dimension of image color. [3.0]")
flags.DEFINE_string("water_dataset", "mini", "The name of dataset [celebA, mnist, lsun]")
flags.DEFINE_string("air_dataset","air_images","The name of dataset with air images")
flags.DEFINE_string("depth_dataset","air_depth","The name of dataset with depth images")
flags.DEFINE_string("input_fname_pattern", "*.*", "Glob pattern of filename of input images [*]")
flags.DEFINE_string("checkpoint_dir", "checkpoint", "Directory name to save the checkpoints [checkpoint]")
flags.DEFINE_string("results_dir", "results", "Directory name to save the checkpoints [results]")
flags.DEFINE_string("sample_dir", "samples", "Directory name to save the image samples [samples]")
flags.DEFINE_boolean("is_train", True, "True for training, False for testing [False]")
flags.DEFINE_boolean("is_crop", True, "True for training, False for testing [False]")
flags.DEFINE_boolean("visualize", False, "True for visualizing, False for nothing [False]")
flags.DEFINE_integer("num_samples",64, "True for visualizing, False for nothing [4000]")
flags.DEFINE_integer("save_epoch",25, "The size of the output images to produce. If None, same value as output_height [None]")
FLAGS = flags.FLAGS

def main(_):
  pp.pprint(flags.FLAGS.__flags)

  if FLAGS.input_width is None:
    FLAGS.input_width = FLAGS.input_height
  if FLAGS.output_width is None:
    FLAGS.output_width = FLAGS.output_height

  if not os.path.exists(FLAGS.checkpoint_dir):
    os.makedirs(FLAGS.checkpoint_dir)
  if not os.path.exists(FLAGS.sample_dir):
    os.makedirs(FLAGS.sample_dir)

  run_config = tf.ConfigProto()
  run_config.gpu_options.allow_growth=True
  with tf.Session(config=run_config) as sess:
    wgan = WGAN(
      sess,
      input_width=FLAGS.input_width,
      input_height=FLAGS.input_height,
      input_water_width=FLAGS.input_water_width,
      input_water_height=FLAGS.input_water_height,
      output_width=FLAGS.output_width,
      output_height=FLAGS.output_height,
      batch_size=FLAGS.batch_size,
      c_dim=FLAGS.c_dim,
      max_depth = FLAGS.max_depth,
      save_epoch=FLAGS.save_epoch,
      water_dataset_name=FLAGS.water_dataset,
      air_dataset_name = FLAGS.air_dataset,
      depth_dataset_name = FLAGS.depth_dataset,
      input_fname_pattern=FLAGS.input_fname_pattern,
      is_crop=FLAGS.is_crop,
      checkpoint_dir=FLAGS.checkpoint_dir,
      results_dir = FLAGS.results_dir,
      sample_dir=FLAGS.sample_dir,
      num_samples = FLAGS.num_samples)

    if FLAGS.is_train:
      wgan.train(FLAGS)
    else:
      if not wgan.load(FLAGS.checkpoint_dir):
        raise Exception("[!] Train a model first, then run test mode")
      wgan.test(FLAGS)

    # to_json("./web/js/layers.js", [wgan.h0_w, wgan.h0_b, wgan.g_bn0],
    #                 [wgan.h1_w, wgan.h1_b, wgan.g_bn1],
    #                 [wgan.h2_w, wgan.h2_b, wgan.g_bn2],
    #                 [wgan.h3_w, wgan.h3_b, wgan.g_bn3],
    #                 [wgan.h4_w, wgan.h4_b, None])

    # Below is codes for visualization
    #OPTION = 1
    #visualize(sess, wgan, FLAGS, OPTION)

if __name__ == '__main__':
  tf.app.run()
