/*
 * QEMU ARC CPU
 *
 * Copyright (c) 2023 Synopsys Inc.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, see
 * http://www.gnu.org/licenses/lgpl-2.1.html
 */

#include "qemu/osdep.h"
#include "hw/boards.h"
#include "hw/arc/virt.h"
#include "cpu.h"
#include "qemu/units.h"

/*
 * Available command line properties, defined by:
 * their name, parent structure, name inside parent structure, and default value
 */
static Property arc_virt_properties[] = {
    /* Default value kept at 0x8000_0000 for compatibility reasons */
    DEFINE_PROP_UINT64("ram-start", ARCVirtMachineState, ram_start, 0x00000000),
    DEFINE_PROP_END_OF_LIST(),
};

static void arc_virt_machine_init(MachineClass *mc) {
    mc->default_ram_size = 4 * GiB;
    mc->default_cpus = 1;
    mc->default_ram_id = "ram0";
    mc->is_default = true;
}

/* Definition of parent ARC virtual machine */
static void arc_virt_machine_class_init(ObjectClass *oc, void *data)
{   
    printf("****************** Definition of machine %p", oc);
    MachineClass *mc = MACHINE_CLASS(oc);
    // printf("****************** Definition of device %p", oc);
    // DeviceClass *dc = DEVICE_CLASS(oc);

#ifdef TARGET_ARC64
    mc->default_cpu_type = TYPE_ARC_CPU_HS6X;
#else
    mc->default_cpu_type = TYPE_ARC_CPU_ARCHS;
#endif

    //device_class_set_props(dc, arc_virt_properties);
    arc_virt_machine_init(mc);
}

static const TypeInfo arc_virt_machine_info = {
    .name          = TYPE_ARC_VIRT_MACHINE,
    .parent        = TYPE_MACHINE,
    .abstract      = true,
    .instance_size = sizeof(ARCVirtMachineState),
    .class_size    = sizeof(ARCVirtMachineClass),
    .class_init    = arc_virt_machine_class_init,
};

static void machvirt_machine_init(void)
{   
    printf("Initializing virtual machine");
    type_register_static(&arc_virt_machine_info);
}
type_init(machvirt_machine_init);
