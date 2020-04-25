"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=images/train_labels.csv --image_dir=images/train --output_path=train.record
  # Create test data:
  python generate_tfrecord.py --csv_input=images/test_labels.csv  --image_dir=images/test --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

flags =  tf.compat.v1.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('image_dir', '', 'Path to the image directory')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS


# TO-DO replace this with label map
# Edit this function to train on your custom dataset
def class_text_to_int(row_label):
    if row_label == 'AM General Hummer SUV':
        return 1
    elif row_label == 'Acura RL Sedan':
        return 2
    elif row_label == 'Acura TL Sedan':
        return 3
    elif row_label == 'Acura TL Type-S':
        return 4
    elif row_label == 'Acura TSX Sedan':
        return 5
    elif row_label == 'Acura Integra Type R':
        return 6
    elif row_label == 'Acura ZDX Hatchback':
        return 7
    elif row_label == 'Aston Martin V8 Vantage Convertible':
        return 8
    elif row_label == 'Aston Martin V8 Vantage Coupe':
        return 9
    elif row_label == 'Aston Martin Virage Convertible':
        return 10
    elif row_label == 'Aston Martin Virage Coupe':
        return 11
    elif row_label == 'Audi RS 4 Convertible':
        return 12
    elif row_label == 'Audi A5 Coupe':
        return 13
    elif row_label == 'Audi TTS Coupe':
        return 14
    elif row_label == 'Audi R8 Coupe':
        return 15
    elif row_label == 'Audi V8 Sedan':
        return 16
    elif row_label == 'Audi 100 Sedan':
        return 17
    elif row_label == 'Audi 100 Wagon':
        return 18
    elif row_label == 'Audi TT Hatchback':
        return 19
    elif row_label == 'Audi S6 Sedan':
        return 20
    elif row_label == 'Audi S5 Convertible':
        return 21
    elif row_label == 'Audi S5 Coupe':
        return 22
    elif row_label == 'Audi S4 Sedan':
        return 23
    elif row_label == 'Audi TT RS Coupe':
        return 24
    elif row_label == 'BMW ActiveHybrid 5 Sedan':
        return 25
    elif row_label == 'BMW 1 Series Convertible':
        return 26
    elif row_label == 'BMW 1 Series Coupe':
        return 27
    elif row_label == 'BMW 3 Series Sedan':
        return 28
    elif row_label == 'BMW 3 Series Wagon':
        return 29
    elif row_label == 'BMW 6 Series Convertible':
        return 30
    elif row_label == 'BMW X5 SUV':
        return 31
    elif row_label == 'BMW X6 SUV':
        return 32
    elif row_label == 'BMW M3 Coupe':
        return 33
    elif row_label == 'BMW M5 Sedan':
        return 34
    elif row_label == 'BMW M6 Convertible':
        return 35
    elif row_label == 'BMW X3 SUV':
        return 36
    elif row_label == 'BMW Z4 Convertible':
        return 37
    elif row_label == 'Bentley Continental Supersports Conv. Convertible':
        return 38
    elif row_label == 'Bentley Arnage Sedan':
        return 39
    elif row_label == 'Bentley Mulsanne Sedan':
        return 40
    elif row_label == 'Bentley Continental GT Coupe':
        return 41
    elif row_label == 'Bentley Continental Flying Spur Sedan':
        return 42
    elif row_label == 'Bugatti Veyron 16.4 Convertible':
        return 43
    elif row_label == 'Bugatti Veyron 16.4 Coupe':
        return 44
    elif row_label == 'Buick Regal GS':
        return 45
    elif row_label == 'Buick Rainier SUV':
        return 46
    elif row_label == 'Buick Verano Sedan':
        return 47
    elif row_label == 'Buick Enclave SUV':
        return 48
    elif row_label == 'Cadillac CTS-V Sedan':
        return 49
    elif row_label == 'Cadillac SRX SUV':
        return 50
    elif row_label == 'Cadillac Escalade EXT Crew Cab':
        return 51
    elif row_label == 'Chevrolet Silverado 1500 Hybrid Crew Cab':
        return 52
    elif row_label == 'Chevrolet Corvette Convertible':
        return 53
    elif row_label == 'Chevrolet Corvette ZR1':
        return 54
    elif row_label == 'Chevrolet Corvette Ron Fellows Edition Z06':
        return 55
    elif row_label == 'Chevrolet Traverse SUV':
        return 56
    elif row_label == 'Chevrolet Camaro Convertible':
        return 57
    elif row_label == 'Chevrolet HHR SS':
        return 58
    elif row_label == 'Chevrolet Impala Sedan':
        return 59
    elif row_label == 'Chevrolet Tahoe Hybrid SUV':
        return 60
    elif row_label == 'Chevrolet Sonic Sedan':
        return 61
    elif row_label == 'Chevrolet Express Cargo Van':
        return 62
    elif row_label == 'Chevrolet Avalanche Crew Cab':
        return 63
    elif row_label == 'Chevrolet Cobalt SS':
        return 64
    elif row_label == 'Chevrolet Malibu Hybrid Sedan':
        return 65
    elif row_label == 'Chevrolet TrailBlazer SS':
        return 66
    elif row_label == 'Chevrolet Silverado 2500HD Regular Cab':
        return 67
    elif row_label == 'Chevrolet Silverado 1500 Classic Extended Cab':
        return 68
    elif row_label == 'Chevrolet Express Van':
        return 69
    elif row_label == 'Chevrolet Monte Carlo Coupe':
        return 70
    elif row_label == 'Chevrolet Malibu Sedan':
        return 71
    elif row_label == 'Chevrolet Silverado 1500 Extended Cab':
        return 72
    elif row_label == 'Chevrolet Silverado 1500 Regular Cab':
        return 73
    elif row_label == 'Chrysler Aspen SUV':
        return 74
    elif row_label == 'Chrysler Sebring Convertible':
        return 75
    elif row_label == 'Chrysler Town and Country Minivan':
        return 76
    elif row_label == 'Chrysler 300 SRT-8':
        return 77
    elif row_label == 'Chrysler Crossfire Convertible':
        return 78
    elif row_label == 'Chrysler PT Cruiser Convertible':
        return 79
    elif row_label == 'Daewoo Nubira Wagon':
        return 80
    elif row_label == 'Dodge Caliber Wagon':
        return 81
    elif row_label == 'Dodge Caravan Minivan':
        return 82
    elif row_label == 'Dodge Ram Pickup 3500 Crew Cab':
        return 83
    elif row_label == 'Dodge Ram Pickup 3500 Quad Cab':
        return 84
    elif row_label == 'Dodge Sprinter Cargo Van':
        return 85
    elif row_label == 'Dodge Journey SUV':
        return 86
    elif row_label == 'Dodge Dakota Crew Cab':
        return 87
    elif row_label == 'Dodge Dakota Club Cab':
        return 88
    elif row_label == 'Dodge Magnum Wagon':
        return 89
    elif row_label == 'Dodge Challenger SRT8':
        return 90
    elif row_label == 'Dodge Durango SUV':
        return 91
    elif row_label == 'Dodge Charger Sedan':
        return 92
    elif row_label == 'Dodge Charger SRT-8':
        return 93
    elif row_label == 'Eagle Talon Hatchback':
        return 94
    elif row_label == 'FIAT 500 Abarth':
        return 95
    elif row_label == 'FIAT 500 Convertible':
        return 96
    elif row_label == 'Ferrari FF Coupe':
        return 97
    elif row_label == 'Ferrari California Convertible':
        return 98
    elif row_label == 'Ferrari 458 Italia Convertible':
        return 99
    elif row_label == 'Ferrari 458 Italia Coupe':
        return 100
    elif row_label == 'Fisker Karma Sedan':
        return 101
    elif row_label == 'Ford F-450 Super Duty Crew Cab':
        return 102
    elif row_label == 'Ford Mustang Convertible':
        return 103
    elif row_label == 'Ford Freestar Minivan':
        return 104
    elif row_label == 'Ford Expedition EL SUV':
        return 105
    elif row_label == 'Ford Edge SUV':
        return 106
    elif row_label == 'Ford Ranger SuperCab':
        return 107
    elif row_label == 'Ford GT Coupe':
        return 108
    elif row_label == 'Ford F-150 Regular Cab':
        return 109
    elif row_label == 'Ford Focus Sedan':
        return 110
    elif row_label == 'Ford E-Series Wagon Van':
        return 111
    elif row_label == 'Ford Fiesta Sedan':
        return 112
    elif row_label == 'GMC Terrain SUV':
        return 113
    elif row_label == 'GMC Savana Van':
        return 114
    elif row_label == 'GMC Yukon Hybrid SUV':
        return 115
    elif row_label == 'GMC Acadia SUV':
        return 116
    elif row_label == 'GMC Canyon Extended Cab':
        return 117
    elif row_label == 'Geo Metro Convertible':
        return 118
    elif row_label == 'HUMMER H3T Crew Cab':
        return 119
    elif row_label == 'HUMMER H2 SUT Crew Cab':
        return 120
    elif row_label == 'Honda Odyssey Minivan':
        return 121
    elif row_label == 'Honda Accord Coupe':
        return 122
    elif row_label == 'Honda Accord Sedan':
        return 123
    elif row_label == 'Hyundai Veloster Hatchback':
        return 124
    elif row_label == 'Hyundai Santa Fe SUV':
        return 125
    elif row_label == 'Hyundai Tucson SUV':
        return 126
    elif row_label == 'Hyundai Veracruz SUV':
        return 127
    elif row_label == 'Hyundai Sonata Hybrid Sedan':
        return 128
    elif row_label == 'Hyundai Elantra Sedan':
        return 129
    elif row_label == 'Hyundai Accent Sedan':
        return 130
    elif row_label == 'Hyundai Genesis Sedan':
        return 131
    elif row_label == 'Hyundai Sonata Sedan':
        return 132
    elif row_label == 'Hyundai Elantra Touring Hatchback':
        return 133
    elif row_label == 'Hyundai Azera Sedan':
        return 134
    elif row_label == 'Infiniti G Coupe IPL':
        return 135
    elif row_label == 'Infiniti QX56 SUV':
        return 136
    elif row_label == 'Isuzu Ascender SUV':
        return 137
    elif row_label == 'Jaguar XK XKR':
        return 138
    elif row_label == 'Jeep Patriot SUV':
        return 139
    elif row_label == 'Jeep Wrangler SUV':
        return 140
    elif row_label == 'Jeep Liberty SUV':
        return 141
    elif row_label == 'Jeep Grand Cherokee SUV':
        return 142
    elif row_label == 'Jeep Compass SUV':
        return 143
    elif row_label == 'Lamborghini Reventon Coupe':
        return 144
    elif row_label == 'Lamborghini Aventador Coupe':
        return 145
    elif row_label == 'Lamborghini Gallardo LP 570-4 Superleggera':
        return 146
    elif row_label == 'Lamborghini Diablo Coupe':
        return 147
    elif row_label == 'Land Rover Range Rover SUV':
        return 148
    elif row_label == 'Land Rover LR2 SUV':
        return 149
    elif row_label == 'Lincoln Town Car Sedan':
        return 150
    elif row_label == 'MINI Cooper Roadster Convertible':
        return 151
    elif row_label == 'Maybach Landaulet Convertible':
        return 152
    elif row_label == 'Mazda Tribute SUV':
        return 153
    elif row_label == 'McLaren MP4-12C Coupe':
        return 154
    elif row_label == 'Mercedes-Benz 300-Class Convertible':
        return 155
    elif row_label == 'Mercedes-Benz C-Class Sedan':
        return 156
    elif row_label == 'Mercedes-Benz SL-Class Coupe':
        return 157
    elif row_label == 'Mercedes-Benz E-Class Sedan':
        return 158
    elif row_label == 'Mercedes-Benz S-Class Sedan':
        return 159
    elif row_label == 'Mercedes-Benz Sprinter Van':
        return 160
    elif row_label == 'Mitsubishi Lancer Sedan':
        return 161
    elif row_label == 'Nissan Leaf Hatchback':
        return 162
    elif row_label == 'Nissan NV Passenger Van':
        return 163
    elif row_label == 'Nissan Juke Hatchback':
        return 164
    elif row_label == 'Nissan 240SX Coupe':
        return 165
    elif row_label == 'Plymouth Neon Coupe':
        return 166
    elif row_label == 'Porsche Panamera Sedan':
        return 167
    elif row_label == 'Ram C/V Cargo Van Minivan':
        return 168
    elif row_label == 'Rolls-Royce Phantom Drophead Coupe Convertible':
        return 169
    elif row_label == 'Rolls-Royce Ghost Sedan':
        return 170
    elif row_label == 'Rolls-Royce Phantom Sedan':
        return 171
    elif row_label == 'Scion xD Hatchback':
        return 172
    elif row_label == 'Spyker C8 Convertible':
        return 173
    elif row_label == 'Spyker C8 Coupe':
        return 174
    elif row_label == 'Suzuki Aerio Sedan':
        return 175
    elif row_label == 'Suzuki Kizashi Sedan':
        return 176
    elif row_label == 'Suzuki SX4 Hatchback':
        return 177
    elif row_label == 'Suzuki SX4 Sedan':
        return 178
    elif row_label == 'Tesla Model S Sedan':
        return 179
    elif row_label == 'Toyota Sequoia SUV':
        return 180
    elif row_label == 'Toyota Camry Sedan':
        return 181
    elif row_label == 'Toyota Corolla Sedan':
        return 182
    elif row_label == 'Toyota 4Runner SUV':
        return 183
    elif row_label == 'Volkswagen Golf Hatchback':
        return 184
    elif row_label == 'Volkswagen Beetle Hatchback':
        return 185
    elif row_label == 'Volvo C30 Hatchback':
        return 186
    elif row_label == 'Volvo 240 Sedan':
        return 187
    elif row_label == 'Volvo XC90 SUV':
        return 188
    elif row_label == 'smart fortwo Convertible':
        return 189
    else:
        None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.compat.v1.python_io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(os.getcwd(), FLAGS.image_dir)
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.compat.v1.app.run()
