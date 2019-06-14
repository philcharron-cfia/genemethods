#!/usr/bin/env python3
import logging
import shutil
import os
import re
__author__ = 'adamkoziol'


class Compress(object):

    def remove(self):
        """Removes unnecessary temporary files generated by the pipeline"""
        logging.info('Removing large and/or temporary files')
        removefolder = list()
        for sample in self.metadata:
            # Use os.walk to iterate through all the files in the sample output directory
            for path, dirs, files in os.walk(sample.general.outputdirectory):
                for item in files:
                    # Use regex to find files to remove
                    if re.search(".fastq$", item) or re.search(".fastq.gz$", item) or re.search(".bam$", item) \
                            or re.search(".bt2$", item) or re.search(".tab$", item) or re.search("^before", item) \
                            or re.search("^baitedtargets", item) or re.search("_combined.csv$", item) \
                            or re.search("^scaffolds", item) or re.search(".fastg$", item) or re.search(".gfa$", item) \
                            or re.search(".bai$", item) or 'coregenome' in path or 'prophages' in path:
                        # Keep the baitedtargets.fa, core genome, and merged metagenome files
                        if item != 'baitedtargets.fa' and not re.search("coregenome", item) \
                                and not re.search("paired", item):
                            # Remove the unnecessary files
                            try:
                                os.remove(os.path.join(path, item))
                            except IOError:
                                pass
        # Clear out the folders
        for folder in removefolder:
            try:
                shutil.rmtree(folder)
            except (OSError, TypeError):
                pass

    def __init__(self, inputobject):
        self.metadata = inputobject.runmetadata.samples
        self.remove()
