#! /usr/bin/env python

import sys
import os
import time

from multiprocess import Pool
import numpy as np

sys.path.append(os.environ['REPO_DIR'] + '/utilities')
from utilities2015 import *
from metadata import *
from data_manager import *
from conversion import images_to_volume

###########################################################

import argparse
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='')
parser.add_argument("stack", type=str, help="Fixed stack name")
parser.add_argument("structure", type=str, help="Structure")
parser.add_argument("detector_id", type=int, help="Detector id")
parser.add_argument("downscale", type=int, help="Downscale factor of reconstructed volume", default=32)
parser.add_argument("-n", "--nissl_only", action='store_true', help="Reconstruct using nissl sections only")
args = parser.parse_args()

stack = args.stack
structure = args.structure
detector_id = args.detector_id
downscale = args.downscale
use_nissl_only = args.nissl_only

###########################################################

voxel_z_size = SECTION_THICKNESS/(XY_PIXEL_DISTANCE_LOSSLESS * downscale)

def load_scoremap_worker(stack, sec, structure, downscale, detector_id):
    try:
        # actual_setting = resolve_actual_setting(setting=classifier_id, stack=stack, sec=sec)
        # sm = DataManager.load_scoremap(stack=stack, section=sec, structure=structure, downscale=downscale, classifier_id=actual_setting)
        sm = DataManager.load_scoremap(stack=stack, section=sec, structure=structure, downscale=downscale, detector_id=detector_id)
        return sm
    except:
        pass

def load_scoremaps_multiple_sections_parallel(sections, stack, structure, downscale, detector_id):
    pool = Pool(12)
    scoremaps = pool.map(lambda sec: load_scoremap_worker(stack, sec, structure, downscale, detector_id=detector_id),
                                     sections)
    pool.close()
    pool.join()
    return {sec: sm for sec, sm in zip(sections, scoremaps) if sm is not None}

def load_downscaled_scoremaps_multiple_sections_sequential(sections, stack, structure, downscale, detector_id):
    scoremaps = {}
    for sec in sections:
        # try:
            # actual_setting = resolve_actual_setting(setting=classifier_id, stack=stack, sec=sec)
            # sm = DataManager.load_downscaled_scoremap(stack=stack, section=sec, structure=structure, downscale=downscale, classifier_id=actual_setting)
        sm = DataManager.load_scoremap(stack=stack, section=sec, structure=structure, downscale=downscale, detector_id=detector_id)
        if sm is not None:
            scoremaps[sec] = sm
        # except:
        #     pass
    return scoremaps

if use_nissl_only:
    assert stack in all_alt_nissl_ntb_stacks or stack in all_alt_nissl_tracing_stacks, "Option \"nissl only\" is only sensible for alternate stained stacks."
    nissl_sections = []
    for sec in metadata_cache['valid_sections'][stack]:
        fn = metadata_cache['sections_to_filenames'][stack][sec]
        if not is_invalid(fn) and fn.split('-')[1][0] == 'N':
            nissl_sections.append(sec)
    used_sections = nissl_sections
else:
    used_sections = metadata_cache['valid_sections'][stack]

t = time.time()
scoremaps = load_downscaled_scoremaps_multiple_sections_sequential(stack=stack, sections=used_sections,
                                                structure=structure, downscale=downscale, detector_id=detector_id)

if len(scoremaps) < 2:
    sys.stderr.write('Number of valid scoremaps for %s is less than 2.\n' % structure)
    sys.exit(1)

sys.stderr.write('Load scoremaps: %.2f seconds\n' % (time.time() - t))

t = time.time()
score_volume, score_volume_bbox = images_to_volume(images=scoremaps, voxel_size=(1, 1, voxel_z_size),
                                                   first_sec=np.min(used_sections)-1, last_sec=np.max(used_sections)-1)
sys.stderr.write('Create score volume: %.2f seconds\n' % (time.time() - t))

#         t = time.time()

score_volume_filepath = DataManager.get_score_volume_filepath(stack=stack, downscale=downscale, structure=structure, detector_id=detector_id, prep_id=2)
create_parent_dir_if_not_exists(score_volume_filepath)
bp.pack_ndarray_file(score_volume.astype(np.float16), score_volume_filepath)
upload_to_s3(score_volume_filepath)

score_volume_bbox_filepath = DataManager.get_score_volume_bbox_filepath(stack=stack, downscale=downscale, structure=structure,
                                                                       detector_id=detector_id, prep_id=2)
np.savetxt(score_volume_bbox_filepath, np.array(score_volume_bbox)[None], fmt='%d')
upload_to_s3(score_volume_bbox_filepath)

del score_volume, scoremaps

#         sys.stderr.write('Save score volume: %.2f seconds\n' % (time.time() - t)) # 1s (down=32)
