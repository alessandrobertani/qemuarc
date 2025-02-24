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

Bug reporting
=============

The QEMU project uses GitLab issues to track bugs. Bugs
found when running code built from QEMU git or upstream released sources
should be reported via:

* `<https://gitlab.com/qemu-project/qemu/-/issues>`_

If using QEMU via an operating system vendor pre-built binary package, it
is preferable to report bugs to the vendor's own bug tracker first. If
the bug is also known to affect latest upstream code, it can also be
reported via GitLab.

For additional information on bug reporting consult:

* `<https://wiki.qemu.org/Contribute/ReportABug>`_


ChangeLog
=========

For version history and release notes, please visit
`<https://wiki.qemu.org/ChangeLog/>`_ or look at the git history for
more detailed information.


Contact
=======

The QEMU community can be contacted in a number of ways, with the two
main methods being email and IRC:

* `<mailto:qemu-devel@nongnu.org>`_
* `<https://lists.nongnu.org/mailman/listinfo/qemu-devel>`_
* #qemu on irc.oftc.net

Information on additional methods of contacting the community can be
found online via the QEMU website:

* `<https://wiki.qemu.org/Contribute/StartHere>`_
