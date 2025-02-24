===========
QEMU-ARC README
===========

Building
========

.. code-block:: shell

  mkdir build
  cd build
  ../configure --target-list=arc-softmmu --disable-werror --extra-cflags="-ggdb -O0"
  make


Preparing the firmware
======================

.. code-block:: shell

  python main_fw_extract.py --input <firmware.bin> --output <output_dir> --extract

This will extract the firmware images into the output directory.
If `--extract` is omitted, the script will only generate the JSON files describing the firmware images.

.. code-block:: shell

  python qemu_script_gen.py --inputfile <fw_image_n.bin> --inputjson <fw_image_n.json> --output <output_dir>

This will extract the code/data blocks from the firmware image and generate a
QEMU script that loads them at the correct addresses.

Running 
=======
To run QEMU-ARC from the previous output directory:

.. code-block:: shell
  
  ./qemu_script_<core_name>.sh

The script spawns a gdb server instance and waits for a connection on port 1234.
Execution can be controlled using gdb.

