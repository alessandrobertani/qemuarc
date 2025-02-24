import os
from argparse import ArgumentParser
from json import load
from pathlib import Path

def gen_qemu_script(fw_info, output_dir):
    if fw_info["proc"][:2] == "HS":
        cpu = "archs"
    else:
        cpu = "arcem"
    
    qemu_script = f"""
#!/bin/sh
qemu-system-arc \\
    -s \\
    -S \\
    -nographic \\
    -cpu {cpu} \\
    -kernel /dev/null \\
    -d cpu,in_asm,unimp \\"""

    for image in fw_info.keys():
        if image.startswith("block"):
            addr=fw_info[image]["dst"]
            qemu_script += f"\n\t\t-device loader,file={f'{image}.bin'},addr={hex(addr)},force-raw=on \\"

    qemu_script = qemu_script[:-2]
    qemu_fname = output_dir.joinpath(f"qemu_script_{fw_info['proc'][:-1]}.sh")
    with open(qemu_fname, "w") as f:
        f.write(qemu_script)
    
    os.chmod(qemu_fname, 0o744)    

def split_fw_image(fw_image: Path, fw_info: dict, output_dir: Path):
    with open(fw_image, "rb") as f:
        bindata = f.read()
    
    for image in fw_info.keys():
        if image.startswith("block"):
            with open(output_dir.joinpath(f"{image}.bin"), "wb") as f:
                f.write(bindata[fw_info[image]["src"]:fw_info[image]["src"] + fw_info[image]["blk_size"]])
    
def parse_args():
    parser = ArgumentParser(description='Qemu Script Generator')
    parser.add_argument("-if", "--inputfile", help="input file or path", required=True)
    parser.add_argument("-ij", "--inputjson", help="input json file", required=True)
    parser.add_argument("-o", "--output", help="directory for any output files", required=False)

    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    input = Path(args.inputfile)
    input_json = Path(args.inputjson)
    if args.output:
        outdir = Path(args.output)
    else:
        outdir = Path.cwd()

    if not outdir.exists():
        outdir.mkdir(parents=True)
    
    with open(input_json, "r") as f:
        fw_info = load(f)
    
    split_fw_image(input, fw_info, outdir)
    gen_qemu_script(fw_info, outdir)

if __name__ == '__main__':
    main()